import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  Search,
  CheckCircle,
  XCircle,
  Clock,
  Filter,
  Loader2,
  AlertCircle,
  PlayCircle,
  StopCircle,
  Calendar,
  X,
  ChevronRight
} from 'lucide-react'
import { useExecutionStore } from '@/stores/executionStore'
import { formatDistanceToNow } from 'date-fns'

export default function LogsPage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [showFilters, setShowFilters] = useState(false)

  const {
    executions,
    isLoading,
    error,
    fetchExecutions,
    cancelExecution,
    clearError,
  } = useExecutionStore()

  // Get workflow_id from URL params if present
  const workflowId = searchParams.get('workflow_id') || undefined

  useEffect(() => {
    fetchExecutions({
      workflow_id: workflowId,
      status: statusFilter === 'all' ? undefined : statusFilter,
    })
  }, [fetchExecutions, workflowId, statusFilter])

  const handleCancelExecution = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm('Are you sure you want to cancel this execution?')) return

    try {
      await cancelExecution(id)
    } catch (error) {
      console.error('Failed to cancel execution:', error)
    }
  }

  const handleViewDetails = (executionId: string) => {
    navigate(`/executions/${executionId}`)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-300" />
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-300" />
      case 'running':
        return <Loader2 className="h-5 w-5 animate-spin text-blue-300" />
      case 'cancelled':
        return <StopCircle className="h-5 w-5 text-white/60" />
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-300" />
      default:
        return <Clock className="h-5 w-5 text-white/60" />
    }
  }

  const getStatusBadge = (status: string) => {
    const styles = {
      completed: 'bg-green-500/20 text-green-300',
      failed: 'bg-red-500/20 text-red-300',
      running: 'bg-blue-500/20 text-blue-300',
      cancelled: 'bg-white/10 text-white/70',
      pending: 'bg-yellow-500/20 text-yellow-300',
    }
    return (
      <span
        className={`inline-flex rounded-full px-2 py-1 font-medium text-xs ${
          styles[status as keyof typeof styles] || styles.pending
        }`}
      >
        {status}
      </span>
    )
  }

  const formatDuration = (ms?: number) => {
    if (!ms) return '-'
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${(ms / 60000).toFixed(1)}m`
  }

  const filteredExecutions = executions.filter((exec) =>
    exec.workflow_name?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="flex-1 overflow-auto">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-6 fade-in">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-bold text-3xl text-white">Execution Logs</h1>
              <p className="mt-2 text-white/70">
                Monitor and debug your workflow executions
              </p>
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={cn('glass-button px-4 py-2', showFilters && 'bg-purple-500/30')}
            >
              <Filter className="mr-2 h-4 w-4" />
              Filters
            </button>
          </div>

          {showFilters && (
            <div className="mt-4 flex flex-wrap gap-2 fade-in">
              {['all', 'running', 'completed', 'failed', 'cancelled', 'pending'].map(
                (status) => (
                  <button
                    key={status}
                    className={cn(
                      'glass-button px-3 py-1.5 text-sm',
                      statusFilter === status && 'bg-purple-500/30'
                    )}
                    onClick={() => setStatusFilter(status)}
                  >
                    {status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1)}
                  </button>
                )
              )}
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="glass-card mb-6 border-2 border-red-500/30 bg-red-500/10 p-4 fade-in">
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-red-300" />
              <span className="text-sm text-red-200">{error}</span>
              <button onClick={clearError} className="glass-button ml-auto p-2">
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Search */}
        <div className="relative mb-6 fade-in" style={{ animationDelay: '0.1s' }}>
          <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-white/40" />
          <input
            placeholder="Search executions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="glass-input w-full pl-10"
          />
        </div>

        {/* Executions List */}
        {isLoading && executions.length === 0 ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-white/40" />
          </div>
        ) : filteredExecutions.length === 0 ? (
          <div className="glass-card flex flex-col items-center justify-center py-12 text-center fade-in" style={{ animationDelay: '0.2s' }}>
            <PlayCircle className="mb-4 h-12 w-12 text-white/40" />
            <h3 className="mb-2 font-semibold text-lg text-white">
              {searchQuery ? 'No executions found' : 'No executions yet'}
            </h3>
            <p className="text-sm text-white/70">
              {searchQuery
                ? 'Try adjusting your search query'
                : 'Execute a workflow to see logs here'}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredExecutions.map((exec, index) => (
              <div
                key={exec.id}
                className="glass-card group cursor-pointer p-6 fade-in"
                style={{ animationDelay: `${0.2 + index * 0.05}s` }}
                onClick={() => handleViewDetails(exec.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 flex-1">
                    {getStatusIcon(exec.status)}
                    <div className="flex-1">
                      <div className="mb-1 flex items-center gap-2">
                        <p className="font-medium text-white">
                          {exec.workflow_name || exec.workflow_id}
                        </p>
                        {getStatusBadge(exec.status)}
                      </div>
                      <div className="flex flex-wrap items-center gap-3 text-xs text-white/60">
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {formatDistanceToNow(new Date(exec.created_at), {
                            addSuffix: true,
                          })}
                        </span>
                        {exec.error_message && (
                          <span className="text-red-300">
                            Error: {exec.error_message.substring(0, 50)}
                            {exec.error_message.length > 50 ? '...' : ''}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <p className="text-sm text-white/60">Duration</p>
                      <p className="font-medium text-white">
                        {formatDuration(exec.duration_ms)}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      {exec.status === 'running' && (
                        <button
                          className="glass-button px-3 py-1.5 text-sm"
                          onClick={(e) => handleCancelExecution(exec.id, e)}
                          disabled={isLoading}
                        >
                          <StopCircle className="mr-2 h-4 w-4" />
                          Cancel
                        </button>
                      )}
                      <button className="glass-button p-2">
                        <ChevronRight className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}
