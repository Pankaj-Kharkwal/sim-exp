import { useState, useMemo } from 'react'
import { Loader2, Send } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Textarea } from '@/components/ui/textarea'
import { sendChatMessage } from '@/lib/api'
import { useChatStore } from '@/stores/panel/chat/store'

interface WorkflowChatProps {
  workflowId: string
}

const createMessageId = () =>
  typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : Math.random().toString(36).slice(2)

export function WorkflowChat({ workflowId }: WorkflowChatProps) {
  const messages = useChatStore((state) =>
    state.messages.filter((message) => message.workflowId === workflowId)
  )
  const addMessage = useChatStore((state) => state.addMessage)
  const clearChat = useChatStore((state) => state.clearChat)
  const setConversationId = useChatStore((state) => state.setConversationId)
  const conversationId = useChatStore(
    (state) => state.conversationIds[workflowId] ?? null
  )

  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sortedMessages = useMemo(
    () =>
      [...messages].sort(
        (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      ),
    [messages]
  )

  const handleSend = async () => {
    const trimmed = input.trim()
    if (!trimmed || isSending) return
    setInput('')
    setError(null)
    setIsSending(true)

    const userMessageId = createMessageId()
    addMessage({
      id: userMessageId,
      workflowId,
      type: 'user',
      content: trimmed,
    })

    try {
      const response = await sendChatMessage({
        message: trimmed,
        conversation_id: conversationId ?? undefined,
        workflow_id: workflowId,
      })

      setConversationId(workflowId, response.conversation_id)
      addMessage({
        id: createMessageId(),
        workflowId,
        type: 'workflow',
        content: response.message,
      })
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to send chat message'
      setError(message)
      addMessage({
        id: createMessageId(),
        workflowId,
        type: 'workflow',
        content: `Error: ${message}`,
      })
    } finally {
      setIsSending(false)
    }
  }

  return (
    <div className='flex h-full flex-col'>
      <div className='flex items-center justify-between border-b px-4 py-3'>
        <div>
          <p className='text-sm font-semibold text-slate-900'>Workflow Chat</p>
          <p className='text-xs text-slate-500'>
            Conversations are scoped to this workflow. Running workflows is optional.
          </p>
        </div>
        <Button variant='ghost' size='sm' onClick={() => clearChat(workflowId)}>
          Clear
        </Button>
      </div>

      <ScrollArea className='flex-1 px-4 py-3'>
        {sortedMessages.length === 0 ? (
          <div className='flex h-full flex-col items-center justify-center gap-2 text-center text-sm text-muted-foreground'>
            <p className='font-medium text-slate-900'>Start the conversation</p>
            <p className='text-sm text-slate-500'>
              Ask questions about this workflow or request status updates.
            </p>
          </div>
        ) : (
          <div className='space-y-3'>
            {sortedMessages.map((message) => {
              const isUser = message.type === 'user'
              return (
                <div
                  key={message.id}
                  className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                      isUser
                        ? 'bg-indigo-600 text-white shadow'
                        : 'bg-slate-100 text-slate-900'
                    }`}
                  >
                    <p className='text-[11px] font-semibold uppercase opacity-70'>
                      {isUser ? 'You' : 'Workflow'}
                    </p>
                    <div className='mt-1 whitespace-pre-wrap text-sm'>{message.content}</div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </ScrollArea>

      <div className='border-t p-4'>
        {error && (
          <div className='mb-2 rounded border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-700'>
            {error}
          </div>
        )}
        <div className='flex gap-2'>
          <Textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder='Ask a question about this workflow…'
            className='min-h-[60px] resize-none'
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault()
                handleSend()
              }
            }}
          />
          <Button onClick={handleSend} disabled={!input.trim() || isSending} className='h-[60px] px-4'>
            {isSending ? <Loader2 className='h-4 w-4 animate-spin' /> : <Send className='h-4 w-4' />}
          </Button>
        </div>
      </div>
    </div>
  )
}
