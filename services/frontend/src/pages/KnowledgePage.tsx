import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Search, FileText, Trash2, Loader2, AlertCircle, BookOpen, Database, X } from 'lucide-react'
import { useKnowledgeStore } from '@/stores/knowledgeStore'
import { formatDistanceToNow } from 'date-fns'

export default function KnowledgePage() {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [newKBName, setNewKBName] = useState('')
  const [newKBDescription, setNewKBDescription] = useState('')

  const {
    knowledgeBases,
    isLoading,
    error,
    fetchKnowledgeBases,
    createKnowledgeBase,
    deleteKnowledgeBase,
    clearError,
  } = useKnowledgeStore()

  useEffect(() => {
    fetchKnowledgeBases()
  }, [fetchKnowledgeBases])

  const handleCreateKB = async () => {
    if (!newKBName.trim()) return

    try {
      const kb = await createKnowledgeBase({
        name: newKBName,
        description: newKBDescription || undefined,
      })
      setShowCreateDialog(false)
      setNewKBName('')
      setNewKBDescription('')
      navigate(`/knowledge/${kb.id}`)
    } catch (error) {
      console.error('Failed to create knowledge base:', error)
    }
  }

  const handleDeleteKB = async (id: string, name: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm(`Are you sure you want to delete "${name}"? This will delete all documents in this knowledge base.`)) {
      return
    }

    try {
      await deleteKnowledgeBase(id)
    } catch (error) {
      console.error('Failed to delete knowledge base:', error)
    }
  }

  const filteredKBs = knowledgeBases.filter(
    (kb) =>
      kb.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      kb.description?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const formatSize = (bytes?: number) => {
    if (!bytes) return '0 B'
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-6 fade-in">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-bold text-3xl text-white">Knowledge Base</h1>
              <p className="mt-2 text-white/70">
                Manage your document collections for AI workflows
              </p>
            </div>
            <button
              onClick={() => setShowCreateDialog(true)}
              className="glass-button px-4 py-2"
              disabled={isLoading}
            >
              <Plus className="mr-2 h-4 w-4" />
              New Knowledge Base
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="glass-card mb-6 border-2 border-red-500/30 bg-red-500/10 p-4 fade-in">
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-red-300 flex-shrink-0" />
              <span className="text-sm font-medium text-red-200 flex-1">{error}</span>
              <button
                onClick={clearError}
                className="glass-button p-2"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Search */}
        <div className="relative mb-8 fade-in" style={{ animationDelay: '0.1s' }}>
          <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-white/40" />
          <input
            placeholder="Search knowledge bases by name or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="glass-input w-full pl-10"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="glass-button -translate-y-1/2 absolute top-1/2 right-3 p-2"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>

        {/* Loading State */}
        {isLoading && knowledgeBases.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16">
            <Loader2 className="mb-4 h-8 w-8 animate-spin text-white/40" />
            <p className="text-white/70">Loading knowledge bases...</p>
          </div>
        ) : filteredKBs.length === 0 ? (
          /* Empty State */
          <div className="glass-card mx-auto max-w-md p-12 text-center fade-in" style={{ animationDelay: '0.2s' }}>
            <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-r from-purple-500/30 to-blue-500/30">
              <BookOpen className="h-10 w-10 text-white" />
            </div>
            <h3 className="mb-3 font-semibold text-xl text-white">
              {searchQuery ? 'No knowledge bases found' : 'No knowledge bases yet'}
            </h3>
            <p className="mb-6 text-white/70">
              {searchQuery
                ? 'Try adjusting your search terms or create a new knowledge base'
                : 'Create your first knowledge base to store and organize documents for AI workflows'}
            </p>
            {!searchQuery ? (
              <button
                onClick={() => setShowCreateDialog(true)}
                className="glass-button w-full bg-gradient-to-r from-purple-500/30 to-blue-500/30 py-3 font-semibold"
              >
                <Plus className="mr-2 h-5 w-5" />
                Create Your First Knowledge Base
              </button>
            ) : (
              <button
                className="glass-button w-full py-3"
                onClick={() => setSearchQuery('')}
              >
                Clear Search
              </button>
            )}
          </div>
        ) : (
          /* Knowledge Bases Grid */
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filteredKBs.map((kb, index) => (
              <div
                key={kb.id}
                className="glass-card group cursor-pointer p-6 fade-in"
                style={{ animationDelay: `${0.2 + index * 0.05}s` }}
                onClick={() => navigate(`/knowledge/${kb.id}`)}
              >
                {/* Header with icon and actions */}
                <div className="mb-5 flex items-start justify-between">
                  <div className="inline-flex rounded-xl bg-gradient-to-r from-purple-500/30 to-blue-500/30 p-3">
                    <Database className="h-6 w-6 text-white" />
                  </div>
                  <button
                    onClick={(e) => handleDeleteKB(kb.id, kb.name, e)}
                    className="glass-button p-2 opacity-0 transition-all hover:bg-red-500/20 group-hover:opacity-100"
                    disabled={isLoading}
                    title="Delete knowledge base"
                  >
                    <Trash2 className="h-4 w-4 text-red-300" />
                  </button>
                </div>

                {/* Content */}
                <h3 className="mb-2 line-clamp-1 font-semibold text-white">
                  {kb.name}
                </h3>
                <p className="mb-5 line-clamp-2 min-h-[3em] text-sm text-white/70">
                  {kb.description || 'No description provided'}
                </p>

                {/* Stats */}
                <div className="mb-4 rounded-lg bg-white/10 p-3">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-purple-300" />
                      <span className="font-medium text-white">{kb.document_count || 0}</span>
                      <span className="text-white/60">documents</span>
                    </div>
                    <span className="text-xs text-white/50">
                      {formatDistanceToNow(new Date(kb.updated_at), { addSuffix: true })}
                    </span>
                  </div>
                </div>

                {/* Footer with metadata */}
                <div className="grid grid-cols-2 gap-3 border-t border-white/10 pt-4 text-xs">
                  <div className="flex flex-col">
                    <span className="mb-1 text-white/60">Embedding Model</span>
                    <span className="truncate font-mono text-white/80">{kb.embedding_model}</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="mb-1 text-white/60">Chunk Size</span>
                    <span className="font-mono text-white/80">{kb.chunk_size}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Knowledge Base Dialog */}
      {showCreateDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm fade-in">
          <div className="glass-card m-4 w-full max-w-md p-8">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="font-bold text-xl text-white">Create Knowledge Base</h2>
              <button
                onClick={() => {
                  setShowCreateDialog(false)
                  setNewKBName('')
                  setNewKBDescription('')
                }}
                className="glass-button p-2"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="space-y-5">
              <div>
                <label className="mb-2 block text-sm font-medium text-white/80">Name *</label>
                <input
                  value={newKBName}
                  onChange={(e) => setNewKBName(e.target.value)}
                  placeholder="e.g., Product Documentation"
                  className="glass-input w-full"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && newKBName.trim()) {
                      handleCreateKB()
                    }
                  }}
                />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-white/80">
                  Description (optional)
                </label>
                <input
                  value={newKBDescription}
                  onChange={(e) => setNewKBDescription(e.target.value)}
                  placeholder="Describe what this knowledge base contains"
                  className="glass-input w-full"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && newKBName.trim()) {
                      handleCreateKB()
                    }
                  }}
                />
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => {
                    setShowCreateDialog(false)
                    setNewKBName('')
                    setNewKBDescription('')
                  }}
                  className="glass-button flex-1 py-3"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateKB}
                  className="glass-button flex-1 bg-gradient-to-r from-purple-500/30 to-blue-500/30 py-3 font-semibold"
                  disabled={isLoading || !newKBName.trim()}
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center gap-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Creating...</span>
                    </div>
                  ) : (
                    <>
                      <Plus className="mr-2 h-4 w-4" />
                      Create
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
