// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

type RequestOptions = RequestInit & { skipAuth?: boolean }

// Custom error class for API errors
export class APIError extends Error {
  status: number
  detail?: any

  constructor(message: string, status: number, detail?: any) {
    super(message)
    this.name = 'APIError'
    this.status = status
    this.detail = detail
  }
}

async function request<T>(path: string, init: RequestOptions = {}): Promise<T> {
  const headers = new Headers(init.headers ?? {})

  // Set Content-Type for JSON payloads
  if (!headers.has('Content-Type') && init.body && typeof init.body === 'string') {
    headers.set('Content-Type', 'application/json')
  }

  // Add Authorization header
  if (!init.skipAuth && !headers.has('Authorization')) {
    const token = localStorage.getItem('access_token')
    if (token) {
      headers.set('Authorization', `Bearer ${token}`)
    }
  }

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers,
      cache: 'no-store',
    })

    if (!response.ok) {
      let detail = response.statusText
      try {
        const body = await response.json()
        detail = body.detail ?? JSON.stringify(body)
      } catch {
        detail = await response.text()
      }
      throw new APIError(
        detail || `API request failed`,
        response.status,
        detail
      )
    }

    if (response.status === 204) {
      // @ts-ignore - explicit undefined for no content
      return undefined
    }

    return (await response.json()) as T
  } catch (error) {
    if (error instanceof APIError) {
      throw error
    }
    throw new APIError(
      error instanceof Error ? error.message : 'Network error',
      0
    )
  }
}

// Multipart form data request
async function uploadRequest<T>(
  path: string,
  formData: FormData,
  onProgress?: (progress: number) => void
): Promise<T> {
  const token = localStorage.getItem('access_token')

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress((e.loaded / e.total) * 100)
      }
    })

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve(response as T)
        } catch {
          resolve(xhr.responseText as T)
        }
      } else {
        reject(new APIError(xhr.statusText, xhr.status))
      }
    })

    xhr.addEventListener('error', () => {
      reject(new APIError('Network error', 0))
    })

    xhr.open('POST', `${API_BASE_URL}${path}`)
    if (token) {
      xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    }
    xhr.send(formData)
  })
}

// ========================================
// TYPE DEFINITIONS
// ========================================

// -------- User & Auth --------

export interface User {
  id: string
  email: string
  name: string
  email_verified: boolean
  image?: string | null
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string // email
  password: string
}

export interface SignupRequest {
  email: string
  password: string
  name: string
}

export interface AuthResponse {
  token: string
  refresh_token?: string
  user: {
    id: string
    email: string
    name: string
  }
}

export interface TokenResponse {
  access_token: string
  token_type: string
  refresh_token?: string
}

// -------- Workflows --------

export interface WorkflowSummary {
  id: string
  name: string
  description?: string | null
  updated_at: string
  created_at: string
  is_deployed: boolean
  folder_id?: string | null
  blocks: WorkflowBlock[]
  edges: WorkflowEdge[]
}

export interface WorkflowBlock {
  id: string
  name: string
  type: string
  position: { x: number; y: number }
  data?: Record<string, unknown>
}

export interface WorkflowEdge {
  id: string
  source: string
  target: string
  sourceHandle?: string | null
  targetHandle?: string | null
}

export interface CreateWorkflowRequest {
  name: string
  description?: string
  folder_id?: string
  blocks?: WorkflowBlock[]
  edges?: WorkflowEdge[]
}

export interface UpdateWorkflowRequest {
  name?: string
  description?: string
  folder_id?: string
  blocks?: WorkflowBlock[]
  edges?: WorkflowEdge[]
}

export interface ExecuteWorkflowRequest {
  input_data?: Record<string, unknown>
  config?: Record<string, unknown>
}

export interface ExecutionResult {
  execution_id: string
  status: 'running' | 'completed' | 'failed'
  result?: any
  error?: string
}

// ========================================
// API FUNCTIONS
// ========================================

// -------- Authentication --------

export async function signup(data: SignupRequest): Promise<AuthResponse> {
  return request('/auth/signup', {
    method: 'POST',
    body: JSON.stringify(data),
    skipAuth: true,
  })
}

export async function login(data: LoginRequest): Promise<TokenResponse> {
  // OAuth2 requires form-encoded data
  const formData = new URLSearchParams()
  formData.append('username', data.username)
  formData.append('password', data.password)

  return request('/auth/login', {
    method: 'POST',
    body: formData.toString(),
    skipAuth: true,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
}

export async function getCurrentUser(): Promise<User> {
  return request('/auth/me')
}

export async function getSocketToken(): Promise<{ token: string }> {
  return request('/auth/socket-token', {
    method: 'POST',
  })
}

export async function refreshToken(refreshToken: string): Promise<TokenResponse> {
  return request('/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
    skipAuth: true,
  })
}

// -------- Workflows --------

export async function listWorkflows(): Promise<WorkflowSummary[]> {
  const data = await request<{ workflows: WorkflowSummary[] }>('/workflows/')
  return data.workflows
}

export async function getWorkflow(workflowId: string): Promise<WorkflowSummary> {
  const data = await request<{ workflow: WorkflowSummary }>(`/workflows/${workflowId}`)
  return data.workflow
}

export async function createWorkflow(data: CreateWorkflowRequest): Promise<WorkflowSummary> {
  const result = await request<{ workflow: WorkflowSummary }>('/workflows/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return result.workflow
}

export async function updateWorkflow(
  workflowId: string,
  data: UpdateWorkflowRequest
): Promise<WorkflowSummary> {
  const result = await request<{ workflow: WorkflowSummary }>(`/workflows/${workflowId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  return result.workflow
}

export async function deleteWorkflow(workflowId: string): Promise<void> {
  await request(`/workflows/${workflowId}`, {
    method: 'DELETE',
  })
}

export async function executeWorkflow(
  workflowId: string,
  data: ExecuteWorkflowRequest
): Promise<ExecutionResult> {
  return request(`/workflows/${workflowId}/execute`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function validateWorkflow(workflowId: string): Promise<{
  valid: boolean
  errors?: string[]
}> {
  return request(`/workflows/${workflowId}/validate`, {
    method: 'POST',
  })
}

export async function createWorkflowSnapshot(workflowId: string): Promise<{
  snapshot_id: string
}> {
  return request(`/workflows/${workflowId}/snapshot`, {
    method: 'POST',
  })
}

export async function deployWorkflow(workflowId: string, config?: Record<string, unknown>): Promise<{
  deployment_id: string
  status: string
}> {
  return request(`/workflows/${workflowId}/deploy`, {
    method: 'POST',
    body: JSON.stringify(config || {}),
  })
}

// -------- Blocks --------

export interface BlockType {
  type: string
  label: string
  description: string
  category: string
  icon?: string
  inputs?: Record<string, unknown>
  outputs?: Record<string, unknown>
}

export async function listBlocks(): Promise<BlockType[]> {
  const data = await request<{ blocks: BlockType[] }>('/blocks')
  return data.blocks
}

export async function getBlockTypes(): Promise<string[]> {
  const data = await request<{ types: string[] }>('/blocks/types')
  return data.types
}

export async function validateBlockConfig(config: Record<string, unknown>): Promise<{
  valid: boolean
  errors?: string[]
}> {
  return request('/blocks/validate', {
    method: 'POST',
    body: JSON.stringify(config),
  })
}

// -------- Executions --------

export interface Execution {
  id: string
  workflow_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  input_data?: Record<string, unknown>
  output_data?: Record<string, unknown>
  error?: string
  started_at?: string
  completed_at?: string
  created_at: string
}

export interface ExecutionLog {
  id: string
  execution_id: string
  level: 'debug' | 'info' | 'warning' | 'error'
  message: string
  timestamp: string
  metadata?: Record<string, unknown>
}

export async function listExecutions(params?: {
  workflow_id?: string
  status?: string
  limit?: number
  offset?: number
}): Promise<Execution[]> {
  const query = new URLSearchParams()
  if (params?.workflow_id) query.append('workflow_id', params.workflow_id)
  if (params?.status) query.append('status', params.status)
  if (params?.limit) query.append('limit', params.limit.toString())
  if (params?.offset) query.append('offset', params.offset.toString())

  const data = await request<{ executions: Execution[] }>(
    `/executions?${query.toString()}`
  )
  return data.executions
}

export async function getExecution(executionId: string): Promise<Execution> {
  const data = await request<{ execution: Execution }>(`/executions/${executionId}`)
  return data.execution
}

export async function cancelExecution(executionId: string): Promise<void> {
  await request(`/executions/${executionId}/cancel`, {
    method: 'POST',
  })
}

export async function getExecutionLogs(executionId: string): Promise<ExecutionLog[]> {
  const data = await request<{ logs: ExecutionLog[] }>(`/executions/${executionId}/logs`)
  return data.logs
}

// -------- Knowledge Base --------

export interface KnowledgeBase {
  id: string
  name: string
  description?: string
  workspace_id?: string
  created_at: string
  updated_at: string
  document_count?: number
}

export interface Document {
  id: string
  knowledge_base_id: string
  title: string
  content?: string
  file_path?: string
  mime_type?: string
  size?: number
  tags?: string[]
  created_at: string
  updated_at: string
  chunk_count?: number
}

export interface DocumentChunk {
  id: string
  document_id: string
  content: string
  position: number
  metadata?: Record<string, unknown>
  embedding?: number[]
}

export async function listKnowledgeBases(): Promise<KnowledgeBase[]> {
  const data = await request<{ knowledge_bases: KnowledgeBase[] }>('/knowledge')
  return data.knowledge_bases
}

export async function createKnowledgeBase(data: {
  name: string
  description?: string
  workspace_id?: string
}): Promise<KnowledgeBase> {
  const result = await request<{ knowledge_base: KnowledgeBase }>('/knowledge', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return result.knowledge_base
}

export async function getKnowledgeBase(kbId: string): Promise<KnowledgeBase> {
  const data = await request<{ knowledge_base: KnowledgeBase }>(`/knowledge/${kbId}`)
  return data.knowledge_base
}

export async function updateKnowledgeBase(
  kbId: string,
  data: { name?: string; description?: string }
): Promise<KnowledgeBase> {
  const result = await request<{ knowledge_base: KnowledgeBase }>(`/knowledge/${kbId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  return result.knowledge_base
}

export async function deleteKnowledgeBase(kbId: string): Promise<void> {
  await request(`/knowledge/${kbId}`, {
    method: 'DELETE',
  })
}

export async function listDocuments(kbId: string): Promise<Document[]> {
  const data = await request<{ documents: Document[] }>(`/knowledge/${kbId}/documents`)
  return data.documents
}

export async function uploadDocument(
  kbId: string,
  file: File,
  metadata?: { title?: string; tags?: string[] },
  onProgress?: (progress: number) => void
): Promise<Document> {
  const formData = new FormData()
  formData.append('file', file)
  if (metadata?.title) formData.append('title', metadata.title)
  if (metadata?.tags) formData.append('tags', JSON.stringify(metadata.tags))

  const result = await uploadRequest<{ document: Document }>(
    `/knowledge/${kbId}/documents`,
    formData,
    onProgress
  )
  return result.document
}

export async function getDocument(kbId: string, documentId: string): Promise<Document> {
  const data = await request<{ document: Document }>(
    `/knowledge/${kbId}/documents/${documentId}`
  )
  return data.document
}

export async function deleteDocument(kbId: string, documentId: string): Promise<void> {
  await request(`/knowledge/${kbId}/documents/${documentId}`, {
    method: 'DELETE',
  })
}

export async function updateDocument(
  kbId: string,
  documentId: string,
  data: { name?: string; tags?: string[]; metadata?: Record<string, any> }
): Promise<Document> {
  const result = await request<{ document: Document }>(
    `/knowledge/${kbId}/documents/${documentId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    }
  );
  return result.document;
}

export async function processDocument(kbId: string, documentId: string): Promise<void> {
  await request(`/knowledge/${kbId}/documents/${documentId}/process`, {
    method: 'POST',
  });
}

export async function searchKnowledgeBase(
  kbId: string,
  query: string,
  limit?: number
): Promise<{
  results: Array<{
    document: Document
    chunks: DocumentChunk[]
    score: number
  }>
}> {
  return request(`/knowledge/${kbId}/search`, {
    method: 'POST',
    body: JSON.stringify({ query, limit }),
  })
}

// -------- Files --------

export interface FileInfo {
  id: string
  path: string
  name: string
  size: number
  mime_type: string
  url: string
  created_at: string
}

export async function uploadFile(
  file: File,
  onProgress?: (progress: number) => void
): Promise<FileInfo> {
  const formData = new FormData()
  formData.append('file', file)

  const result = await uploadRequest<{ file: FileInfo }>(
    '/files/upload',
    formData,
    onProgress
  )
  return result.file
}

export async function uploadFiles(
  files: File[],
  onProgress?: (progress: number) => void
): Promise<FileInfo[]> {
  const formData = new FormData()
  files.forEach((file) => formData.append('files', file))

  const result = await uploadRequest<{ files: FileInfo[] }>(
    '/files/upload/batch',
    formData,
    onProgress
  )
  return result.files
}

export async function downloadFile(filePath: string): Promise<Blob> {
  const response = await fetch(
    `${API_BASE_URL}/files/download?path=${encodeURIComponent(filePath)}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    }
  )
  if (!response.ok) throw new APIError('Download failed', response.status)
  return response.blob()
}

export async function deleteFile(filePath: string): Promise<void> {
  await request('/files/delete', {
    method: 'DELETE',
    body: JSON.stringify({ path: filePath }),
  })
}

export async function getPresignedUrl(fileName: string): Promise<{ url: string; path: string }> {
  return request('/files/presigned', {
    method: 'POST',
    body: JSON.stringify({ file_name: fileName }),
  })
}

// -------- Organizations & Workspaces --------

export interface Organization {
  id: string
  name: string
  slug: string
  created_at: string
  updated_at: string
}

export interface Workspace {
  id: string
  organization_id: string
  name: string
  slug: string
  created_at: string
  updated_at: string
}

export interface OrganizationMember {
  id: string
  user_id: string
  organization_id: string
  role: 'owner' | 'admin' | 'member'
  created_at: string
}

export async function listOrganizations(): Promise<Organization[]> {
  const data = await request<{ organizations: Organization[] }>('/organizations')
  return data.organizations
}

export async function createOrganization(data: {
  name: string
  slug: string
}): Promise<Organization> {
  const result = await request<{ organization: Organization }>('/organizations', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return result.organization
}

export async function getOrganization(orgId: string): Promise<Organization> {
  const data = await request<{ organization: Organization }>(`/organizations/${orgId}`)
  return data.organization
}

export async function listWorkspaces(orgId: string): Promise<Workspace[]> {
  const data = await request<{ workspaces: Workspace[] }>(
    `/organizations/${orgId}/workspaces`
  )
  return data.workspaces
}

export async function createWorkspace(
  orgId: string,
  data: { name: string; slug: string }
): Promise<Workspace> {
  const result = await request<{ workspace: Workspace }>(
    `/organizations/${orgId}/workspaces`,
    {
      method: 'POST',
      body: JSON.stringify(data),
    }
  )
  return result.workspace
}

// -------- Folders --------

export interface Folder {
  id: string
  name: string
  parent_id?: string | null
  workspace_id?: string
  created_at: string
  updated_at: string
  children?: Folder[]
}

export async function listFolders(params?: { workspace_id?: string }): Promise<Folder[]> {
  const query = params?.workspace_id ? `?workspace_id=${params.workspace_id}` : ''
  const data = await request<{ folders: Folder[] }>(`/folders${query}`)
  return data.folders
}

export async function createFolder(data: {
  name: string
  parent_id?: string
  workspace_id?: string
}): Promise<Folder> {
  const result = await request<{ folder: Folder }>('/folders', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return result.folder
}

export async function updateFolder(
  folderId: string,
  data: { name?: string; parent_id?: string }
): Promise<Folder> {
  const result = await request<{ folder: Folder }>(`/folders/${folderId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  return result.folder
}

export async function deleteFolder(folderId: string): Promise<void> {
  await request(`/folders/${folderId}`, {
    method: 'DELETE',
  })
}

export async function getFolderTree(workspaceId?: string): Promise<Folder[]> {
  const query = workspaceId ? `?workspace_id=${workspaceId}` : ''
  const data = await request<{ tree: Folder[] }>(`/folders/tree${query}`)
  return data.tree
}

// -------- Chat --------

export interface ChatRequestPayload {
  message: string
  conversation_id?: string
  workflow_id?: string
  stream?: boolean
  model?: string
}

export interface ChatResponsePayload {
  conversation_id: string
  message: string
  role: string
  metadata?: Record<string, any>
}

export async function sendChatMessage(payload: ChatRequestPayload): Promise<ChatResponsePayload> {
  return request<ChatResponsePayload>('/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// -------- Copilot --------

export interface CopilotSuggestion {
  type: string
  title: string
  description: string
  code?: string
  confidence: number
}

export async function getCopilotSuggestions(payload: {
  prompt: string
  context?: Record<string, unknown>
}): Promise<{
  suggestions: CopilotSuggestion[]
  explanation?: string
}> {
  return request('/copilot/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function getCopilotStats(): Promise<{
  total_requests: number
  total_tokens: number
  avg_response_time: number
}> {
  return request('/copilot/stats')
}

// -------- Billing --------

export interface BillingSummary {
  subscription?: {
    plan: string
    status: string
    period_end?: string
  }
  usage: {
    workflow_executions: number
    api_calls: number
    storage_gb: number
  }
  limits?: {
    max_workflows: number
    max_executions_per_month: number
  }
}

export async function getBilling(): Promise<BillingSummary> {
  return request('/billing')
}

export async function createPortalSession(): Promise<{ url: string }> {
  return request('/billing/portal', {
    method: 'POST',
  })
}

// -------- Templates --------

export interface Template {
  id: string
  name: string
  description: string | null
  category: 'marketing' | 'sales' | 'finance' | 'support' | 'ai' | 'other'
  icon: string
  color: string
  workflow_state: any
  views: number
  uses: number
  is_public: boolean
  author_name: string
  author_avatar: string | null
  user_id: string
  workspace_id: string
  created_at: string
  updated_at: string
  star_count: number
  user_has_starred: boolean
}

export interface TemplateListItem {
  id: string
  name: string
  description: string | null
  category: string
  icon: string
  color: string
  views: number
  uses: number
  is_public: boolean
  author_name: string
  author_avatar: string | null
  created_at: string
  updated_at: string
  star_count: number
  user_has_starred: boolean
}

export interface TemplateListResponse {
  templates: TemplateListItem[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface TemplateCreate {
  name: string
  description?: string
  category?: string
  icon?: string
  color?: string
  is_public?: boolean
  workflow_state: any
  author_name: string
  author_avatar?: string
}

export interface TemplateUpdate {
  name?: string
  description?: string
  category?: string
  icon?: string
  color?: string
  is_public?: boolean
  workflow_state?: any
}

export async function listTemplates(params?: {
  skip?: number
  limit?: number
  category?: string
  search?: string
  sort_by?: 'created_at' | 'views' | 'uses' | 'name'
  sort_order?: 'asc' | 'desc'
  my_templates?: boolean
}): Promise<TemplateListResponse> {
  const queryParams = new URLSearchParams()
  if (params?.skip !== undefined) queryParams.set('skip', params.skip.toString())
  if (params?.limit !== undefined) queryParams.set('limit', params.limit.toString())
  if (params?.category) queryParams.set('category', params.category)
  if (params?.search) queryParams.set('search', params.search)
  if (params?.sort_by) queryParams.set('sort_by', params.sort_by)
  if (params?.sort_order) queryParams.set('sort_order', params.sort_order)
  if (params?.my_templates !== undefined) queryParams.set('my_templates', params.my_templates.toString())

  return request(`/templates?${queryParams.toString()}`)
}

export async function getTemplate(id: string): Promise<Template> {
  return request(`/templates/${id}`)
}

export async function createTemplate(data: TemplateCreate): Promise<Template> {
  return request('/templates', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function updateTemplate(id: string, data: TemplateUpdate): Promise<Template> {
  return request(`/templates/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

export async function deleteTemplate(id: string): Promise<void> {
  return request(`/templates/${id}`, {
    method: 'DELETE',
  })
}

export async function starTemplate(id: string): Promise<{ message: string }> {
  return request(`/templates/${id}/star`, {
    method: 'POST',
  })
}

export async function unstarTemplate(id: string): Promise<void> {
  return request(`/templates/${id}/star`, {
    method: 'DELETE',
  })
}

export async function useTemplate(
  id: string,
  params?: {
    workflow_name?: string
    folder_id?: string
  }
): Promise<WorkflowSummary> {
  return request(`/templates/${id}/use`, {
    method: 'POST',
    body: JSON.stringify(params || {}),
  })
}
