import { useEffect, useMemo, useState } from 'react'
import { Loader2, Bot, Send } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Textarea } from '@/components/ui/textarea'
import { useCopilotStore } from '@/stores/copilot/store'

interface WorkflowCopilotPanelProps {
  workflowId: string
}

export function WorkflowCopilotPanel({ workflowId }: WorkflowCopilotPanelProps) {
  const messages = useCopilotStore((state) => state.messages)
  const isSendingMessage = useCopilotStore((state) => state.isSendingMessage)
  const copilotError = useCopilotStore((state) => state.error)
  const sendMessage = useCopilotStore((state) => state.sendMessage)
  const setWorkflowId = useCopilotStore((state) => state.setWorkflowId)
  const loadChats = useCopilotStore((state) => state.loadChats)
  const createNewChat = useCopilotStore((state) => state.createNewChat)
  const clearError = useCopilotStore((state) => state.clearError)

  const [input, setInput] = useState('')
  const [localError, setLocalError] = useState<string | null>(null)

  useEffect(() => {
    if (!workflowId) return
    let cancelled = false

    const syncChats = async () => {
      try {
        await setWorkflowId(workflowId)
        await loadChats()
        const { currentChat } = useCopilotStore.getState()
        if (!currentChat) {
          await createNewChat()
        }
      } catch (error) {
        if (!cancelled) {
          setLocalError(error instanceof Error ? error.message : 'Failed to initialize Copilot')
        }
      }
    }

    void syncChats()
    return () => {
      cancelled = true
    }
  }, [workflowId, setWorkflowId, loadChats, createNewChat])

  const renderMessages = useMemo(() => {
    if (messages.length === 0) {
      return (
        <div className='flex h-full flex-col items-center justify-center gap-2 text-center text-sm text-muted-foreground'>
          <Bot className='h-8 w-8 text-slate-400' />
          <p className='font-medium text-slate-900'>Ask Copilot for help</p>
          <p className='text-sm text-slate-500'>
            Copilot can reason about this workflow, explore logs, and suggest fixes.
          </p>
        </div>
      )
    }

    return (
      <div className='space-y-3'>
        {messages.map((message) => (
          <div key={message.id} className='rounded-lg border border-slate-100 bg-slate-50 p-3 text-sm'>
            <div className='flex items-center justify-between'>
              <p className='text-[11px] font-semibold uppercase text-slate-500'>{message.role}</p>
              <span className='font-mono text-[10px] text-slate-400'>
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
            <div className='mt-2 whitespace-pre-wrap text-slate-800'>{message.content}</div>
          </div>
        ))}
      </div>
    )
  }, [messages])

  const handleSend = async () => {
    const trimmed = input.trim()
    if (!trimmed || isSendingMessage) return
    setInput('')
    setLocalError(null)
    clearError()

    try {
      await sendMessage(trimmed, {
        stream: true,
        contexts: [
          {
            kind: 'current_workflow',
            workflowId,
            label: 'Active Workflow',
          },
        ],
      })
    } catch (error) {
      setLocalError(error instanceof Error ? error.message : 'Failed to send message')
    }
  }

  return (
    <div className='flex h-full flex-col'>
      <div className='border-b px-4 py-3'>
        <p className='text-sm font-semibold text-slate-900'>Copilot</p>
        <p className='text-xs text-slate-500'>
          Ask natural language questions. Copilot can reason about workflow state and logs.
        </p>
      </div>

      <ScrollArea className='flex-1 px-4 py-3'>{renderMessages}</ScrollArea>

      <div className='border-t p-4'>
        {(copilotError || localError) && (
          <div className='mb-2 rounded border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-700'>
            {copilotError || localError}
          </div>
        )}
        <div className='flex gap-2'>
          <Textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder='Ask Copilot…'
            className='min-h-[60px] resize-none'
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault()
                handleSend()
              }
            }}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isSendingMessage}
            className='h-[60px] px-4'
          >
            {isSendingMessage ? <Loader2 className='h-4 w-4 animate-spin' /> : <Send className='h-4 w-4' />}
          </Button>
        </div>
      </div>
    </div>
  )
}
