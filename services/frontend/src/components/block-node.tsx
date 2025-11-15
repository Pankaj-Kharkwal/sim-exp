import { Handle, Position, type NodeProps } from 'reactflow'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface BlockNodeData {
  name: string
  type: string
  status?: 'idle' | 'running' | 'success' | 'error'
}

const statusStyles: Record<string, string> = {
  idle: 'border-muted',
  running: 'border-blue-500 ring-4 ring-blue-500/20',
  success: 'border-emerald-500',
  error: 'border-destructive',
}

export function BlockNode({ data, selected }: NodeProps<BlockNodeData>) {
  const status = data.status ?? 'idle'
  return (
    <Card
      className={cn(
        'w-64 border-2 shadow-sm transition-all duration-150',
        statusStyles[status],
        selected && 'ring-4 ring-indigo-500/30 border-indigo-500'
      )}
    >
      <Handle type='target' position={Position.Top} className='!bg-muted-foreground/50' />
      <CardHeader className='flex flex-row items-center justify-between space-y-0 p-3'>
        <CardTitle className='text-sm font-medium'>{data.name}</CardTitle>
        <div
          className={cn(
            'h-2 w-2 rounded-full',
            status === 'running' && 'bg-blue-500',
            status === 'success' && 'bg-emerald-500',
            status === 'error' && 'bg-destructive',
            status === 'idle' && 'bg-muted-foreground/40'
          )}
        />
      </CardHeader>
      <CardContent className='pb-3 text-xs text-muted-foreground capitalize'>
        {data.type}
      </CardContent>
      <Handle type='source' position={Position.Bottom} className='!bg-muted-foreground/50' />
    </Card>
  )
}
