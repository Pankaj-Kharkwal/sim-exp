import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import * as api from '@/lib/api'

export interface WorkflowBlock {
  id: string
  name: string
  type: string
  position: { x: number; y: number }
  data?: Record<string, unknown>
}

export interface WorkflowEdge {
  id: string
  source: string
  target: string
  sourceHandle?: string | null
  targetHandle?: string | null
}

export interface Workflow {
  id: string
  name: string
  description?: string | null
  folder_id?: string | null
  is_deployed: boolean
  blocks: WorkflowBlock[]
  edges: WorkflowEdge[]
  created_at: string
  updated_at: string
}

interface WorkflowState {
  workflows: Workflow[]
  currentWorkflow: Workflow | null
  isLoading: boolean
  error: string | null

  // API Actions
  fetchWorkflows: () => Promise<void>
  fetchWorkflow: (id: string) => Promise<void>
  createWorkflow: (data: {
    name: string
    description?: string
    folder_id?: string
  }) => Promise<Workflow>
  updateWorkflow: (
    id: string,
    data: {
      name?: string
      description?: string
      folder_id?: string
      blocks?: WorkflowBlock[]
      edges?: WorkflowEdge[]
    }
  ) => Promise<void>
  deleteWorkflow: (id: string) => Promise<void>
  executeWorkflow: (
    id: string,
    inputData?: Record<string, unknown>
  ) => Promise<api.ExecutionResult>
  validateWorkflow: (id: string) => Promise<{ valid: boolean; errors?: string[] }>
  deployWorkflow: (id: string, config?: Record<string, unknown>) => Promise<void>

  // Local Actions
  setCurrentWorkflow: (workflow: Workflow | null) => void
  clearError: () => void
}

export const useWorkflowStore = create<WorkflowState>()(
  devtools(
    (set, get) => ({
      workflows: [],
      currentWorkflow: null,
      isLoading: false,
      error: null,

      fetchWorkflows: async () => {
        set({ isLoading: true, error: null })
        try {
          const workflows = await api.listWorkflows()
          set({ workflows, isLoading: false })
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to fetch workflows'
          set({ error: errorMessage, isLoading: false })
        }
      },

      fetchWorkflow: async (id) => {
        set({ isLoading: true, error: null })
        try {
          const workflow = await api.getWorkflow(id)
          set({ currentWorkflow: workflow, isLoading: false })
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to fetch workflow'
          set({ error: errorMessage, isLoading: false })
        }
      },

      createWorkflow: async (data) => {
        set({ isLoading: true, error: null })
        try {
          const workflow = await api.createWorkflow(data)
          set((state) => ({
            workflows: [...state.workflows, workflow],
            currentWorkflow: workflow,
            isLoading: false,
          }))
          return workflow
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to create workflow'
          set({ error: errorMessage, isLoading: false })
          throw error
        }
      },

      updateWorkflow: async (id, data) => {
        set({ isLoading: true, error: null })
        try {
          const updatedWorkflow = await api.updateWorkflow(id, data)

          set((state) => ({
            workflows: state.workflows.map((w) =>
              w.id === id ? updatedWorkflow : w
            ),
            currentWorkflow:
              state.currentWorkflow?.id === id
                ? updatedWorkflow
                : state.currentWorkflow,
            isLoading: false,
          }))
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to update workflow'
          set({ error: errorMessage, isLoading: false })
          throw error
        }
      },

      deleteWorkflow: async (id) => {
        set({ isLoading: true, error: null })
        try {
          await api.deleteWorkflow(id)

          set((state) => ({
            workflows: state.workflows.filter((w) => w.id !== id),
            currentWorkflow:
              state.currentWorkflow?.id === id ? null : state.currentWorkflow,
            isLoading: false,
          }))
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to delete workflow'
          set({ error: errorMessage, isLoading: false })
          throw error
        }
      },

      executeWorkflow: async (id, inputData) => {
        set({ isLoading: true, error: null })
        try {
          const result = await api.executeWorkflow(id, { input_data: inputData })
          set({ isLoading: false })
          return result
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to execute workflow'
          set({ error: errorMessage, isLoading: false })
          throw error
        }
      },

      validateWorkflow: async (id) => {
        set({ isLoading: true, error: null })
        try {
          const result = await api.validateWorkflow(id)
          set({ isLoading: false })
          return result
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to validate workflow'
          set({ error: errorMessage, isLoading: false })
          throw error
        }
      },

      deployWorkflow: async (id, config) => {
        set({ isLoading: true, error: null })
        try {
          await api.deployWorkflow(id, config)

          // Update is_deployed status
          set((state) => ({
            workflows: state.workflows.map((w) =>
              w.id === id ? { ...w, is_deployed: true } : w
            ),
            currentWorkflow:
              state.currentWorkflow?.id === id
                ? { ...state.currentWorkflow, is_deployed: true }
                : state.currentWorkflow,
            isLoading: false,
          }))
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to deploy workflow'
          set({ error: errorMessage, isLoading: false })
          throw error
        }
      },

      setCurrentWorkflow: (workflow) => set({ currentWorkflow: workflow }),

      clearError: () => set({ error: null }),
    }),
    { name: 'workflow-store' }
  )
)
