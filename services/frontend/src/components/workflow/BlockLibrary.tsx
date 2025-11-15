import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Search, ChevronDown, ChevronRight, Loader2, AlertCircle } from 'lucide-react'
import {
  blockCategories,
  type BlockDefinition,
} from '@/lib/blocks/blockDefinitions'
import { useBlocks } from '@/hooks/useBlocks'

interface BlockLibraryProps {
  onAddBlock: (blockDef: BlockDefinition) => void
}

export function BlockLibrary({ onAddBlock }: BlockLibraryProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(
    new Set(Object.keys(blockCategories))
  )

  // Fetch blocks from backend API
  const { blocks: blockDefinitions, isLoading, error } = useBlocks()

  const toggleCategory = (category: string) => {
    setExpandedCategories((prev) => {
      const next = new Set(prev)
      if (next.has(category)) {
        next.delete(category)
      } else {
        next.add(category)
      }
      return next
    })
  }

  // Search blocks
  const searchBlocks = (query: string) => {
    const lowerQuery = query.toLowerCase()
    return blockDefinitions.filter(
      (block) =>
        block.name.toLowerCase().includes(lowerQuery) ||
        block.description.toLowerCase().includes(lowerQuery) ||
        block.type.toLowerCase().includes(lowerQuery)
    )
  }

  // Get blocks by category
  const getBlocksByCategory = (category: string) => {
    return blockDefinitions.filter((block) => block.category === category)
  }

  const filteredBlocks = searchQuery
    ? searchBlocks(searchQuery)
    : blockDefinitions

  const blocksByCategory = searchQuery
    ? { all: filteredBlocks }
    : Object.fromEntries(
        Object.keys(blockCategories).map((cat) => [
          cat,
          getBlocksByCategory(cat),
        ])
      )

  const getColorClass = (color: string) => {
    const colorMap: Record<string, string> = {
      purple: 'bg-purple-100 text-purple-700 hover:bg-purple-200',
      blue: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
      green: 'bg-green-100 text-green-700 hover:bg-green-200',
      orange: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
      pink: 'bg-pink-100 text-pink-700 hover:bg-pink-200',
      gray: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
      amber: 'bg-amber-100 text-amber-700 hover:bg-amber-200',
      cyan: 'bg-cyan-100 text-cyan-700 hover:bg-cyan-200',
      indigo: 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200',
      sky: 'bg-sky-100 text-sky-700 hover:bg-sky-200',
      violet: 'bg-violet-100 text-violet-700 hover:bg-violet-200',
      teal: 'bg-teal-100 text-teal-700 hover:bg-teal-200',
      yellow: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200',
      red: 'bg-red-100 text-red-700 hover:bg-red-200',
      slate: 'bg-slate-100 text-slate-700 hover:bg-slate-200',
    }
    return colorMap[color] || colorMap.gray
  }

  return (
    <div className="editor-panel w-full">
      <div className="editor-panel-header">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-sm">Block Library</h2>
          <div className="text-xs text-slate-500">
            {blockDefinitions.length} blueprint{blockDefinitions.length === 1 ? '' : 's'}
          </div>
        </div>
        <div className="relative mt-3">
          <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-slate-400" />
          <Input
            placeholder="Search blocks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 text-sm"
            disabled={isLoading}
          />
        </div>
      </div>

      <div className="editor-panel-body space-y-3 p-2">
        {/* Loading State */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400 mb-3" />
            <p className="text-sm text-gray-500">Loading blocks...</p>
          </div>
        )}

        {/* Error State */}
        {error && !isLoading && (
          <div className="flex flex-col items-center justify-center py-12 px-4">
            <AlertCircle className="h-8 w-8 text-red-500 mb-3" />
            <p className="text-sm text-red-600 text-center mb-2">Failed to load blocks</p>
            <p className="text-xs text-gray-500 text-center">{error}</p>
          </div>
        )}

        {/* Blocks Content */}
        {!isLoading && !error && (
          searchQuery ? (
          // Search Results
          <div className="space-y-1">
            {filteredBlocks.length === 0 ? (
              <div className="px-3 py-6 text-center text-gray-500 text-sm">
                No blocks found
              </div>
            ) : (
              filteredBlocks.map((block) => (
                <BlockItem
                  key={block.type}
                  block={block}
                  onAdd={onAddBlock}
                  colorClass={getColorClass(block.color)}
                />
              ))
            )}
          </div>
        ) : (
          // Category View
          <div className="space-y-2">
            {Object.entries(blockCategories).map(([categoryKey, category]) => {
              const blocks = blocksByCategory[categoryKey] || []
              const isExpanded = expandedCategories.has(categoryKey)
              const CategoryIcon = category.icon

              return (
                <div key={categoryKey} className="rounded-lg bg-white">
                  {/* Category Header */}
                  <button
                    onClick={() => toggleCategory(categoryKey)}
                    className="flex w-full items-center gap-2 px-3 py-2 text-left transition hover:bg-gray-50"
                  >
                    {isExpanded ? (
                      <ChevronDown className="h-4 w-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="h-4 w-4 text-gray-500" />
                    )}
                    <CategoryIcon className="h-4 w-4 text-gray-600" />
                    <span className="flex-1 font-medium text-gray-900 text-sm">
                      {category.label}
                    </span>
                    <span className="text-gray-500 text-xs">
                      {blocks.length}
                    </span>
                  </button>

                  {/* Category Blocks */}
                  {isExpanded && (
                    <div className="border-t px-2 py-1">
                      {blocks.map((block) => (
                        <BlockItem
                          key={block.type}
                          block={block}
                          onAdd={onAddBlock}
                          colorClass={getColorClass(block.color)}
                        />
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
          )
        )}
      </div>

      {!isLoading && !error && (
        <div className="editor-panel-footer">
          <div className="text-xs text-slate-500">
            {filteredBlocks.length} block{filteredBlocks.length !== 1 ? 's' : ''} available
          </div>
        </div>
      )}
    </div>
  )
}

interface BlockItemProps {
  block: BlockDefinition
  onAdd: (block: BlockDefinition) => void
  colorClass: string
}

function BlockItem({ block, onAdd, colorClass }: BlockItemProps) {
  const BlockIcon = block.icon

  return (
    <button
      onClick={() => onAdd(block)}
      className="flex w-full items-start gap-2 rounded-md px-2 py-2 text-left transition hover:bg-gray-50"
      title={block.description}
    >
      <div className={`rounded p-1 ${colorClass}`}>
        <BlockIcon className="h-3 w-3" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="font-medium text-gray-900 text-xs">{block.name}</div>
        <div className="truncate text-gray-500 text-xs">
          {block.description}
        </div>
      </div>
    </button>
  )
}
