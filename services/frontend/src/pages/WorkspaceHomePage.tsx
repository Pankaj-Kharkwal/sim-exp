import { useEffect } from 'react'
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
      color: 'text-purple-300',
      bgColor: 'bg-purple-500/20',
      link: `/workspace/${workspaceId}/workflows`
    },
    {
      label: 'Knowledge Bases',
      value: kbLoading ? '...' : knowledgeBases.length.toString(),
      icon: Database,
      color: 'text-blue-300',
      bgColor: 'bg-blue-500/20',
      link: `/workspace/${workspaceId}/knowledge`
    },
    {
      label: 'Executions',
      value: executionsLoading ? '...' : executions.length.toString(),
      icon: Activity,
      color: 'text-green-300',
      bgColor: 'bg-green-500/20',
      link: `/workspace/${workspaceId}/logs`
    },
  ]

  return (
    <div className="flex-1 overflow-auto">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8 fade-in">
          <h1 className="font-bold text-3xl text-white">Welcome back!</h1>
          <p className="mt-2 text-white/70">Here's what's happening with your workspace</p>
        </div>

        {/* Stats */}
        <div className="mb-8 grid gap-6 md:grid-cols-3">
          {stats.map((stat, index) => (
            <Link key={stat.label} to={stat.link} className="fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="glass-card stat-card group cursor-pointer shimmer">
                <div className="flex items-center justify-between mb-4">
                  <div className="stat-label">{stat.label}</div>
                  <div className={cn('rounded-lg p-2', stat.bgColor)}>
                    <stat.icon className={cn('h-5 w-5', stat.color)} />
                  </div>
                </div>
                <div className="stat-value mb-2">{stat.value}</div>
                <div className="flex items-center text-white/60 text-xs group-hover:text-white/80 transition-colors">
                  <span>View all</span>
                  <ArrowRight className="ml-1 h-3 w-3" />
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="mb-4 font-semibold text-xl text-white fade-in" style={{ animationDelay: '0.3s' }}>Quick Actions</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Link to={`/workspace/${workspaceId}/workflows`} className="fade-in" style={{ animationDelay: '0.4s' }}>
              <div className="glass-card p-6 cursor-pointer group">
                <div className="mb-4 inline-flex rounded-lg bg-purple-500/20 p-3 w-fit">
                  <Plus className="h-6 w-6 text-purple-300" />
                </div>
                <h3 className="font-semibold text-white mb-2">Create Workflow</h3>
                <p className="text-sm text-white/70">
                  Start building a new AI workflow
                </p>
              </div>
            </Link>

            <Link to={`/workspace/${workspaceId}/templates`} className="fade-in" style={{ animationDelay: '0.5s' }}>
              <div className="glass-card p-6 cursor-pointer group">
                <div className="mb-4 inline-flex rounded-lg bg-indigo-500/20 p-3 w-fit">
                  <LayoutTemplate className="h-6 w-6 text-indigo-300" />
                </div>
                <h3 className="font-semibold text-white mb-2">Browse Templates</h3>
                <p className="text-sm text-white/70">
                  Use pre-built workflow templates
                </p>
              </div>
            </Link>

            <Link to={`/workspace/${workspaceId}/tools`} className="fade-in" style={{ animationDelay: '0.6s' }}>
              <div className="glass-card p-6 cursor-pointer group">
                <div className="mb-4 inline-flex rounded-lg bg-cyan-500/20 p-3 w-fit">
                  <Wrench className="h-6 w-6 text-cyan-300" />
                </div>
                <h3 className="font-semibold text-white mb-2">Manage Tools</h3>
                <p className="text-sm text-white/70">
                  Configure MCP servers and tools
                </p>
              </div>
            </Link>

            <Link to={`/workspace/${workspaceId}/knowledge`} className="fade-in" style={{ animationDelay: '0.7s' }}>
              <div className="glass-card p-6 cursor-pointer group">
                <div className="mb-4 inline-flex rounded-lg bg-blue-500/20 p-3 w-fit">
                  <Database className="h-6 w-6 text-blue-300" />
                </div>
                <h3 className="font-semibold text-white mb-2">Add Knowledge</h3>
                <p className="text-sm text-white/70">
                  Upload documents for RAG
                </p>
              </div>
            </Link>
          </div>
        </div>

        {/* Recent Workflows */}
        <div className="mb-8 fade-in" style={{ animationDelay: '0.8s' }}>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-semibold text-xl text-white">Recent Workflows</h2>
            <Link to={`/workspace/${workspaceId}/workflows`} className="glass-button px-4 py-2 text-sm">
              View all <ArrowRight className="ml-1 h-4 w-4 inline" />
            </Link>
          </div>
          {workflowsLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-white/40" />
            </div>
          ) : workflows.length === 0 ? (
            <div className="glass-card p-12 text-center">
              <Workflow className="mb-2 h-8 w-8 text-white/40 mx-auto" />
              <p className="text-white/70 text-sm mb-4">No workflows yet</p>
              <Link to={`/workspace/${workspaceId}/workflows`} className="glass-button px-6 py-3 inline-flex items-center bg-gradient-to-r from-purple-500/30 to-blue-500/30">
                <Plus className="mr-2 h-4 w-4" />
                Create your first workflow
              </Link>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {workflows.slice(0, 6).map((workflow, index) => (
                <div
                  key={workflow.id}
                  className="glass-card p-6 cursor-pointer group fade-in"
                  style={{ animationDelay: `${(index + 8) * 0.1}s` }}
                  onClick={() => navigate(`/workspace/${workspaceId}/workflows/${workflow.id}`)}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Workflow className="h-4 w-4 text-purple-300" />
                    <h3 className="font-semibold text-white">{workflow.name}</h3>
                  </div>
                  <p className="text-sm text-white/70 line-clamp-2 mb-4 min-h-[2.5rem]">
                    {workflow.description || 'No description'}
                  </p>
                  <div className="flex items-center justify-between text-white/60 text-xs">
                    <span>
                      {formatDistanceToNow(new Date(workflow.updated_at), { addSuffix: true })}
                    </span>
                    {workflow.is_deployed && (
                      <span className="glass-badge success text-xs px-2 py-0.5">
                        Deployed
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Executions */}
        <div className="fade-in" style={{ animationDelay: '0.9s' }}>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-semibold text-xl text-white">Recent Executions</h2>
            <Link to={`/workspace/${workspaceId}/logs`} className="glass-button px-4 py-2 text-sm">
              View all <ArrowRight className="ml-1 h-4 w-4 inline" />
            </Link>
          </div>
          <div className="glass-card p-6">
            {executionsLoading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-white/40" />
              </div>
            ) : executions.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8">
                <Activity className="mb-2 h-6 w-6 text-white/40" />
                <p className="text-white/70 text-sm">No executions yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {executions.slice(0, 5).map((execution: any) => (
                  <div key={execution.id} className="flex items-center gap-4">
                    <div className={cn(
                      'flex h-10 w-10 items-center justify-center rounded-full',
                      execution.status === 'completed' ? 'bg-green-500/20' :
                      execution.status === 'failed' ? 'bg-red-500/20' :
                      execution.status === 'running' ? 'bg-blue-500/20' :
                      'bg-white/10'
                    )}>
                      <Activity className={cn(
                        'h-5 w-5',
                        execution.status === 'completed' ? 'text-green-300' :
                        execution.status === 'failed' ? 'text-red-300' :
                        execution.status === 'running' ? 'text-blue-300' :
                        'text-white/60'
                      )} />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm text-white">
                        {execution.workflow?.name || 'Workflow'} {execution.status}
                      </p>
                      <p className="text-white/60 text-sm">
                        {formatDistanceToNow(new Date(execution.started_at), { addSuffix: true })}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className={cn(
                        'glass-badge text-xs px-2 py-0.5',
                        execution.status === 'completed' ? 'bg-green-500/20 text-green-300' :
                        execution.status === 'failed' ? 'bg-red-500/20 text-red-300' :
                        execution.status === 'running' ? 'bg-blue-500/20 text-blue-300' :
                        'bg-white/10 text-white/70'
                      )}>
                        {execution.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}
