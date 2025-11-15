import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
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
        return <CheckCircle className="h-5 w-5 text-green-600" />
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-600" />
      case 'running':
        return <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
      case 'cancelled':
        return <StopCircle className="h-5 w-5 text-gray-600" />
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-600" />
      default:
        return <Clock className="h-5 w-5 text-gray-600" />
    }
  }

  const getStatusBadge = (status: string) => {
    const styles = {
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      running: 'bg-blue-100 text-blue-800',
      cancelled: 'bg-gray-100 text-gray-800',
      pending: 'bg-yellow-100 text-yellow-800',
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
      <div className="border-b bg-white px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-bold text-2xl">Execution Logs</h1>
            <p className="mt-1 text-gray-600 text-sm">
              Monitor and debug your workflow executions
            </p>
          </div>
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="mr-2 h-4 w-4" />
            Filters
          </Button>
        </div>

        {showFilters && (
          <div className="mt-4 flex gap-2">
            {['all', 'running', 'completed', 'failed', 'cancelled', 'pending'].map(
              (status) => (
                <Button
                  key={status}
                  variant={statusFilter === status ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setStatusFilter(status)}
                >
                  {status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1)}
                </Button>
              )
            )}
          </div>
        )}
      </div>

      <div className="p-8">
        {error && (
          <div className="mb-6 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
            <button
              onClick={clearError}
              className="ml-auto text-red-600 hover:text-red-800"
            >
              ×
            </button>
          </div>
        )}

        <div className="mb-6 relative">
          <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search executions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        {isLoading && executions.length === 0 ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        ) : filteredExecutions.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <PlayCircle className="mb-4 h-12 w-12 text-gray-400" />
            <h3 className="mb-2 font-semibold text-gray-900 text-lg">
              {searchQuery ? 'No executions found' : 'No executions yet'}
            </h3>
            <p className="text-gray-600 text-sm">
              {searchQuery
                ? 'Try adjusting your search query'
                : 'Execute a workflow to see logs here'}
            </p>
          </div>
        ) : (
          <Card>
            <CardContent className="p-0">
              <div className="divide-y">
                {filteredExecutions.map((exec) => (
                  <div
                    key={exec.id}
                    className="flex cursor-pointer items-center justify-between p-4 transition hover:bg-gray-50"
                    onClick={() => handleViewDetails(exec.id)}
                  >
                    <div className="flex items-center gap-4">
                      {getStatusIcon(exec.status)}
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="font-medium">
                            {exec.workflow_name || exec.workflow_id}
                          </p>
                          {getStatusBadge(exec.status)}
                        </div>
                        <div className="mt-1 flex items-center gap-3 text-gray-500 text-xs">
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {formatDistanceToNow(new Date(exec.created_at), {
                              addSuffix: true,
                            })}
                          </span>
                          {exec.error_message && (
                            <span className="text-red-600">
                              Error: {exec.error_message.substring(0, 50)}
                              {exec.error_message.length > 50 ? '...' : ''}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <p className="text-gray-500 text-sm">Duration</p>
                        <p className="font-medium">
                          {formatDuration(exec.duration_ms)}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        {exec.status === 'running' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => handleCancelExecution(exec.id, e)}
                            disabled={isLoading}
                          >
                            <StopCircle className="mr-2 h-4 w-4" />
                            Cancel
                          </Button>
                        )}
                        <Button variant="ghost" size="sm">
                          View Details
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
