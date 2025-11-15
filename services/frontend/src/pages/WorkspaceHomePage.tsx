import { useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Plus, Workflow, Database, Activity, ArrowRight, Loader2, LayoutTemplate, Wrench } from 'lucide-react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { useWorkflowStore } from '@/stores/workflowStore'
import { useKnowledgeStore } from '@/stores/knowledgeStore'
import { useExecutionStore } from '@/stores/executionStore'
import { formatDistanceToNow } from 'date-fns'

export default function WorkspaceHomePage() {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

  const { workflows, isLoading: workflowsLoading, fetchWorkflows } = useWorkflowStore()
  const { knowledgeBases, isLoading: kbLoading, fetchKnowledgeBases } = useKnowledgeStore()
  const { executions, isLoading: executionsLoading, fetchExecutions } = useExecutionStore()

  useEffect(() => {
    fetchWorkflows()
    fetchKnowledgeBases()
    fetchExecutions({ limit: 5 })
  }, [fetchWorkflows, fetchKnowledgeBases, fetchExecutions])

  const stats = [
    {
      label: 'Workflows',
      value: workflowsLoading ? '...' : workflows.length.toString(),
      icon: Workflow,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      link: `/workspace/${workspaceId}/workflows`
    },
    {
      label: 'Knowledge Bases',
      value: kbLoading ? '...' : knowledgeBases.length.toString(),
      icon: Database,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      link: `/workspace/${workspaceId}/knowledge`
    },
    {
      label: 'Executions',
      value: executionsLoading ? '...' : executions.length.toString(),
      icon: Activity,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      link: `/workspace/${workspaceId}/logs`
    },
  ]

  return (
    <div className="flex-1 overflow-auto p-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-bold text-3xl">Welcome back!</h1>
          <p className="mt-2 text-gray-600">Here's what's happening with your workspace</p>
        </div>

        {/* Stats */}
        <div className="mb-8 grid gap-6 md:grid-cols-3">
          {stats.map((stat) => (
            <Link key={stat.label} to={stat.link}>
              <Card className="cursor-pointer transition-all hover:shadow-lg">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="font-medium text-sm">{stat.label}</CardTitle>
                  <div className={cn('rounded-lg p-2', stat.bgColor)}>
                    <stat.icon className={cn('h-5 w-5', stat.color)} />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="font-bold text-2xl">{stat.value}</div>
                  <div className="mt-2 flex items-center text-gray-600 text-xs">
                    <span>View all</span>
                    <ArrowRight className="ml-1 h-3 w-3" />
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="mb-4 font-semibold text-xl">Quick Actions</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card className="cursor-pointer transition hover:shadow-md">
              <Link to={`/workspace/${workspaceId}/workflows`}>
                <CardHeader>
                  <div className="mb-2 inline-flex rounded-lg bg-purple-100 p-3 w-fit">
                    <Plus className="h-6 w-6 text-purple-600" />
                  </div>
                  <CardTitle>Create Workflow</CardTitle>
                  <CardDescription>
                    Start building a new AI workflow
                  </CardDescription>
                </CardHeader>
              </Link>
            </Card>

            <Card className="cursor-pointer transition hover:shadow-md">
              <Link to={`/workspace/${workspaceId}/templates`}>
                <CardHeader>
                  <div className="mb-2 inline-flex rounded-lg bg-indigo-100 p-3 w-fit">
                    <LayoutTemplate className="h-6 w-6 text-indigo-600" />
                  </div>
                  <CardTitle>Browse Templates</CardTitle>
                  <CardDescription>
                    Use pre-built workflow templates
                  </CardDescription>
                </CardHeader>
              </Link>
            </Card>

            <Card className="cursor-pointer transition hover:shadow-md">
              <Link to={`/workspace/${workspaceId}/tools`}>
                <CardHeader>
                  <div className="mb-2 inline-flex rounded-lg bg-cyan-100 p-3 w-fit">
                    <Wrench className="h-6 w-6 text-cyan-600" />
                  </div>
                  <CardTitle>Manage Tools</CardTitle>
                  <CardDescription>
                    Configure MCP servers and tools
                  </CardDescription>
                </CardHeader>
              </Link>
            </Card>

            <Card className="cursor-pointer transition hover:shadow-md">
              <Link to={`/workspace/${workspaceId}/knowledge`}>
                <CardHeader>
                  <div className="mb-2 inline-flex rounded-lg bg-blue-100 p-3 w-fit">
                    <Database className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle>Add Knowledge</CardTitle>
                  <CardDescription>
                    Upload documents for RAG
                  </CardDescription>
                </CardHeader>
              </Link>
            </Card>
          </div>
        </div>

        {/* Recent Workflows */}
        <div className="mb-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-semibold text-xl">Recent Workflows</h2>
            <Button variant="ghost" size="sm" asChild>
              <Link to={`/workspace/${workspaceId}/workflows`}>
                View all <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
          {workflowsLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
            </div>
          ) : workflows.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Workflow className="mb-2 h-8 w-8 text-gray-400" />
                <p className="text-gray-600 text-sm">No workflows yet</p>
                <Button className="mt-4" size="sm" asChild>
                  <Link to={`/workspace/${workspaceId}/workflows`}>
                    <Plus className="mr-2 h-4 w-4" />
                    Create your first workflow
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {workflows.slice(0, 6).map((workflow) => (
                <Card
                  key={workflow.id}
                  className="cursor-pointer transition hover:shadow-md"
                  onClick={() => navigate(`/workspace/${workspaceId}/workflows/${workflow.id}`)}
                >
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-base">
                      <Workflow className="h-4 w-4 text-purple-600" />
                      {workflow.name}
                    </CardTitle>
                    <CardDescription className="line-clamp-2 text-xs">
                      {workflow.description || 'No description'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between text-gray-600 text-xs">
                      <span>
                        {formatDistanceToNow(new Date(workflow.updated_at), { addSuffix: true })}
                      </span>
                      {workflow.is_deployed && (
                        <span className="rounded-full bg-green-100 px-2 py-0.5 text-green-700">
                          Deployed
                        </span>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Recent Executions */}
        <div>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-semibold text-xl">Recent Executions</h2>
            <Button variant="ghost" size="sm" asChild>
              <Link to={`/workspace/${workspaceId}/logs`}>
                View all <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
          <Card>
            <CardContent className="pt-6">
              {executionsLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
                </div>
              ) : executions.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-8">
                  <Activity className="mb-2 h-6 w-6 text-gray-400" />
                  <p className="text-gray-600 text-sm">No executions yet</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {executions.slice(0, 5).map((execution: any) => (
                    <div key={execution.id} className="flex items-center gap-4">
                      <div className={cn(
                        'flex h-10 w-10 items-center justify-center rounded-full',
                        execution.status === 'completed' ? 'bg-green-100' :
                        execution.status === 'failed' ? 'bg-red-100' :
                        execution.status === 'running' ? 'bg-blue-100' :
                        'bg-gray-100'
                      )}>
                        <Activity className={cn(
                          'h-5 w-5',
                          execution.status === 'completed' ? 'text-green-600' :
                          execution.status === 'failed' ? 'text-red-600' :
                          execution.status === 'running' ? 'text-blue-600' :
                          'text-gray-600'
                        )} />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-sm">
                          {execution.workflow?.name || 'Workflow'} {execution.status}
                        </p>
                        <p className="text-gray-500 text-sm">
                          {formatDistanceToNow(new Date(execution.started_at), { addSuffix: true })}
                        </p>
                      </div>
                      <div className="text-right">
                        <span className={cn(
                          'rounded-full px-2 py-0.5 text-xs',
                          execution.status === 'completed' ? 'bg-green-100 text-green-700' :
                          execution.status === 'failed' ? 'bg-red-100 text-red-700' :
                          execution.status === 'running' ? 'bg-blue-100 text-blue-700' :
                          'bg-gray-100 text-gray-700'
                        )}>
                          {execution.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}
