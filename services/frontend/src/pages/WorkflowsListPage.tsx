import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useWorkflowStore } from '@/stores/workflowStore'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Plus, Search, Workflow as WorkflowIcon, Clock, Play, Loader2, Trash2 } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { ActionButton } from '@/components/layout/ActionButtons'
import { Card, FeatureCard } from '@/components/layout/Cards'
import { ContentSection, Grid } from '@/components/layout/Header'
import { Badge } from '@/components/ui/badge'

export default function WorkflowsListPage() {
  const { workspaceId } = useParams()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [workflowName, setWorkflowName] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [isCreatingWorkflow, setIsCreatingWorkflow] = useState(false)

  const {
    workflows,
    isLoading,
    error,
    fetchWorkflows,
    createWorkflow,
    deleteWorkflow,
    executeWorkflow,
  } = useWorkflowStore()

  // Fetch workflows on mount
  useEffect(() => {
    fetchWorkflows()
  }, [fetchWorkflows])

  const handleCreateWorkflow = async () => {
    if (isCreatingWorkflow || !workflowName.trim()) return
    
    try {
      setIsCreatingWorkflow(true)
      const workflow = await createWorkflow({
        name: workflowName.trim(),
        description: '',
      })
      if (workflow?.id) {
        setIsDialogOpen(false)
        setWorkflowName('')
        // Navigate to the new workflow editor
        navigate(`/workspace/${workspaceId}/w/${workflow.id}`)
      }
    } catch (error) {
      console.error('Failed to create workflow:', error)
      alert('Failed to create workflow. Please try again.')
    } finally {
      setIsCreatingWorkflow(false)
    }
  }

  const handleOpenWorkflow = (workflowId: string) => {
    navigate(`/workspace/${workspaceId}/w/${workflowId}`)
  }

  const handleDeleteWorkflow = async (id: string, name: string, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()

    if (!confirm(`Are you sure you want to delete "${name}"?`)) return

    try {
      await deleteWorkflow(id)
    } catch (error) {
      console.error('Failed to delete workflow:', error)
    }
  }

  const handleExecuteWorkflow = async (id: string, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()

    try {
      const result = await executeWorkflow(id)
      alert(`Workflow execution started: ${result.execution_id}`)
    } catch (error) {
      console.error('Failed to execute workflow:', error)
    }
  }

  const filteredWorkflows = workflows.filter((workflow) =>
    workflow.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="page-container">
      {/* Aurora Background */}
      <div className="aurora-background" />

      {/* Page Header */}
      <div className="page-header flex items-center justify-between fade-in">
        <div>
          <h1 className="page-title">Workflows</h1>
          <p className="page-subtitle">Create and manage your AI workflow automations</p>
        </div>
        <button
          onClick={() => setIsDialogOpen(true)}
          disabled={isLoading}
          className="glass-button flex items-center space-x-2 px-6 py-3"
        >
          <Plus className="h-5 w-5" />
          <span className="font-semibold">New Workflow</span>
        </button>
      </div>

      <div className="space-y-6">
        {/* Error Display */}
        {error && (
          <div className="glass-card p-4 border-red-500/50 bg-red-500/20">
            <p className="text-sm text-red-200">{error}</p>
          </div>
        )}

        {/* Enhanced Search */}
        <div className="glass-panel p-4 fade-in" style={{ animationDelay: '0.1s' }}>
          <div className="relative">
            <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-white/50" />
            <input
              type="text"
              placeholder="Search workflows by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="glass-input pl-12 h-12"
              disabled={isLoading}
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 glass-button p-2"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>

        {/* Loading State */}
        {isLoading && workflows.length === 0 && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        )}

        {/* Workflows Grid */}
        {!isLoading && filteredWorkflows.length > 0 && (
          <div className="grid-3">
            {filteredWorkflows.map((workflow, index) => (
              <div
                key={workflow.id}
                className="glass-card p-6 workflow-card group fade-in"
                style={{ animationDelay: `${index * 0.1}s` }}
                onClick={() => handleOpenWorkflow(workflow.id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    handleOpenWorkflow(workflow.id)
                  }
                }}
              >
                {/* Header with icon and actions */}
                <div className="mb-4 flex items-start justify-between">
                  <div className="workflow-card-icon bg-gradient-to-br from-purple-500/30 to-blue-500/30">
                    <WorkflowIcon className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex gap-2 opacity-0 transition-opacity group-hover:opacity-100">
                    <button
                      onClick={(e) => handleExecuteWorkflow(workflow.id, e)}
                      title="Run workflow"
                      className="glass-button p-2 hover:bg-green-500/20"
                    >
                      <Play className="h-4 w-4" />
                    </button>
                    <button
                      onClick={(e) => handleDeleteWorkflow(workflow.id, workflow.name, e)}
                      title="Delete workflow"
                      className="glass-button p-2 hover:bg-red-500/20"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {/* Content */}
                <h3 className="workflow-card-name mb-2 line-clamp-1">
                  {workflow.name}
                </h3>
                <p className="workflow-card-description mb-4 min-h-[3em] line-clamp-2">
                  {workflow.description || 'No description provided'}
                </p>

                {/* Footer with metadata */}
                <div className="workflow-card-meta border-t border-white/10 pt-4">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    <span>
                      {workflow.updated_at
                        ? formatDistanceToNow(new Date(workflow.updated_at), {
                            addSuffix: true,
                          })
                        : 'Just now'}
                    </span>
                  </div>
                  {workflow.is_deployed && (
                    <div className="glass-badge success">
                      <span className="mr-1 h-2 w-2 animate-pulse rounded-full bg-green-400"></span>
                      Live
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && filteredWorkflows.length === 0 && (
          <div className="flex items-center justify-center py-12 fade-in" style={{ animationDelay: '0.2s' }}>
            <div className="glass-card max-w-md text-center p-8">
              <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-purple-600 shadow-xl shadow-primary/20">
                <WorkflowIcon className="h-10 w-10 text-white" />
              </div>
              <h3 className="mb-3 text-xl font-semibold text-white">
                {searchQuery ? 'No workflows match your search' : 'No workflows yet'}
              </h3>
              <p className="mb-6 text-sm text-white/70">
                {searchQuery
                  ? 'Try adjusting your search terms or create a new workflow'
                  : 'Get started by creating your first AI workflow automation'}
              </p>
              {!searchQuery && (
                <button
                  onClick={() => setIsDialogOpen(true)}
                  className="glass-button w-full flex items-center justify-center space-x-2 px-6 py-3"
                >
                  <Plus className="h-5 w-5" />
                  <span className="font-semibold">Create Your First Workflow</span>
                </button>
              )}
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="glass-button w-full px-6 py-3"
                >
                  Clear Search
                </button>
              )}
            </div>
          </div>
        )}
      </ContentSection>

      {/* Workflow Creation Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-md glass-card border-white/20">
          <DialogHeader>
            <DialogTitle className="text-xl font-semibold text-white">Create New Workflow</DialogTitle>
            <DialogDescription className="text-white/70">
              Enter a name for your new workflow automation
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 mt-4">
            <input
              type="text"
              placeholder="Workflow name..."
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleCreateWorkflow()
                }
              }}
              disabled={isCreatingWorkflow}
              autoFocus
              className="glass-input h-12"
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsDialogOpen(false)}
                disabled={isCreatingWorkflow}
                className="glass-button px-6 py-2"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateWorkflow}
                disabled={isCreatingWorkflow || !workflowName.trim()}
                className="glass-button px-6 py-2 bg-gradient-to-r from-primary/30 to-purple-600/30 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCreatingWorkflow ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin inline" />
                    Creating...
                  </>
                ) : (
                  'Create Workflow'
                )}
              </button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
