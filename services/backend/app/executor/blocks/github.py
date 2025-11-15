"""GitHub block executor - Repository and development automation"""

from typing import Any, Optional
import os
import httpx

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_github_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute a GitHub block for repository operations

    Supports:
    - Repository operations (create, get, update, delete)
    - Issue management (create, update, list, comment)
    - Pull requests (create, merge, review, comment)
    - Branch operations (create, delete, list)
    - File operations (get, create, update)
    - Workflows (trigger, list runs, get logs)
    - Releases (create, list, get)
    """

    logger.info("github_block_executing", block_id=block["id"], action=input_data.get("action", "create_issue"))

    # Get GitHub token
    token = input_data.get("token") or input_data.get("github_token") or os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or provide in block config.")

    # Determine action
    action = input_data.get("action", "create_issue").lower()

    try:
        if action == "create_issue":
            result = await _create_issue(token, input_data)
        elif action == "update_issue":
            result = await _update_issue(token, input_data)
        elif action == "list_issues":
            result = await _list_issues(token, input_data)
        elif action == "add_comment" or action == "comment":
            result = await _add_comment(token, input_data)
        elif action == "create_pr" or action == "create_pull_request":
            result = await _create_pull_request(token, input_data)
        elif action == "merge_pr" or action == "merge_pull_request":
            result = await _merge_pull_request(token, input_data)
        elif action == "list_prs" or action == "list_pull_requests":
            result = await _list_pull_requests(token, input_data)
        elif action == "get_repo" or action == "get_repository":
            result = await _get_repository(token, input_data)
        elif action == "create_repo" or action == "create_repository":
            result = await _create_repository(token, input_data)
        elif action == "get_file" or action == "get_content":
            result = await _get_file_content(token, input_data)
        elif action == "create_file":
            result = await _create_file(token, input_data)
        elif action == "update_file":
            result = await _update_file(token, input_data)
        elif action == "create_branch":
            result = await _create_branch(token, input_data)
        elif action == "list_branches":
            result = await _list_branches(token, input_data)
        elif action == "trigger_workflow":
            result = await _trigger_workflow(token, input_data)
        elif action == "list_workflow_runs":
            result = await _list_workflow_runs(token, input_data)
        elif action == "create_release":
            result = await _create_release(token, input_data)
        elif action == "list_releases":
            result = await _list_releases(token, input_data)
        else:
            raise ValueError(f"Unknown GitHub action: {action}")

        logger.info("github_block_completed", block_id=block["id"], action=action)
        return {"success": True, **result}

    except Exception as e:
        logger.error("github_block_failed", block_id=block["id"], error=str(e))
        raise


async def _create_issue(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new GitHub issue"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    title = input_data.get("title")
    body = input_data.get("body") or input_data.get("description", "")
    assignees = input_data.get("assignees", [])
    labels = input_data.get("labels", [])
    milestone = input_data.get("milestone")

    if not owner or not repo:
        raise ValueError("Owner and repository are required")
    if not title:
        raise ValueError("Issue title is required")

    payload = {
        "title": title,
        "body": body,
    }

    if assignees:
        payload["assignees"] = assignees if isinstance(assignees, list) else [assignees]
    if labels:
        payload["labels"] = labels if isinstance(labels, list) else [labels]
    if milestone:
        payload["milestone"] = milestone

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error: {response.text}")

    issue = response.json()
    return {
        "issue_number": issue.get("number"),
        "issue_id": issue.get("id"),
        "url": issue.get("html_url"),
        "state": issue.get("state"),
    }


async def _update_issue(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Update an existing GitHub issue"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    issue_number = input_data.get("issue_number") or input_data.get("number")
    title = input_data.get("title")
    body = input_data.get("body")
    state = input_data.get("state")  # open or closed
    assignees = input_data.get("assignees")
    labels = input_data.get("labels")

    if not owner or not repo or not issue_number:
        raise ValueError("Owner, repository, and issue_number are required")

    payload = {}
    if title:
        payload["title"] = title
    if body:
        payload["body"] = body
    if state:
        payload["state"] = state
    if assignees is not None:
        payload["assignees"] = assignees if isinstance(assignees, list) else [assignees]
    if labels is not None:
        payload["labels"] = labels if isinstance(labels, list) else [labels]

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    issue = response.json()
    return {
        "issue_number": issue.get("number"),
        "url": issue.get("html_url"),
        "state": issue.get("state"),
        "updated": True,
    }


async def _list_issues(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List issues in a repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    state = input_data.get("state", "open")  # open, closed, all
    labels = input_data.get("labels")
    assignee = input_data.get("assignee")
    per_page = input_data.get("per_page", 30)

    if not owner or not repo:
        raise ValueError("Owner and repository are required")

    params = {
        "state": state,
        "per_page": per_page,
    }

    if labels:
        params["labels"] = ",".join(labels) if isinstance(labels, list) else labels
    if assignee:
        params["assignee"] = assignee

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params=params,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    issues = response.json()
    return {
        "issues": [
            {
                "number": issue.get("number"),
                "id": issue.get("id"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "url": issue.get("html_url"),
                "created_at": issue.get("created_at"),
                "updated_at": issue.get("updated_at"),
                "labels": [label.get("name") for label in issue.get("labels", [])],
            }
            for issue in issues
        ],
        "count": len(issues),
    }


async def _add_comment(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Add a comment to an issue or pull request"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    issue_number = input_data.get("issue_number") or input_data.get("number") or input_data.get("pr_number")
    body = input_data.get("body") or input_data.get("comment")

    if not owner or not repo or not issue_number:
        raise ValueError("Owner, repository, and issue_number are required")
    if not body:
        raise ValueError("Comment body is required")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json={"body": body},
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error: {response.text}")

    comment = response.json()
    return {
        "comment_id": comment.get("id"),
        "url": comment.get("html_url"),
        "created_at": comment.get("created_at"),
    }


async def _create_pull_request(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new pull request"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    title = input_data.get("title")
    head = input_data.get("head") or input_data.get("head_branch")
    base = input_data.get("base") or input_data.get("base_branch", "main")
    body = input_data.get("body") or input_data.get("description", "")
    draft = input_data.get("draft", False)

    if not owner or not repo:
        raise ValueError("Owner and repository are required")
    if not title or not head:
        raise ValueError("Title and head branch are required")

    payload = {
        "title": title,
        "head": head,
        "base": base,
        "body": body,
        "draft": draft,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/pulls",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error: {response.text}")

    pr = response.json()
    return {
        "pr_number": pr.get("number"),
        "pr_id": pr.get("id"),
        "url": pr.get("html_url"),
        "state": pr.get("state"),
        "draft": pr.get("draft"),
    }


async def _merge_pull_request(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Merge a pull request"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    pr_number = input_data.get("pr_number") or input_data.get("number")
    commit_title = input_data.get("commit_title")
    commit_message = input_data.get("commit_message")
    merge_method = input_data.get("merge_method", "merge")  # merge, squash, rebase

    if not owner or not repo or not pr_number:
        raise ValueError("Owner, repository, and pr_number are required")

    payload = {
        "merge_method": merge_method,
    }

    if commit_title:
        payload["commit_title"] = commit_title
    if commit_message:
        payload["commit_message"] = commit_message

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    result = response.json()
    return {
        "merged": result.get("merged", False),
        "sha": result.get("sha"),
        "message": result.get("message"),
    }


async def _list_pull_requests(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List pull requests in a repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    state = input_data.get("state", "open")  # open, closed, all
    per_page = input_data.get("per_page", 30)

    if not owner or not repo:
        raise ValueError("Owner and repository are required")

    params = {
        "state": state,
        "per_page": per_page,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params=params,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    prs = response.json()
    return {
        "pull_requests": [
            {
                "number": pr.get("number"),
                "id": pr.get("id"),
                "title": pr.get("title"),
                "state": pr.get("state"),
                "url": pr.get("html_url"),
                "created_at": pr.get("created_at"),
                "updated_at": pr.get("updated_at"),
                "draft": pr.get("draft"),
            }
            for pr in prs
        ],
        "count": len(prs),
    }


async def _get_repository(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get repository information"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")

    if not owner or not repo:
        raise ValueError("Owner and repository are required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    repo_data = response.json()
    return {
        "id": repo_data.get("id"),
        "name": repo_data.get("name"),
        "full_name": repo_data.get("full_name"),
        "description": repo_data.get("description"),
        "url": repo_data.get("html_url"),
        "default_branch": repo_data.get("default_branch"),
        "stars": repo_data.get("stargazers_count"),
        "forks": repo_data.get("forks_count"),
        "open_issues": repo_data.get("open_issues_count"),
        "private": repo_data.get("private"),
        "created_at": repo_data.get("created_at"),
        "updated_at": repo_data.get("updated_at"),
    }


async def _create_repository(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new repository"""

    name = input_data.get("name")
    description = input_data.get("description", "")
    private = input_data.get("private", False)
    auto_init = input_data.get("auto_init", False)

    if not name:
        raise ValueError("Repository name is required")

    payload = {
        "name": name,
        "description": description,
        "private": private,
        "auto_init": auto_init,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error: {response.text}")

    repo = response.json()
    return {
        "id": repo.get("id"),
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "url": repo.get("html_url"),
        "clone_url": repo.get("clone_url"),
    }


async def _get_file_content(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get file content from repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    path = input_data.get("path") or input_data.get("file_path")
    ref = input_data.get("ref") or input_data.get("branch", "main")

    if not owner or not repo or not path:
        raise ValueError("Owner, repository, and file path are required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params={"ref": ref},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    file_data = response.json()

    # Decode base64 content
    import base64
    content = base64.b64decode(file_data.get("content", "")).decode("utf-8")

    return {
        "content": content,
        "sha": file_data.get("sha"),
        "path": file_data.get("path"),
        "size": file_data.get("size"),
        "url": file_data.get("html_url"),
    }


async def _create_file(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a file in repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    path = input_data.get("path") or input_data.get("file_path")
    content = input_data.get("content")
    message = input_data.get("message") or input_data.get("commit_message", f"Create {path}")
    branch = input_data.get("branch", "main")

    if not owner or not repo or not path or content is None:
        raise ValueError("Owner, repository, path, and content are required")

    # Encode content to base64
    import base64
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    payload = {
        "message": message,
        "content": encoded_content,
        "branch": branch,
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error: {response.text}")

    result = response.json()
    return {
        "path": path,
        "sha": result.get("content", {}).get("sha"),
        "url": result.get("content", {}).get("html_url"),
        "commit_sha": result.get("commit", {}).get("sha"),
    }


async def _update_file(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Update a file in repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    path = input_data.get("path") or input_data.get("file_path")
    content = input_data.get("content")
    sha = input_data.get("sha")  # Required for updates
    message = input_data.get("message") or input_data.get("commit_message", f"Update {path}")
    branch = input_data.get("branch", "main")

    if not owner or not repo or not path or content is None or not sha:
        raise ValueError("Owner, repository, path, content, and sha are required")

    # Encode content to base64
    import base64
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    payload = {
        "message": message,
        "content": encoded_content,
        "sha": sha,
        "branch": branch,
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    result = response.json()
    return {
        "path": path,
        "sha": result.get("content", {}).get("sha"),
        "url": result.get("content", {}).get("html_url"),
        "commit_sha": result.get("commit", {}).get("sha"),
    }


async def _create_branch(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new branch"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    branch_name = input_data.get("branch") or input_data.get("branch_name")
    from_branch = input_data.get("from_branch", "main")

    if not owner or not repo or not branch_name:
        raise ValueError("Owner, repository, and branch_name are required")

    # Get SHA of the source branch
    async with httpx.AsyncClient() as client:
        # First get the ref of the source branch
        ref_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{from_branch}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            timeout=30.0,
        )

        if ref_response.status_code != 200:
            raise Exception(f"GitHub API error getting source branch: {ref_response.text}")

        sha = ref_response.json().get("object", {}).get("sha")

        # Create new branch
        create_response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/git/refs",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json={
                "ref": f"refs/heads/{branch_name}",
                "sha": sha,
            },
            timeout=30.0,
        )

    if create_response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error creating branch: {create_response.text}")

    result = create_response.json()
    return {
        "branch": branch_name,
        "ref": result.get("ref"),
        "sha": result.get("object", {}).get("sha"),
    }


async def _list_branches(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List branches in repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    per_page = input_data.get("per_page", 30)

    if not owner or not repo:
        raise ValueError("Owner and repository are required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/branches",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params={"per_page": per_page},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    branches = response.json()
    return {
        "branches": [
            {
                "name": branch.get("name"),
                "protected": branch.get("protected"),
                "commit_sha": branch.get("commit", {}).get("sha"),
            }
            for branch in branches
        ],
        "count": len(branches),
    }


async def _trigger_workflow(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Trigger a GitHub Actions workflow"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    workflow_id = input_data.get("workflow_id") or input_data.get("workflow")
    ref = input_data.get("ref") or input_data.get("branch", "main")
    inputs = input_data.get("inputs", {})

    if not owner or not repo or not workflow_id:
        raise ValueError("Owner, repository, and workflow_id are required")

    payload = {
        "ref": ref,
    }

    if inputs:
        payload["inputs"] = inputs

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 204:
        raise Exception(f"GitHub API error: {response.text}")

    return {"triggered": True, "workflow_id": workflow_id, "ref": ref}


async def _list_workflow_runs(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List workflow runs"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    workflow_id = input_data.get("workflow_id")
    per_page = input_data.get("per_page", 30)

    if not owner or not repo:
        raise ValueError("Owner and repository are required")

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    if workflow_id:
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params={"per_page": per_page},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    result = response.json()
    runs = result.get("workflow_runs", [])

    return {
        "runs": [
            {
                "id": run.get("id"),
                "name": run.get("name"),
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
                "created_at": run.get("created_at"),
                "updated_at": run.get("updated_at"),
                "url": run.get("html_url"),
            }
            for run in runs
        ],
        "count": len(runs),
    }


async def _create_release(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new release"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    tag_name = input_data.get("tag_name") or input_data.get("tag")
    name = input_data.get("name") or tag_name
    body = input_data.get("body") or input_data.get("description", "")
    draft = input_data.get("draft", False)
    prerelease = input_data.get("prerelease", False)

    if not owner or not repo or not tag_name:
        raise ValueError("Owner, repository, and tag_name are required")

    payload = {
        "tag_name": tag_name,
        "name": name,
        "body": body,
        "draft": draft,
        "prerelease": prerelease,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/releases",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"GitHub API error: {response.text}")

    release = response.json()
    return {
        "release_id": release.get("id"),
        "tag_name": release.get("tag_name"),
        "name": release.get("name"),
        "url": release.get("html_url"),
        "draft": release.get("draft"),
        "prerelease": release.get("prerelease"),
    }


async def _list_releases(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List releases in repository"""

    owner = input_data.get("owner") or input_data.get("repo_owner")
    repo = input_data.get("repo") or input_data.get("repository")
    per_page = input_data.get("per_page", 30)

    if not owner or not repo:
        raise ValueError("Owner and repository are required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/releases",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params={"per_page": per_page},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.text}")

    releases = response.json()
    return {
        "releases": [
            {
                "id": release.get("id"),
                "tag_name": release.get("tag_name"),
                "name": release.get("name"),
                "url": release.get("html_url"),
                "created_at": release.get("created_at"),
                "published_at": release.get("published_at"),
                "draft": release.get("draft"),
                "prerelease": release.get("prerelease"),
            }
            for release in releases
        ],
        "count": len(releases),
    }
