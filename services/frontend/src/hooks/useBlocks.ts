import { useEffect, useState } from 'react'
import type { BlockDefinition } from '@/lib/blocks/blockDefinitions'
import {
  Code,
  Zap,
  GitBranch,
  Repeat,
  Settings,
  MessageSquare,
  Globe,
  Clock,
  Send,
  type LucideIcon,
} from 'lucide-react'

// Map backend block types to frontend icons
const iconMap: Record<string, LucideIcon> = {
  agent: MessageSquare,
  api: Globe,
  function: Code,
  condition: GitBranch,
  router: GitBranch,
  loop: Repeat,
  parallel: Zap,
  variables: Settings,
  wait: Clock,
  response: Send,
  default: Code,
}

// Map backend categories to frontend categories
const categoryMap: Record<string, BlockDefinition['category']> = {
  processing: 'ai',
  logic: 'logic',
  control_flow: 'automation',
  output: 'integration',
}

// Map backend block types to colors
const colorMap: Record<string, string> = {
  agent: 'purple',
  api: 'blue',
  function: 'violet',
  condition: 'green',
  router: 'cyan',
  loop: 'orange',
  parallel: 'pink',
  variables: 'indigo',
  wait: 'amber',
  response: 'teal',
}

interface BackendBlock {
  type: string
  name: string
  category: string
  description: string
  config_schema: Record<string, any>
}

interface BackendBlocksResponse {
  blocks: BackendBlock[]
  total: number
}

export function useBlocks() {
  const [blocks, setBlocks] = useState<BlockDefinition[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchBlocks() {
      try {
        setIsLoading(true)
        setError(null)

        const response = await fetch('http://localhost:8000/api/v1/blocks/')
        if (!response.ok) {
          throw new Error(`Failed to fetch blocks: ${response.statusText}`)
        }

        const data: BackendBlocksResponse = await response.json()

        if (!mounted) return

        // Transform backend blocks to frontend BlockDefinition format
        const transformedBlocks: BlockDefinition[] = data.blocks.map((block) => {
          // Extract parameters from config_schema
          const parameters = Object.entries(block.config_schema || {}).map(
            ([name, schema]: [string, any]) => ({
              name,
              type: schema.type || 'string',
              required: schema.required || false,
              default: schema.default,
              description: schema.description,
              options: schema.enum
                ? schema.enum.map((val: string) => ({ label: val, value: val }))
                : undefined,
            })
          )

          return {
            type: block.type,
            name: block.name,
            description: block.description,
            category: categoryMap[block.category] || 'logic',
            icon: iconMap[block.type] || iconMap.default,
            color: colorMap[block.type] || 'gray',
            parameters,
            outputs: ['result'], // Backend doesn't provide outputs yet, use default
          }
        })

        setBlocks(transformedBlocks)
      } catch (err) {
        console.error('Error fetching blocks:', err)
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to fetch blocks')
        }
      } finally {
        if (mounted) {
          setIsLoading(false)
        }
      }
    }

    fetchBlocks()

    return () => {
      mounted = false
    }
  }, [])

  return { blocks, isLoading, error }
}
