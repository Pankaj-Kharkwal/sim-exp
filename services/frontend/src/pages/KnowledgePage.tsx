import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Plus, Search, FileText, Upload, Trash2, Edit, Loader2, AlertCircle, BookOpen, Database } from 'lucide-react'
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
    <div className="flex-1 overflow-auto relative">
      {/* Enhanced header with glassmorphic design */}
      <header className="page-header sticky top-0 z-10 glass-background-strong backdrop-blur-lg border-b border-subtle">
        <div className="flex items-center justify-between animate-slideIn">
          <div>
            <h1 className="page-title text-gradient">Knowledge Base</h1>
            <p className="page-subtitle">
              📚 Manage your document collections for AI workflows
            </p>
          </div>
          <button
            onClick={() => setShowCreateDialog(true)}
            className="btn btn-primary btn-ripple shadow-xl hover:shadow-2xl hover:scale-105 transition-all"
            disabled={isLoading}
          >
            <Plus className="mr-2 h-4 w-4" />
            New Knowledge Base
          </button>
        </div>
      </header>

      <div className="p-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 glass-card-enhanced border-2 border-red-500/30 bg-red-500/10 p-4 rounded-xl animate-slideIn">
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
              <span className="text-sm font-medium text-red-600 dark:text-red-400 flex-1">{error}</span>
              <button
                onClick={clearError}
                className="glass-button h-8 w-8 rounded-lg p-0 hover:bg-red-500/10 transition-all"
              >
                <svg className="h-4 w-4 mx-auto text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Enhanced Search */}
        <div className="mb-8 relative animate-slideIn">
          <Search className="-translate-y-1/2 absolute top-1/2 left-4 h-5 w-5 text-tertiary transition-colors" />
          <input
            placeholder="Search knowledge bases by name or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input pl-12 h-14 text-base shadow-lg focus:shadow-xl transition-all"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-4 top-1/2 -translate-y-1/2 glass-button h-8 w-8 rounded-lg p-0 hover:bg-red-500/10"
            >
              <svg className="h-4 w-4 mx-auto text-tertiary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Loading State */}
        {isLoading && knowledgeBases.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 animate-fadeIn">
            <div className="w-16 h-16 rounded-2xl gradient-animated flex items-center justify-center mb-4 shadow-xl">
              <Loader2 className="h-8 w-8 text-white animate-spin" />
            </div>
            <p className="text-body">Loading knowledge bases...</p>
          </div>
        ) : filteredKBs.length === 0 ? (
          /* Enhanced Empty State */
          <div className="empty-state animate-fadeIn">
            <div className="glass-card-enhanced p-12 max-w-md mx-auto">
              <div className="w-20 h-20 mx-auto mb-6 rounded-2xl gradient-animated flex items-center justify-center shadow-xl">
                <BookOpen className="h-10 w-10 text-white" />
              </div>
              <h3 className="text-heading-3 text-center mb-3">
                {searchQuery ? 'No knowledge bases found' : 'No knowledge bases yet'}
              </h3>
              <p className="text-body text-center mb-6">
                {searchQuery
                  ? 'Try adjusting your search terms or create a new knowledge base'
                  : 'Create your first knowledge base to store and organize documents for AI workflows'}
              </p>
              {!searchQuery && (
                <button
                  onClick={() => setShowCreateDialog(true)}
                  className="btn btn-primary btn-ripple w-full h-12 shadow-xl hover:shadow-2xl"
                >
                  <Plus className="mr-2 h-5 w-5" />
                  Create Your First Knowledge Base
                </button>
              )}
              {searchQuery && (
                <button
                  className="btn btn-secondary w-full h-12"
                  onClick={() => setSearchQuery('')}
                >
                  Clear Search
                </button>
              )}
            </div>
          </div>
        ) : (
          /* Enhanced Knowledge Bases Grid */
          <div className="grid-cards">
            {filteredKBs.map((kb, index) => (
              <div
                key={kb.id}
                className={`glass-card-enhanced hover-lift p-6 cursor-pointer group animate-slideUp`}
                style={{ animationDelay: `${index * 50}ms` }}
                onClick={() => navigate(`/knowledge/${kb.id}`)}
              >
                {/* Header with icon and actions */}
                <div className="mb-5 flex items-start justify-between">
                  <div className="inline-flex rounded-xl gradient-animated p-3 shadow-lg group-hover:shadow-xl transition-shadow">
                    <Database className="h-6 w-6 text-white" />
                  </div>
                  <button
                    onClick={(e) => handleDeleteKB(kb.id, kb.name, e)}
                    className="glass-button h-9 w-9 p-0 rounded-lg hover:bg-red-500/20 hover:border-red-500/50 opacity-0 group-hover:opacity-100 transition-all"
                    disabled={isLoading}
                    title="Delete knowledge base"
                  >
                    <Trash2 className="h-4 w-4 mx-auto text-red-600" />
                  </button>
                </div>

                {/* Content */}
                <h3 className="text-heading-3 line-clamp-1 mb-2 group-hover:text-gradient transition-all">
                  {kb.name}
                </h3>
                <p className="text-body line-clamp-2 mb-5 min-h-[3em]">
                  {kb.description || 'No description provided'}
                </p>

                {/* Stats */}
                <div className="glass-card p-3 rounded-lg mb-4">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-primary" />
                      <span className="font-medium">{kb.document_count || 0}</span>
                      <span className="text-tertiary">documents</span>
                    </div>
                    <span className="text-xs text-tertiary">
                      {formatDistanceToNow(new Date(kb.updated_at), { addSuffix: true })}
                    </span>
                  </div>
                </div>

                {/* Footer with metadata */}
                <div className="pt-4 border-t border-subtle grid grid-cols-2 gap-3 text-xs">
                  <div className="flex flex-col">
                    <span className="text-tertiary mb-1">Embedding Model</span>
                    <span className="font-mono text-primary truncate">{kb.embedding_model}</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-tertiary mb-1">Chunk Size</span>
                    <span className="font-mono text-primary">{kb.chunk_size}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Enhanced Create Knowledge Base Dialog */}
      {showCreateDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fadeIn">
          <div className="glass-modal w-full max-w-md p-8 m-4 animate-scaleIn">
            <h2 className="text-heading-2 mb-6 text-gradient">Create Knowledge Base</h2>
            <div className="space-y-5">
              <div className="animate-slideIn">
                <label className="block text-sm font-medium text-secondary mb-2">Name *</label>
                <input
                  value={newKBName}
                  onChange={(e) => setNewKBName(e.target.value)}
                  placeholder="e.g., Product Documentation"
                  className="input"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && newKBName.trim()) {
                      handleCreateKB()
                    }
                  }}
                />
              </div>
              <div className="animate-slideIn delay-100">
                <label className="block text-sm font-medium text-secondary mb-2">Description (optional)</label>
                <input
                  value={newKBDescription}
                  onChange={(e) => setNewKBDescription(e.target.value)}
                  placeholder="Describe what this knowledge base contains"
                  className="input"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && newKBName.trim()) {
                      handleCreateKB()
                    }
                  }}
                />
              </div>
              <div className="flex gap-3 pt-4 animate-slideIn delay-200">
                <button
                  onClick={() => {
                    setShowCreateDialog(false)
                    setNewKBName('')
                    setNewKBDescription('')
                  }}
                  className="btn btn-secondary flex-1 h-12"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateKB}
                  className="btn btn-primary btn-ripple flex-1 h-12 shadow-xl hover:shadow-2xl"
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
