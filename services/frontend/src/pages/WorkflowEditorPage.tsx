// @ts-nocheck

import { useCallback, useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import ReactFlow, {
  Background,
  BackgroundVariant,
  ConnectionMode,
  Controls,
  MiniMap,
  Panel,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { Play, Save, ArrowLeft, Loader2, PanelLeftClose, PanelLeft } from 'lucide-react'

import { BlockConfigPanel } from '@/components/workflow/BlockConfigPanel'
import { BlockLibrary } from '@/components/workflow/BlockLibrary'
import { WorkflowPanel } from '@/components/workflow/panel/WorkflowPanel'
import { WorkflowBlockNode } from '@/components/workflow/WorkflowBlockNode'
import { Button } from '@/components/ui/button'
import { buildDefaultConfig } from '@/lib/workflow/blockConfig'
import type { BlockDefinition } from '@/lib/blocks/blockDefinitions'
import { useExecutionStore } from '@/stores/executionStore'
import { usePanelStore } from '@/stores/panel/store'
import { useWorkflowEditorStore } from '@/stores/workflowEditorStore'
import { useWorkflowStore } from '@/stores/workflowStore'

const nodeTypes = {
  workflowBlock: WorkflowBlockNode,
}

export default function WorkflowEditorPage() {
  const { workspaceId, workflowId } = useParams()
  const navigate = useNavigate()
  const [showLibrary, setShowLibrary] = useState(true)
  const [activeExecutionId, setActiveExecutionId] = useState<string | null>(null)

  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    addNode,
    setNodes,
    setEdges,
    selectNode,
    clearSelection,
  } = useWorkflowEditorStore()

  const {
    currentWorkflow,
    fetchWorkflow,
    updateWorkflow,
    executeWorkflow,
    isLoading,
  } = useWorkflowStore()

  const {
    fetchExecution,
    fetchLogs,
    subscribeToExecution,
    unsubscribeFromExecution,
    clearLogs,
    setCurrentExecution,
  } = useExecutionStore()

  const { isOpen: isPanelOpen, togglePanel, setActiveTab } = usePanelStore()

  useEffect(() => {
    if (workflowId) {
      fetchWorkflow(workflowId)
    }
  }, [workflowId, fetchWorkflow])

  useEffect(() => {
    if (!currentWorkflow) return

    setNodes(
      (currentWorkflow.blocks || []).map((block) => ({
        id: block.id,
        type: 'workflowBlock',
        position: block.position,
        data: {
          id: block.id,
          type: block.type,
          name: block.name,
          config:
            (block.data as Record<string, any> | undefined)?.config ??
            (block.data as Record<string, any> | undefined) ??
            {},
        },
      }))
    )

    setEdges(
      (currentWorkflow.edges || []).map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        sourceHandle: edge.sourceHandle ?? undefined,
        targetHandle: edge.targetHandle ?? undefined,
        type: edge.type ?? 'smoothstep',
      }))
    )
  }, [currentWorkflow, setNodes, setEdges])

  const handleBack = () => {
    navigate(`/workspace/${workspaceId}/workflows`)
  }

  const handleAddBlock = useCallback(
    (blockDef: BlockDefinition) => {
      const config = buildDefaultConfig(blockDef)
      addNode({
        type: 'workflowBlock',
        position: { x: 250, y: 250 },
        data: {
          id: '',
          type: blockDef.type,
          name: blockDef.name,
          config,
        },
      })
    },
    [addNode]
  )

  const handleSave = async () => {
    if (!currentWorkflow || !workflowId) return

    try {
      const blocks = nodes.map((node) => ({
        id: node.id,
        type: node.data.type,
        name: node.data.name,
        position: node.position,
        data: { config: node.data.config },
      }))

      const updatedEdges = edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        sourceHandle: edge.sourceHandle ?? null,
        targetHandle: edge.targetHandle ?? null,
        type: edge.type ?? 'smoothstep',
      }))

      await updateWorkflow(workflowId, {
        blocks,
        edges: updatedEdges,
      })

      alert('Workflow saved successfully!')
    } catch (error) {
      console.error('Failed to save workflow:', error)
      alert('Failed to save workflow')
    }
  }

  const handleExecute = async () => {
    if (!workflowId) return

    try {
      const result = await executeWorkflow(workflowId)
      setActiveExecutionId(result.execution_id)
      setCurrentExecution(result.execution_id)
      setActiveTab('console')
      togglePanel()
      alert(`Workflow execution started: ${result.execution_id}`)
    } catch (error) {
      console.error('Failed to execute workflow:', error)
      alert('Failed to execute workflow')
    }
  }

  const handleSelectionChange = useCallback(
    ({ nodes, edges }: { nodes: any[]; edges: any[] }) => {
      if (nodes.length === 1 && edges.length === 0) {
        selectNode(nodes[0].id)
      } else {
        clearSelection()
      }
    },
    [selectNode, clearSelection]
  )

  return (
    <div className='editor-page'>
      <div className='aurora-background' />

      <div className='editor-toolbar glass-panel fade-in'>
        <div className='flex items-center gap-3'>
          <button className='glass-button px-4 py-2' onClick={handleBack}>
            <ArrowLeft className='mr-2 h-4 w-4' />
            Back
          </button>
          <div className='h-6 w-px bg-white/40' />
          <div>
            <p className='text-xs text-white/60'>Workflow</p>
            <h1 className='text-lg font-semibold text-white'>
              {currentWorkflow?.name || 'Loading...'}
            </h1>
          </div>
        </div>

        <div className='flex flex-wrap items-center gap-2'>
          <button className='glass-button px-4 py-2' onClick={() => setShowLibrary(!showLibrary)}>
            {showLibrary ? (
              <>
                <PanelLeftClose className='mr-2 h-4 w-4' />
                Hide Library
              </>
            ) : (
              <>
                <PanelLeft className='mr-2 h-4 w-4' />
                Show Library
              </>
            )}
          </button>
          <button className='glass-button px-4 py-2' onClick={togglePanel}>
            {isPanelOpen ? 'Hide Panel' : 'Show Panel'}
          </button>
          <button className='glass-button px-4 py-2' onClick={handleSave} disabled={isLoading}>
            {isLoading ? (
              <Loader2 className='mr-2 h-4 w-4 animate-spin' />
            ) : (
              <Save className='mr-2 h-4 w-4' />
            )}
            Save
          </button>
          <button
            className='glass-button px-4 py-2 bg-gradient-to-r from-purple-500/30 to-blue-500/30 disabled:opacity-50'
            onClick={handleExecute}
            disabled={isLoading}
          >
            <Play className='mr-2 h-4 w-4' />
            Execute
          </button>
        </div>
      </div>

      <div className='editor-shell'>
        {showLibrary && (
          <div className='editor-library'>
            <BlockLibrary onAddBlock={handleAddBlock} />
          </div>
        )}

        <div className='editor-canvas'>
          <div className='canvas-surface'>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              connectionMode={ConnectionMode.Loose}
              fitView
              snapToGrid
              snapGrid={[20, 20]}
              defaultEdgeOptions={{
                type: 'smoothstep',
                animated: true,
                style: { stroke: '#94a3b8', strokeWidth: 2 },
              }}
              onPaneClick={clearSelection}
              onNodeClick={(_, node) => selectNode(node.id)}
              onSelectionChange={handleSelectionChange}
              className='workflow-canvas'
            >
              <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
              <Controls showInteractive={false} />
              <MiniMap
                nodeColor={(node) => {
                  if (node.selected) return '#3b82f6'
                  return '#cbd5e1'
                }}
                maskColor='rgba(0, 0, 0, 0.08)'
                position='bottom-right'
              />

              <Panel position='top-left' className='space-y-2'>
                {nodes.length === 0 && !showLibrary && (
                  <div className='glass-card p-4 fade-in'>
                    <h3 className='mb-2 font-semibold text-white text-sm'>
                      Get Started
                    </h3>
                    <p className='mb-3 text-white/70 text-xs'>
                      Show the block library to add blocks to your workflow
                    </p>
                    <button onClick={() => setShowLibrary(true)} className='glass-button w-full px-4 py-2 text-sm'>
                      <PanelLeft className='mr-2 h-3 w-3' />
                      Show Library
                    </button>
                  </div>
                )}
              </Panel>

              <Panel position='top-right' className='flex gap-2'>
                <div className='glass-badge px-4 py-2 text-xs'>
                  {nodes.length} blocks · {edges.length} connections
                </div>
              </Panel>
            </ReactFlow>
          </div>
        </div>

        <div className='editor-sidepanels'>
          <BlockConfigPanel />
          <WorkflowPanel workflowId={currentWorkflow?.id ?? null} />
        </div>
      </div>
    </div>
  )

}
