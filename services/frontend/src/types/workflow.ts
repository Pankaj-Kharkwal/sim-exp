// Shared workflow types
export interface BlockData {
  id: string
  type: string
  name: string
  config?: Record<string, any>
  [key: string]: any
}
