// Naming utility stub
const adjectives = ['Quick', 'Smart', 'Clever', 'Dynamic', 'Efficient', 'Powerful']
const nouns = ['Workflow', 'Process', 'Pipeline', 'Automation', 'Task', 'Flow']

export function generateCreativeWorkflowName(): string {
  const adj = adjectives[Math.floor(Math.random() * adjectives.length)]
  const noun = nouns[Math.floor(Math.random() * nouns.length)]
  return `${adj} ${noun}`
}
