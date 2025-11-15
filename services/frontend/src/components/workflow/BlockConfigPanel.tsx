import { useEffect, useMemo, useState } from 'react'
import { SlidersHorizontal, Trash2, Copy, CheckCircle2, Info } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { getBlockDefinition } from '@/lib/blocks/blockDefinitions'
import {
  getParameterCompletion,
  isParameterValueSet,
} from '@/lib/workflow/blockConfig'
import { useWorkflowEditorStore } from '@/stores/workflowEditorStore'

export function BlockConfigPanel() {
  const {
    nodes,
    selectedNodeId,
    updateNode,
    deleteNode,
    duplicateNode,
    clearSelection,
  } = useWorkflowEditorStore()

  const selectedNode = nodes.find((node) => node.id === selectedNodeId)
  const [draftValues, setDraftValues] = useState<Record<string, string>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})

  const { definition, requiredComplete, requiredTotal } = useMemo(() => {
    if (!selectedNode) {
      return { definition: undefined, requiredComplete: 0, requiredTotal: 0 }
    }
    return getParameterCompletion(selectedNode.data.type, selectedNode.data.config)
  }, [selectedNode])

  useEffect(() => {
    if (!selectedNode) {
      setDraftValues({})
      setErrors({})
      return
    }
    const blockDefinition = getBlockDefinition(selectedNode.data.type)
    if (!blockDefinition) {
      setDraftValues({})
      setErrors({})
      return
    }
    const nextDraft: Record<string, string> = {}
    blockDefinition.parameters.forEach((param) => {
      if (param.type === 'json' || param.type === 'array') {
        const value = selectedNode.data.config?.[param.name]
        nextDraft[param.name] = value !== undefined ? JSON.stringify(value, null, 2) : ''
      }
    })
    setDraftValues(nextDraft)
    setErrors({})
  }, [selectedNodeId])

  const handleNameChange = (value: string) => {
    if (!selectedNode) return
    updateNode(selectedNode.id, { name: value })
  }

  const applyConfigChange = (paramName: string, value: any) => {
    if (!selectedNode) return
    const currentConfig = selectedNode.data.config || {}
    const nextConfig = { ...currentConfig }
    if (value === undefined || value === '') {
      delete nextConfig[paramName]
    } else {
      nextConfig[paramName] = value
    }
    updateNode(selectedNode.id, { config: nextConfig })
  }

  const handleJsonChange = (paramName: string, rawValue: string) => {
    setDraftValues((prev) => ({ ...prev, [paramName]: rawValue }))
    if (!selectedNode) return
    if (rawValue.trim() === '') {
      applyConfigChange(paramName, undefined)
      setErrors((prev) => {
        const next = { ...prev }
        delete next[paramName]
        return next
      })
      return
    }

    try {
      const parsed = JSON.parse(rawValue)
      applyConfigChange(paramName, parsed)
      setErrors((prev) => {
        const next = { ...prev }
        delete next[paramName]
        return next
      })
    } catch {
      setErrors((prev) => ({ ...prev, [paramName]: 'Invalid JSON structure' }))
    }
  }

  const renderParameterInput = (param: NonNullable<typeof definition>['parameters'][number]) => {
    if (!selectedNode) return null
    const configValue = selectedNode.data.config?.[param.name]

    switch (param.type) {
      case 'string':
        return (
          <Input
            value={typeof configValue === 'string' ? configValue : ''}
            onChange={(event) => applyConfigChange(param.name, event.target.value)}
            placeholder={param.description}
          />
        )
      case 'number':
        return (
          <Input
            type='number'
            value={typeof configValue === 'number' ? String(configValue) : ''}
            onChange={(event) => {
              if (event.target.value === '') {
                applyConfigChange(param.name, undefined)
                return
              }
              const numericValue = Number(event.target.value)
              if (!Number.isNaN(numericValue)) {
                applyConfigChange(param.name, numericValue)
              }
            }}
          />
        )
      case 'boolean':
        return (
          <div className='flex items-center gap-2'>
            <Switch
              checked={Boolean(configValue)}
              onCheckedChange={(checked) => applyConfigChange(param.name, checked)}
            />
            <span className='text-sm text-slate-600'>{checkedLabel(Boolean(configValue))}</span>
          </div>
        )
      case 'select':
        return (
          <Select
            value={typeof configValue === 'string' ? configValue : undefined}
            onValueChange={(value) => applyConfigChange(param.name, value)}
          >
            <SelectTrigger>
              <SelectValue placeholder='Select option' />
            </SelectTrigger>
            <SelectContent>
              {param.options?.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )
      case 'json':
      case 'array':
        return (
          <div className='space-y-2'>
            <Textarea
              value={draftValues[param.name] ?? ''}
              onChange={(event) => handleJsonChange(param.name, event.target.value)}
              rows={4}
              className='font-mono text-xs'
              placeholder={param.type === 'json' ? '{ "key": "value" }' : '["item-a", "item-b"]'}
            />
            {errors[param.name] && (
              <p className='text-xs text-destructive'>{errors[param.name]}</p>
            )}
          </div>
        )
      default:
        return (
          <Input
            value={typeof configValue === 'string' ? configValue : ''}
            onChange={(event) => applyConfigChange(param.name, event.target.value)}
          />
        )
    }
  }

  const handleDuplicate = () => {
    if (!selectedNode) return
    duplicateNode(selectedNode.id)
  }

  const handleDelete = () => {
    if (!selectedNode) return
    deleteNode(selectedNode.id)
    clearSelection()
  }

  if (!selectedNode) {
    return (
      <div className='editor-panel h-full w-full justify-center text-center'>
        <div className='mx-auto flex max-w-xs flex-col items-center justify-center gap-3 px-6 text-slate-500'>
          <div className='rounded-full bg-white/60 p-4 text-slate-500 shadow-inner'>
            <SlidersHorizontal className='h-5 w-5' />
          </div>
          <div>
            <p className='text-sm font-semibold text-slate-900'>Select a block to configure</p>
            <p className='text-xs text-slate-500'>
              Choose a block on the canvas to edit its parameters and metadata.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className='editor-panel h-full w-full'>
      <div className='editor-panel-header'>
        <div className='flex items-center gap-2 text-sm font-semibold text-slate-900'>
          <SlidersHorizontal className='h-4 w-4 text-slate-500' />
          Block Configuration
        </div>
        <p className='mt-1 text-xs text-slate-500'>
          {selectedNode.data.type} · ID {selectedNode.id}
        </p>
      </div>

      <ScrollArea className='editor-panel-body'>
        <div className='space-y-5 px-4 py-4'>
          <div className='space-y-2'>
            <Label htmlFor='block-name'>Display Name</Label>
            <Input
              id='block-name'
              value={selectedNode.data.name ?? ''}
              onChange={(event) => handleNameChange(event.target.value)}
            />
          </div>

          <div className='rounded-lg border border-slate-100 bg-slate-50/60 p-3 text-sm text-slate-600'>
            <div className='flex items-center gap-2'>
              {requiredTotal > 0 ? (
                <CheckCircle2 className='h-4 w-4 text-emerald-500' />
              ) : (
                <Info className='h-4 w-4 text-slate-400' />
              )}
              <span>
                {requiredTotal > 0
                  ? `${requiredComplete}/${requiredTotal} required parameters configured`
                  : 'No required parameters for this block'}
              </span>
            </div>
          </div>

          <div className='flex items-center gap-2'>
            <Button variant='outline' size='sm' className='flex-1 gap-2' onClick={handleDuplicate}>
              <Copy className='h-3.5 w-3.5' />
              Duplicate block
            </Button>
            <Button
              variant='outline'
              size='sm'
              className='flex-1 gap-2 text-destructive hover:text-destructive'
              onClick={handleDelete}
            >
              <Trash2 className='h-3.5 w-3.5' />
              Delete
            </Button>
          </div>

          <Separator />

          <div>
            <div className='mb-3'>
              <p className='text-sm font-semibold text-slate-900'>Parameters</p>
              <p className='text-xs text-slate-500'>
                {definition?.parameters.length
                  ? `${definition.parameters.length} configurable field${
                      definition.parameters.length > 1 ? 's' : ''
                    }`
                  : 'This block does not expose configurable parameters.'}
              </p>
            </div>

            {definition && definition.parameters.length > 0 ? (
              <div className='space-y-3'>
                {definition.parameters.map((param) => (
                  <div
                    key={param.name}
                    className='space-y-2 rounded-lg border border-slate-100 bg-slate-50/50 p-3'
                  >
                    <div className='flex items-start justify-between'>
                      <div>
                        <p className='text-sm font-medium text-slate-900'>{param.name}</p>
                        {param.description && (
                          <p className='text-xs text-slate-500'>{param.description}</p>
                        )}
                      </div>
                      <div className='flex items-center gap-2'>
                        {param.required && (
                          <Badge variant='outline' className='border-amber-200 bg-amber-50 text-[10px] text-amber-700'>
                            Required
                          </Badge>
                        )}
                        {isParameterValueSet(selectedNode.data.config?.[param.name]) && (
                          <Badge
                            variant='outline'
                            className='border-emerald-200 bg-emerald-50 text-[10px] text-emerald-700'
                          >
                            Configured
                          </Badge>
                        )}
                      </div>
                    </div>
                    {renderParameterInput(param)}
                  </div>
                ))}
              </div>
            ) : (
              <div className='rounded-lg border border-dashed border-slate-200 p-4 text-sm text-slate-500'>
                This block does not have configurable parameters.
              </div>
            )}
          </div>
        </div>
      </ScrollArea>
    </div>
  )
}

const checkedLabel = (value: boolean) => (value ? 'Enabled' : 'Disabled')
