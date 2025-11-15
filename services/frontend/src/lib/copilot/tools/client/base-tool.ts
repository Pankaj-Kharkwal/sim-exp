// @ts-nocheck
// Minimal base tool stub - TODO: Implement full copilot tool functionality

export enum ClientToolCallState {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  COMPLETED = 'completed',
  ERROR = 'error',
}

export interface BaseClientToolMetadata {
  name: string
  description: string
  parameters: Record<string, any>
}

export interface ClientToolDisplay {
  name: string
  description: string
  icon?: string
}

export class BaseClientTool {
  name: string
  description: string

  constructor(name: string, description: string) {
    this.name = name
    this.description = description
  }

  async execute(params: Record<string, any>): Promise<any> {
    throw new Error('Not implemented')
  }
}
