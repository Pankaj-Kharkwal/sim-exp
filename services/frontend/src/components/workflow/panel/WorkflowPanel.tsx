import { PanelRightClose, PanelRightOpen } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { ExecutionConsole } from '@/components/workflow/panel/ExecutionConsole'
import { WorkflowChat } from '@/components/workflow/panel/WorkflowChat'
import { WorkflowCopilotPanel } from '@/components/workflow/panel/WorkflowCopilotPanel'
import { usePanelStore } from '@/stores/panel/store'

interface WorkflowPanelProps {
  workflowId?: string | null
}

const TABS: Array<{ id: 'console' | 'chat' | 'copilot' | 'variables'; label: string }> = [
  { id: 'console', label: 'Run Logs' },
  { id: 'chat', label: 'Chat' },
  { id: 'copilot', label: 'Copilot' },
  { id: 'variables', label: 'Variables' },
]

export function WorkflowPanel({ workflowId }: WorkflowPanelProps) {
  const { isOpen, panelWidth, activeTab, setActiveTab, togglePanel } = usePanelStore()

  if (!isOpen) {
    return null
  }

  return (
    <div
      className='editor-panel flex h-full flex-col'
      style={{ width: panelWidth }}
    >
      <div className='editor-panel-header flex items-center justify-between'>
        <div className='flex flex-wrap gap-2'>
          {TABS.map((tab) => (
            <Button
              key={tab.id}
              size='sm'
              variant={activeTab === tab.id ? 'secondary' : 'ghost'}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </Button>
          ))}
        </div>
        <Button size='icon' variant='ghost' onClick={togglePanel}>
          {isOpen ? <PanelRightClose className='h-4 w-4' /> : <PanelRightOpen className='h-4 w-4' />}
        </Button>
      </div>

      <div className='editor-panel-body overflow-hidden'>
        {!workflowId && (
          <div className='flex h-full flex-col items-center justify-center px-6 text-center text-sm text-muted-foreground'>
            Select a workflow to use the run panel.
          </div>
        )}

        {workflowId && activeTab === 'console' && <ExecutionConsole workflowId={workflowId} />}
        {workflowId && activeTab === 'chat' && <WorkflowChat workflowId={workflowId} />}
        {workflowId && activeTab === 'copilot' && <WorkflowCopilotPanel workflowId={workflowId} />}
        {workflowId && activeTab === 'variables' && (
          <div className='flex h-full flex-col items-center justify-center gap-2 px-6 text-center text-sm text-muted-foreground'>
            <p className='font-medium text-slate-900'>Variables coming soon</p>
            <p className='text-sm text-slate-500'>
              View and edit workflow variables from this panel in an upcoming update.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
