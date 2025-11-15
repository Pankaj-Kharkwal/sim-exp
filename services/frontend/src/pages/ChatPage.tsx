import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { sendChatMessage, type ChatResponsePayload } from '@/lib/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const quickPrompts = [
    {
      title: 'Daily summary',
      description: 'Recap today’s workflow progress in two sentences.',
      prompt: 'Summarize today’s workflow progress and highlight any blockers.',
    },
    {
      title: 'Brainstorm ideas',
      description: 'Ask the assistant to suggest workflow automations.',
      prompt: 'Suggest three creative workflow automations we could build in Sim.',
    },
    {
      title: 'Knowledge query',
      description: 'Draft a question for the knowledge base.',
      prompt: 'Generate an outline for a knowledge base article about Sim best practices.',
    },
  ]

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)
    setError(null)

    try {
      const response: ChatResponsePayload = await sendChatMessage({
        message: userMessage,
        conversation_id: conversationId || undefined,
      })

      setConversationId(response.conversation_id)
      setMessages(prev => [...prev, { role: 'assistant', content: response.message }])
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message'
      setError(errorMessage)
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${errorMessage}` }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handlePromptClick = (prompt: string) => {
    setInput(prompt)
  }

  return (
    <div className="chat-page">
      <div className="workspace-aurora workspace-aurora--chat" />
      <div className="chat-shell">
        <aside className="chat-sidebar glass-panel">
          <div className="chat-sidebar__header">
            <div>
              <p className="text-xs text-slate-500">Live assistant</p>
              <h1 className="text-lg font-semibold text-slate-900">Sim AI Chat</h1>
            </div>
            {conversationId && (
              <Badge variant="outline" className="border-purple-200 bg-purple-50 text-purple-600">
                Session · {conversationId.slice(0, 8)}
              </Badge>
            )}
          </div>

          <div className="chat-sidebar__section">
            <p className="text-xs text-slate-500 mb-2">Workspace context</p>
            <div className="space-y-2 text-xs text-slate-600">
              <p>Messages remain local to your browser.</p>
              <p>Connect knowledge bases to give the assistant more context.</p>
            </div>
          </div>

          <div className="chat-sidebar__section">
            <p className="text-xs text-slate-500 mb-2">Quick prompts</p>
            <div className="space-y-2">
              {quickPrompts.map((item) => (
                <button
                  key={item.title}
                  className="workspace-mini-card text-left"
                  onClick={() => handlePromptClick(item.prompt)}
                >
                  <p className="font-medium text-sm text-slate-900">{item.title}</p>
                  <p className="text-xs text-slate-500">{item.description}</p>
                </button>
              ))}
            </div>
          </div>
        </aside>

        <section className="chat-thread glass-panel">
          <div className="chat-thread__header">
            <div>
              <p className="text-xs text-slate-500 mb-1">Assistant</p>
              <h2 className="text-lg font-semibold text-slate-900">Conversation</h2>
            </div>
            <div className="flex gap-2">
              <Link to="/">
                <Button variant="outline" size='sm'>Dashboard</Button>
              </Link>
              {conversationId && (
                <Badge variant="secondary" className="h-8 px-3 flex items-center">
                  ID · {conversationId.slice(0, 8)}
                </Badge>
              )}
            </div>
          </div>

          <ScrollArea className="chat-messages">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center text-slate-500">
                <p className="text-lg font-semibold">Start a conversation</p>
                <p className="text-sm">Type a message below or pick a quick prompt.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={message.role === 'user' ? 'chat-message chat-message--user' : 'chat-message chat-message--assistant'}
                  >
                    <div className="chat-message__bubble">
                      <div className="text-xs font-semibold opacity-70 mb-1">
                        {message.role === 'user' ? 'You' : 'AI Assistant'}
                      </div>
                      <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="chat-message chat-message--assistant">
                    <div className="chat-message__bubble">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                        <div
                          className="w-2 h-2 bg-current rounded-full animate-bounce"
                          style={{ animationDelay: '0.2s' }}
                        />
                        <div
                          className="w-2 h-2 bg-current rounded-full animate-bounce"
                          style={{ animationDelay: '0.4s' }}
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </ScrollArea>

          <div className="chat-input">
            {error && (
              <div className="text-sm text-destructive bg-destructive/10 rounded px-3 py-2">
                {error}
              </div>
            )}
            <div className="chat-input__controls">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder='Type your message... (Press Enter to send, Shift+Enter for new line)'
                className="chat-textarea"
                disabled={isLoading}
              />
              <Button
                onClick={handleSendMessage}
                disabled={isLoading || !input.trim()}
                className="chat-send"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </Button>
            </div>
            <p className="text-xs text-slate-500">
              Backend API: {import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}
            </p>
          </div>

          <div className="chat-stats">
            <div className="chat-stat">
              <p className="text-xs text-slate-500">Total Messages</p>
              <p className="text-lg font-semibold text-slate-900">{messages.length}</p>
            </div>
            <div className="chat-stat">
              <p className="text-xs text-slate-500">Your Messages</p>
              <p className="text-lg font-semibold text-slate-900">
                {messages.filter((m) => m.role === 'user').length}
              </p>
            </div>
            <div className="chat-stat">
              <p className="text-xs text-slate-500">Active Conversations</p>
              <p className="text-lg font-semibold text-slate-900">
                {conversationId ? '1' : '0'}
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  )

}
