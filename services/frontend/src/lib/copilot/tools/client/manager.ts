// Tool manager stub - TODO: Implement full tool management

import { BaseClientTool } from './base-tool'

const tools = new Map<string, BaseClientTool>()

export function registerClientTool(tool: BaseClientTool): void {
  tools.set(tool.name, tool)
}

export function getClientTool(name: string): BaseClientTool | undefined {
  return tools.get(name)
}

export function registerToolStateSync(callback: (state: any) => void): void {
  // TODO: Implement tool state synchronization
  console.warn('registerToolStateSync not yet implemented')
}
