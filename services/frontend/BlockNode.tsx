import { Handle, Position, NodeProps } from 'reactflow';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface BlockNodeData {
  label: string;
  type: string;
  status?: 'idle' | 'running' | 'success' | 'error';
}

const statusColors = {
  idle: 'border-gray-300',
  running: 'border-blue-500 ring-4 ring-blue-500/20',
  success: 'border-green-500',
  error: 'border-red-500',
};

export function BlockNode({ data, selected }: NodeProps<BlockNodeData>) {
  const status = data.status || 'idle';

  return (
    <Card className={cn(
      'w-64 border-2 shadow-sm',
      statusColors[status],
      selected && 'ring-4 ring-indigo-500/30 border-indigo-500'
    )}>
      <Handle type="target" position={Position.Top} className="!bg-gray-400" />
      
      <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
        <CardTitle className="text-sm font-medium">{data.label}</CardTitle>
        <div className={cn(
          'h-2 w-2 rounded-full',
          status === 'running' && 'bg-blue-500',
          status === 'success' && 'bg-green-500',
          status === 'error' && 'bg-red-500',
          status === 'idle' && 'bg-gray-300',
        )} />
      </CardHeader>

      <Handle type="source" position={Position.Bottom} className="!bg-gray-400" />
    </Card>
  );
}
