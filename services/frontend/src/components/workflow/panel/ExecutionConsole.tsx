import { useState, useMemo } from 'react'
import { Loader2, RefreshCw, Clock } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { useExecutionStore } from '@/stores/executionStore'

interface ExecutionConsoleProps {
  workflowId: string
}

const LEVEL_COLORS: Record<string, string> = {
  debug: 'bg-slate-100 text-slate-700',
  info: 'bg-blue-100 text-blue-800',
  warning: 'bg-amber-100 text-amber-800',
  error: 'bg-rose-100 text-rose-800',
}

const STATUS_COLORS: Record<string, string> = {
  pending: 'bg-slate-100 text-slate-800',
  running: 'bg-blue-100 text-blue-800',
  completed: 'bg-emerald-100 text-emerald-800',
  failed: 'bg-rose-100 text-rose-800',
  cancelled: 'bg-amber-100 text-amber-800',
}

export function ExecutionConsole({ workflowId }: ExecutionConsoleProps) {
  const logs = useExecutionStore((state) => state.logs)
  const currentExecution = useExecutionStore((state) => state.currentExecution)
  const isLoading = useExecutionStore((state) => state.isLoading)
  const fetchExecution = useExecutionStore((state) => state.fetchExecution)
  const fetchLogs = useExecutionStore((state) => state.fetchLogs)
  const cancelExecution = useExecutionStore((state) => state.cancelExecution)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const executionId = currentExecution?.id
  const status = currentExecution?.status ?? 'idle'
  const statusBadgeClass = STATUS_COLORS[status] ?? 'bg-slate-100 text-slate-700'

  const durationLabel = useMemo(() => {
    if (!currentExecution?.started_at) return null
    if (!currentExecution.completed_at) return 'Running…'
    if (!currentExecution.duration_ms) return null
    return `${(currentExecution.duration_ms / 1000).toFixed(1)}s`
  }, [currentExecution])

  const handleRefresh = async () => {
    if (!executionId) return
    setIsRefreshing(true)
    try {
      await Promise.all([fetchExecution(executionId), fetchLogs(executionId)])
    } finally {
      setIsRefreshing(false)
    }
  }

  const handleCancel = async () => {
    if (!executionId) return
    await cancelExecution(executionId)
  }

  if (!workflowId) {
    return (
      <div className='flex h-full items-center justify-center px-6 text-center text-sm text-muted-foreground'>
        Select a workflow to start running and viewing execution logs.
      </div>
    )
  }

  return (
    <div className='flex h-full flex-col'>
      <div className='border-b px-4 py-3'>
        <div className='flex items-center justify-between'>
          <div>
            <p className='text-sm font-semibold text-slate-900'>Workflow Run</p>
            <div className='flex items-center gap-2 text-xs text-slate-500'>
              <Badge variant='outline' className={statusBadgeClass}>
                {status}
              </Badge>
              {executionId && (
                <span className='font-mono text-[11px] text-slate-500'>#{executionId.slice(-6)}</span>
              )}
              {durationLabel && (
                <span className='inline-flex items-center gap-1'>
                  <Clock className='h-3 w-3' />
                  {durationLabel}
                </span>
              )}
            </div>
          </div>
          <div className='flex items-center gap-2'>
            {status === 'running' && (
              <Button size='sm' variant='outline' onClick={handleCancel}>
                Cancel run
              </Button>
            )}
            <Button size='icon' variant='ghost' onClick={handleRefresh} disabled={!executionId || isRefreshing}>
              {isRefreshing ? <Loader2 className='h-4 w-4 animate-spin' /> : <RefreshCw className='h-4 w-4' />}
            </Button>
          </div>
        </div>
      </div>

      {isLoading && (
        <div className='flex items-center justify-center px-4 py-3 text-sm text-muted-foreground'>
          <Loader2 className='mr-2 h-4 w-4 animate-spin' />
          Preparing execution logs…
        </div>
      )}

      {!executionId && !isLoading && (
        <div className='flex flex-1 flex-col items-center justify-center gap-2 px-6 text-center text-sm text-muted-foreground'>
          <p className='font-medium text-slate-900'>No run yet</p>
          <p className='text-sm text-slate-500'>
            Click <strong>Execute</strong> to run this workflow and stream logs here.
          </p>
        </div>
      )}

      {executionId && (
        <ScrollArea className='flex-1 px-4 py-3'>
          {logs.length === 0 ? (
            <div className='rounded-md border border-dashed border-slate-200 px-4 py-8 text-center text-sm text-slate-500'>
              Waiting for logs…
            </div>
          ) : (
            <div className='space-y-3'>
              {logs.map((log) => (
                <div
                  key={`${log.id}-${log.timestamp}`}
                  className='rounded-lg border border-slate-100 bg-slate-50/80 p-3 text-sm shadow-sm'
                >
                  <div className='mb-1 flex items-center justify-between'>
                    <span className='font-mono text-[11px] text-slate-500'>
                      {new Date(log.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit',
                      })}
                    </span>
                    <Badge variant='outline' className={LEVEL_COLORS[log.level] ?? LEVEL_COLORS.info}>
                      {log.level}
                    </Badge>
                  </div>
                  <p className='text-slate-800'>{log.message}</p>
                  {log.metadata && (
                    <pre className='mt-2 rounded bg-white/80 p-2 text-xs text-slate-600'>
                      {JSON.stringify(log.metadata, null, 2)}
                    </pre>
                  )}
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      )}
    </div>
  )
}
