import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import {
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  type Node,
  type Edge,
  type NodeChange,
  type EdgeChange,
  type Connection,
} from 'reactflow'
import type { BlockData } from '@/types/workflow'

export type { BlockData }

export interface WorkflowNode extends Node {
  data: BlockData
}

export type WorkflowEdge = Edge<BlockData>;

interface WorkflowEditorState {
  // Canvas state
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
  selectedNodeId: string | null
  selectedEdgeId: string | null

  // Canvas settings
  canvasZoom: number
  canvasPosition: { x: number; y: number }

  // Interaction state
  isDragging: boolean
  isConnecting: boolean

  // Actions - Node management
  addNode: (node: Omit<WorkflowNode, 'id'>) => void
  updateNode: (nodeId: string, data: Partial<BlockData>) => void
  deleteNode: (nodeId: string) => void
  duplicateNode: (nodeId: string) => void

  // Actions - Edge management
  addEdgeConnection: (connection: Connection) => void
  deleteEdge: (edgeId: string) => void

  // Actions - Selection
  selectNode: (nodeId: string | null) => void
  selectEdge: (edgeId: string | null) => void
  clearSelection: () => void

  // Actions - Canvas
  setCanvasZoom: (zoom: number) => void
  setCanvasPosition: (position: { x: number; y: number }) => void
  fitView: () => void

  // Actions - ReactFlow handlers
  onNodesChange: (changes: NodeChange[]) => void
  onEdgesChange: (changes: EdgeChange[]) => void
  onConnect: (connection: Connection) => void

  // Actions - Bulk operations
  setNodes: (nodes: WorkflowNode[]) => void
  setEdges: (edges: WorkflowEdge[]) => void
  clearCanvas: () => void

  // Actions - State
  setIsDragging: (dragging: boolean) => void
  setIsConnecting: (connecting: boolean) => void
}

let nodeIdCounter = 0
const generateNodeId = () => `node_${Date.now()}_${++nodeIdCounter}`

export const useWorkflowEditorStore = create<WorkflowEditorState>()(
  devtools(
    (set, get) => ({
      // Initial state
      nodes: [],
      edges: [],
      selectedNodeId: null,
      selectedEdgeId: null,
      canvasZoom: 1,
      canvasPosition: { x: 0, y: 0 },
      isDragging: false,
      isConnecting: false,

      // Node management
      addNode: (nodeData) => {
        const newNode: WorkflowNode = {
          ...nodeData,
          id: generateNodeId(),
          type: 'workflowBlock',
        }

        set((state) => ({
          nodes: [...state.nodes, newNode],
          selectedNodeId: newNode.id,
        }))
      },

      updateNode: (nodeId, data) => {
        set((state) => ({
          nodes: state.nodes.map((node) =>
            node.id === nodeId
              ? { ...node, data: { ...node.data, ...data } }
              : node
          ),
        }))
      },

      deleteNode: (nodeId) => {
        set((state) => ({
          nodes: state.nodes.filter((node) => node.id !== nodeId),
          edges: state.edges.filter(
            (edge) => edge.source !== nodeId && edge.target !== nodeId
          ),
          selectedNodeId: state.selectedNodeId === nodeId ? null : state.selectedNodeId,
        }))
      },

      duplicateNode: (nodeId) => {
        const nodeToDuplicate = get().nodes.find((n) => n.id === nodeId)
        if (!nodeToDuplicate) return

        const newNode: WorkflowNode = {
          ...nodeToDuplicate,
          id: generateNodeId(),
          position: {
            x: nodeToDuplicate.position.x + 50,
            y: nodeToDuplicate.position.y + 50,
          },
          data: {
            ...nodeToDuplicate.data,
            name: `${nodeToDuplicate.data.name} (copy)`,
          },
        }

        set((state) => ({
          nodes: [...state.nodes, newNode],
          selectedNodeId: newNode.id,
        }))
      },

      // Edge management
      addEdgeConnection: (connection) => {
        set((state) => ({
          edges: addEdge(connection, state.edges),
        }))
      },

      deleteEdge: (edgeId) => {
        set((state) => ({
          edges: state.edges.filter((edge) => edge.id !== edgeId),
          selectedEdgeId: state.selectedEdgeId === edgeId ? null : state.selectedEdgeId,
        }))
      },

      // Selection
      selectNode: (nodeId) => {
        set({ selectedNodeId: nodeId, selectedEdgeId: null })
      },

      selectEdge: (edgeId) => {
        set({ selectedEdgeId: edgeId, selectedNodeId: null })
      },

      clearSelection: () => {
        set({ selectedNodeId: null, selectedEdgeId: null })
      },

      // Canvas
      setCanvasZoom: (zoom) => {
        set({ canvasZoom: zoom })
      },

      setCanvasPosition: (position) => {
        set({ canvasPosition: position })
      },

      fitView: () => {
        // This will be implemented by ReactFlow's fitView
        // Store just tracks that it was called
      },

      // ReactFlow handlers
      onNodesChange: (changes) => {
        set((state) => ({
          nodes: applyNodeChanges(changes, state.nodes) as WorkflowNode[],
        }))
      },

      onEdgesChange: (changes) => {
        set((state) => ({
          edges: applyEdgeChanges(changes, state.edges) as WorkflowEdge[],
        }))
      },

      onConnect: (connection) => {
        get().addEdgeConnection(connection)
      },

      // Bulk operations
      setNodes: (nodes) => {
        set({ nodes })
      },

      setEdges: (edges) => {
        set({ edges })
      },

      clearCanvas: () => {
        set({
          nodes: [],
          edges: [],
          selectedNodeId: null,
          selectedEdgeId: null,
        })
      },

      // State setters
      setIsDragging: (dragging) => {
        set({ isDragging: dragging })
      },

      setIsConnecting: (connecting) => {
        set({ isConnecting: connecting })
      },
    }),
    { name: 'workflow-editor-store' }
  )
)
