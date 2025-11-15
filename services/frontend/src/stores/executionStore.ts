// @ts-nocheck

import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import * as api from '../lib/api'
import { onSocketEvent, offSocketEvent, joinExecution, leaveExecution } from '../lib/socket'

interface ExecutionLog {
  id: string
  execution_id: string
  timestamp: string
  level: 'debug' | 'info' | 'warning' | 'error'
  message: string
  metadata?: Record<string, any>
}

interface Execution {
  id: string
  workflow_id: string
  workflow_name?: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  input_data?: Record<string, any>
  output_data?: Record<string, any>
  error_message?: string
  started_at?: string
  completed_at?: string
  duration_ms?: number
  created_at: string
  updated_at: string
}

interface ExecutionState {
  executions: Execution[]
  currentExecution: Execution | null
  logs: ExecutionLog[]
  isLoading: boolean
  error: string | null

  // Execution Actions
  fetchExecutions: (filters?: {
    workflow_id?: string
    status?: string
    limit?: number
  }) => Promise<void>
  fetchExecution: (id: string) => Promise<void>
  cancelExecution: (id: string) => Promise<void>

  // Logs Actions
  fetchLogs: (executionId: string) => Promise<void>
  clearLogs: () => void

  // Real-time Actions
  subscribeToExecution: (executionId: string) => void
  unsubscribeFromExecution: (executionId: string) => void

  // Utility Actions
  clearError: () => void
  setCurrentExecution: (execution: Execution | null) => void
  reset: () => void
}

export const useExecutionStore = create<ExecutionState>()(
  devtools(
    (set, get) => ({
      executions: [],
      currentExecution: null,
      logs: [],
      isLoading: false,
      error: null,

      // Execution Actions
      fetchExecutions: async (filters) => {
        set({ isLoading: true, error: null })
        try {
          const executions = await api.listExecutions(
            filters?.workflow_id,
            filters?.status,
            filters?.limit
          )
          set({ executions, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      fetchExecution: async (id: string) => {
        set({ isLoading: true, error: null })
        try {
          const execution = await api.getExecution(id)
          set({ currentExecution: execution, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      cancelExecution: async (id: string) => {
        set({ isLoading: true, error: null })
        try {
          await api.cancelExecution(id)
          // Update execution status in state
          set((state) => ({
            executions: state.executions.map((exec) =>
              exec.id === id ? { ...exec, status: 'cancelled' as const } : exec
            ),
            currentExecution:
              state.currentExecution?.id === id
                ? { ...state.currentExecution, status: 'cancelled' as const }
                : state.currentExecution,
            isLoading: false,
          }))
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      // Logs Actions
      fetchLogs: async (executionId: string) => {
        set({ isLoading: true, error: null })
        try {
          const logs = await api.getExecutionLogs(executionId)
          set({ logs, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      clearLogs: () => set({ logs: [] }),

      // Real-time Actions
      subscribeToExecution: (executionId: string) => {
        // Join execution room
        joinExecution(executionId)

        // Listen for execution updates
        onSocketEvent('execution:progress', (data) => {
          if (data.execution_id === executionId) {
            set((state) => ({
              currentExecution: state.currentExecution
                ? { ...state.currentExecution, status: data.status as any }
                : null,
            }))
          }
        })

        onSocketEvent('execution:completed', (data) => {
          if (data.execution_id === executionId) {
            set((state) => ({
              currentExecution: state.currentExecution
                ? {
                    ...state.currentExecution,
                    status: data.status,
                    output_data: data.output,
                    error_message: data.error,
                  }
                : null,
              executions: state.executions.map((exec) =>
                exec.id === executionId
                  ? {
                      ...exec,
                      status: data.status,
                      output_data: data.output,
                      error_message: data.error,
                    }
                  : exec
              ),
            }))
          }
        })

        onSocketEvent('execution:log', (data) => {
          if (data.execution_id === executionId) {
            set((state) => ({
              logs: [
                ...state.logs,
                {
                  id: `${Date.now()}`,
                  execution_id: data.execution_id,
                  timestamp: data.timestamp,
                  level: data.level,
                  message: data.message,
                },
              ],
            }))
          }
        })
      },

      unsubscribeFromExecution: (executionId: string) => {
        leaveExecution(executionId)
        offSocketEvent('execution:progress')
        offSocketEvent('execution:completed')
        offSocketEvent('execution:log')
      },

      // Utility Actions
      clearError: () => set({ error: null }),
      setCurrentExecution: (execution) => set({ currentExecution: execution }),
      reset: () =>
        set({
          executions: [],
          currentExecution: null,
          logs: [],
          isLoading: false,
          error: null,
        }),
    }),
    { name: 'execution-store' }
  )
)
