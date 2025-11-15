// Block outputs utility stub
export function getBlockOutputs(blockType: string): string[] {
  if (!blockType) return ['result']
  return ['result']
}

export function getBlockOutputPaths(blockType: string): string[] {
  return getBlockOutputs(blockType).map((key) => `${blockType}.${key}`)
}

export function getBlockOutputType(_blockType: string, _path: string): string {
  return 'string'
}
