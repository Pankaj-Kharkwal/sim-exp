// Minimal copilot API stub - TODO: Implement full copilot functionality

export interface CopilotChat {
  id: string
  workflowId: string
  messages: CopilotMessage[]
  createdAt: string
  updatedAt: string
}

export interface CopilotMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

export async function sendStreamingMessage(
  chatId: string,
  message: string,
  onChunk?: (chunk: string) => void
): Promise<void> {
  // TODO: Implement streaming message functionality
  console.warn('sendStreamingMessage not yet implemented')
  throw new Error('Copilot API not yet implemented')
}

export async function createChat(workflowId: string): Promise<CopilotChat> {
  // TODO: Implement chat creation
  console.warn('createChat not yet implemented')
  throw new Error('Copilot API not yet implemented')
}

export async function getChats(workflowId: string): Promise<CopilotChat[]> {
  // TODO: Implement get chats
  console.warn('getChats not yet implemented')
  return []
}
