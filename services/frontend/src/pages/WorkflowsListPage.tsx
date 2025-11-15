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
    <div className="space-y-6">
      {/* Header Section */}
      <ContentSection
        title="Workflows"
        description="Create and manage your AI workflow automations"
        action={
          <ActionButton
            variant="primary"
            leftIcon={<Plus className="h-4 w-4" />}
            onClick={() => setIsDialogOpen(true)}
            loading={isLoading}
          >
            New Workflow
          </ActionButton>
        }
      >
        {/* Error Display */}
        {error && (
          <Card variant="solid" className="border-red-500/50 bg-red-500/10">
            <p className="text-sm text-red-600">{error}</p>
          </Card>
        )}

        {/* Enhanced Search */}
        <div className="relative">
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search workflows by name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-12 pl-12 text-base"
            disabled={isLoading}
          />
          {searchQuery && (
            <ActionButton
              variant="ghost"
              size="icon"
              onClick={() => setSearchQuery('')}
              className="absolute right-2 top-1/2 -translate-y-1/2"
            >
              <Trash2 className="h-4 w-4" />
            </ActionButton>
          )}
        </div>

        {/* Loading State */}
        {isLoading && workflows.length === 0 && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        )}

        {/* Workflows Grid */}
        {!isLoading && filteredWorkflows.length > 0 && (
          <Grid cols={3} gap={6}>
            {filteredWorkflows.map((workflow) => (
              <Card
                key={workflow.id}
                variant="glass"
                hover="lift"
                className="group cursor-pointer"
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
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-purple-500/20 text-primary shadow-lg transition-transform group-hover:scale-110">
                    <WorkflowIcon className="h-6 w-6" />
                  </div>
                  <div className="flex gap-2 opacity-0 transition-opacity group-hover:opacity-100">
                    <ActionButton
                      variant="success"
                      size="icon"
                      onClick={(e) => handleExecuteWorkflow(workflow.id, e)}
                      title="Run workflow"
                    >
                      <Play className="h-4 w-4" />
                    </ActionButton>
                    <ActionButton
                      variant="danger"
                      size="icon"
                      onClick={(e) => handleDeleteWorkflow(workflow.id, workflow.name, e)}
                      title="Delete workflow"
                    >
                      <Trash2 className="h-4 w-4" />
                    </ActionButton>
                  </div>
                </div>

                {/* Content */}
                <h3 className="mb-2 line-clamp-1 text-lg font-semibold transition-colors group-hover:text-primary">
                  {workflow.name}
                </h3>
                <p className="mb-4 min-h-[3em] line-clamp-2 text-sm text-muted-foreground">
                  {workflow.description || 'No description provided'}
                </p>

                {/* Footer with metadata */}
                <div className="flex items-center justify-between border-t border-border/40 pt-4">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
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
                    <Badge variant="default" className="bg-gradient-to-r from-emerald-500 to-green-500">
                      <span className="mr-1 h-2 w-2 animate-pulse rounded-full bg-white"></span>
                      Live
                    </Badge>
                  )}
                </div>
              </Card>
            ))}
          </Grid>
        )}

        {/* Empty State */}
        {!isLoading && filteredWorkflows.length === 0 && (
          <div className="flex items-center justify-center py-12">
            <Card variant="glass" className="max-w-md text-center">
              <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-purple-600 shadow-xl shadow-primary/20">
                <WorkflowIcon className="h-10 w-10 text-white" />
              </div>
              <h3 className="mb-3 text-xl font-semibold">
                {searchQuery ? 'No workflows match your search' : 'No workflows yet'}
              </h3>
              <p className="mb-6 text-sm text-muted-foreground">
                {searchQuery
                  ? 'Try adjusting your search terms or create a new workflow'
                  : 'Get started by creating your first AI workflow automation'}
              </p>
              {!searchQuery && (
                <ActionButton
                  variant="primary"
                  leftIcon={<Plus className="h-5 w-5" />}
                  onClick={() => setIsDialogOpen(true)}
                  className="w-full"
                >
                  Create Your First Workflow
                </ActionButton>
              )}
              {searchQuery && (
                <ActionButton
                  variant="secondary"
                  onClick={() => setSearchQuery('')}
                  className="w-full"
                >
                  Clear Search
                </ActionButton>
              )}
            </Card>
          </div>
        )}
      </ContentSection>

      {/* Workflow Creation Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Create New Workflow</DialogTitle>
            <DialogDescription>
              Enter a name for your new workflow automation
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <Input
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
            />
            <div className="flex justify-end gap-2">
              <ActionButton
                variant="ghost"
                onClick={() => setIsDialogOpen(false)}
                disabled={isCreatingWorkflow}
              >
                Cancel
              </ActionButton>
              <ActionButton
                variant="primary"
                onClick={handleCreateWorkflow}
                disabled={isCreatingWorkflow || !workflowName.trim()}
                loading={isCreatingWorkflow}
              >
                {isCreatingWorkflow ? 'Creating...' : 'Create Workflow'}
              </ActionButton>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
