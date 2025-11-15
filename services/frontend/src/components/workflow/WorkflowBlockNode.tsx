import React, { memo } from 'react'
import { Handle, Position, type NodeProps } from 'reactflow'
import {
  Box,
  Zap,
  Code,
  Database,
  Mail,
  MessageSquare,
  FileText,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import { getParameterCompletion, isParameterValueSet } from '@/lib/workflow/blockConfig'
import type { BlockData } from '@/types/workflow'

const getBlockIcon = (type: string) => {
  const iconMap: Record<string, React.ElementType> = {
    api: Zap,
    function: Code,
    database: Database,
    email: Mail,
    chat: MessageSquare,
    file: FileText,
    default: Box,
  }
  return iconMap[type] || iconMap.default
}

const getBlockColor = (type: string) => {
  const colorMap: Record<string, string> = {
    api: 'from-blue-500 to-blue-600',
    function: 'from-purple-500 to-purple-600',
    database: 'from-green-500 to-green-600',
    email: 'from-orange-500 to-orange-600',
    chat: 'from-pink-500 to-pink-600',
    file: 'from-slate-500 to-slate-600',
    default: 'from-slate-400 to-slate-500',
  }
  return colorMap[type] || colorMap.default
}

export const WorkflowBlockNode = memo(({ data, selected }: NodeProps<BlockData>) => {
  const Icon = getBlockIcon(data.type)
  const colorClass = getBlockColor(data.type)
  const { definition, requiredComplete, requiredTotal } = getParameterCompletion(
    data.type,
    data.config
  )
  const needsConfiguration = requiredTotal > 0 && requiredComplete < requiredTotal
  const visibleParameters = definition?.parameters.slice(0, 3) ?? []
  const remainingParameters =
    definition && definition.parameters.length > visibleParameters.length
      ? definition.parameters.length - visibleParameters.length
      : 0

  return (
    <div
      className={cn(
        'min-w-[220px] rounded-xl border bg-white shadow-sm transition-all',
        selected
          ? 'border-indigo-500 ring-4 ring-indigo-100 shadow-lg'
          : 'border-slate-200 hover:shadow-md'
      )}
    >
      <Handle
        type='target'
        position={Position.Top}
        className='!h-3 !w-3 !rounded-full !border-2 !border-white !bg-slate-400'
      />

      <div className={cn('rounded-t-xl px-4 py-3 text-white', `bg-gradient-to-r ${colorClass}`)}>
        <div className='flex items-center justify-between gap-2'>
          <div className='flex items-center gap-2'>
            <Icon className='h-4 w-4' />
            <div>
              <p className='text-[11px] font-medium uppercase leading-none tracking-wide opacity-75'>
                {data.type}
              </p>
              <p className='text-sm font-semibold leading-tight'>{data.name}</p>
            </div>
          </div>
          <Badge
            variant='secondary'
            className={cn(
              'border-white/30 bg-white/20 text-[10px] font-medium text-white',
              needsConfiguration && 'bg-yellow-200/80 text-amber-800'
            )}
          >
            {needsConfiguration ? 'Needs config' : 'Ready'}
          </Badge>
        </div>
        {definition?.description && (
          <p className='mt-2 text-xs text-white/80 line-clamp-2'>{definition.description}</p>
        )}
      </div>

      <div className='px-4 py-3 space-y-3'>
        <div>
          <div className='flex items-center justify-between text-[11px] uppercase tracking-wide text-slate-400'>
            <span>Parameters</span>
            {requiredTotal > 0 && (
              <span>
                {requiredComplete}/{requiredTotal} required
              </span>
            )}
          </div>

          {definition && definition.parameters.length > 0 ? (
            <div className='mt-2 flex flex-wrap gap-1.5'>
              {visibleParameters.map((param) => {
                const configured = isParameterValueSet(data.config?.[param.name])
                return (
                  <Badge
                    key={param.name}
                    variant='outline'
                    className={cn(
                      'flex items-center gap-1 border-slate-200 bg-slate-50 text-[11px] font-normal text-slate-600',
                      configured && 'border-emerald-200 bg-emerald-50 text-emerald-700',
                      !configured && param.required && 'border-amber-200 bg-amber-50 text-amber-700'
                    )}
                  >
                    {configured ? (
                      <CheckCircle2 className='h-3 w-3' />
                    ) : (
                      <AlertCircle className='h-3 w-3' />
                    )}
                    {param.name}
                  </Badge>
                )
              })}
              {remainingParameters > 0 && (
                <Badge
                  variant='outline'
                  className='border-slate-200 bg-white text-[10px] font-medium text-slate-500'
                >
                  +{remainingParameters} more
                </Badge>
              )}
            </div>
          ) : (
            <p className='mt-2 text-xs text-slate-400'>No parameters</p>
          )}
        </div>

        {definition?.outputs?.length ? (
          <div>
            <p className='text-[11px] uppercase tracking-wide text-slate-400'>Outputs</p>
            <div className='mt-2 flex flex-wrap gap-1.5'>
              {definition.outputs.slice(0, 3).map((output) => (
                <Badge
                  key={output}
                  variant='secondary'
                  className='bg-slate-100 text-[11px] font-normal text-slate-600'
                >
                  {output}
                </Badge>
              ))}
              {definition.outputs.length > 3 && (
                <Badge
                  variant='secondary'
                  className='bg-slate-100 text-[10px] font-medium text-slate-500'
                >
                  +{definition.outputs.length - 3}
                </Badge>
              )}
            </div>
          </div>
        ) : null}
      </div>

      <Handle
        type='source'
        position={Position.Bottom}
        className='!h-3 !w-3 !rounded-full !border-2 !border-white !bg-slate-400'
      />
    </div>
  )
})

WorkflowBlockNode.displayName = 'WorkflowBlockNode'
