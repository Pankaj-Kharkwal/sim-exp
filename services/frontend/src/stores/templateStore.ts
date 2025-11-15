import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import * as api from '@/lib/api'

interface TemplateState {
  templates: api.TemplateListItem[]
  currentTemplate: api.Template | null
  isLoading: boolean
  error: string | null
  total: number
  page: number
  pageSize: number
  totalPages: number

  // Filters
  category: string | null
  search: string
  sortBy: 'created_at' | 'views' | 'uses' | 'name'
  sortOrder: 'asc' | 'desc'
  myTemplatesOnly: boolean

  // API Actions
  fetchTemplates: (resetPage?: boolean) => Promise<void>
  fetchTemplate: (id: string) => Promise<void>
  createTemplate: (data: api.TemplateCreate) => Promise<api.Template>
  updateTemplate: (id: string, data: api.TemplateUpdate) => Promise<void>
  deleteTemplate: (id: string) => Promise<void>
  starTemplate: (id: string) => Promise<void>
  unstarTemplate: (id: string) => Promise<void>
  useTemplate: (id: string, params?: { workflow_name?: string; folder_id?: string }) => Promise<api.WorkflowSummary>

  // Filter Actions
  setCategory: (category: string | null) => void
  setSearch: (search: string) => void
  setSortBy: (sortBy: 'created_at' | 'views' | 'uses' | 'name') => void
  setSortOrder: (sortOrder: 'asc' | 'desc') => void
  setMyTemplatesOnly: (myTemplatesOnly: boolean) => void
  setPage: (page: number) => void

  // Local Actions
  setCurrentTemplate: (template: api.Template | null) => void
  clearError: () => void
  reset: () => void
}

export const useTemplateStore = create<TemplateState>()(
  devtools(
    (set, get) => ({
      templates: [],
      currentTemplate: null,
      isLoading: false,
      error: null,
      total: 0,
      page: 1,
      pageSize: 24,
      totalPages: 0,

      // Filters
      category: null,
      search: '',
      sortBy: 'created_at',
      sortOrder: 'desc',
      myTemplatesOnly: false,

      fetchTemplates: async (resetPage = false) => {
        set({ isLoading: true, error: null })

        const state = get()
        const currentPage = resetPage ? 1 : state.page

        try {
          const response = await api.listTemplates({
            skip: (currentPage - 1) * state.pageSize,
            limit: state.pageSize,
            category: state.category || undefined,
            search: state.search || undefined,
            sort_by: state.sortBy,
            sort_order: state.sortOrder,
            my_templates: state.myTemplatesOnly,
          })

          set({
            templates: response.templates,
            total: response.total,
            page: response.page,
            pageSize: response.page_size,
            totalPages: response.total_pages,
            isLoading: false,
          })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to fetch templates',
            isLoading: false,
          })
        }
      },

      fetchTemplate: async (id: string) => {
        set({ isLoading: true, error: null })
        try {
          const template = await api.getTemplate(id)
          set({ currentTemplate: template, isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to fetch template',
            isLoading: false,
          })
        }
      },

      createTemplate: async (data: api.TemplateCreate) => {
        set({ isLoading: true, error: null })
        try {
          const template = await api.createTemplate(data)
          set({ isLoading: false })

          // Refresh templates list
          await get().fetchTemplates()

          return template
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to create template',
            isLoading: false,
          })
          throw error
        }
      },

      updateTemplate: async (id: string, data: api.TemplateUpdate) => {
        set({ isLoading: true, error: null })
        try {
          const template = await api.updateTemplate(id, data)

          // Update current template if it's the one being updated
          if (get().currentTemplate?.id === id) {
            set({ currentTemplate: template })
          }

          // Refresh templates list
          await get().fetchTemplates()

          set({ isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to update template',
            isLoading: false,
          })
          throw error
        }
      },

      deleteTemplate: async (id: string) => {
        set({ isLoading: true, error: null })
        try {
          await api.deleteTemplate(id)

          // Clear current template if it's the one being deleted
          if (get().currentTemplate?.id === id) {
            set({ currentTemplate: null })
          }

          // Refresh templates list
          await get().fetchTemplates()

          set({ isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to delete template',
            isLoading: false,
          })
          throw error
        }
      },

      starTemplate: async (id: string) => {
        try {
          await api.starTemplate(id)

          // Optimistically update UI
          const templates = get().templates.map(t =>
            t.id === id
              ? { ...t, user_has_starred: true, star_count: t.star_count + 1 }
              : t
          )
          set({ templates })

          // Update current template if it's starred
          if (get().currentTemplate?.id === id) {
            set(state => ({
              currentTemplate: state.currentTemplate
                ? {
                    ...state.currentTemplate,
                    user_has_starred: true,
                    star_count: state.currentTemplate.star_count + 1,
                  }
                : null,
            }))
          }
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Failed to star template' })
          // Revert optimistic update
          await get().fetchTemplates()
          throw error
        }
      },

      unstarTemplate: async (id: string) => {
        try {
          await api.unstarTemplate(id)

          // Optimistically update UI
          const templates = get().templates.map(t =>
            t.id === id
              ? { ...t, user_has_starred: false, star_count: Math.max(0, t.star_count - 1) }
              : t
          )
          set({ templates })

          // Update current template if it's unstarred
          if (get().currentTemplate?.id === id) {
            set(state => ({
              currentTemplate: state.currentTemplate
                ? {
                    ...state.currentTemplate,
                    user_has_starred: false,
                    star_count: Math.max(0, state.currentTemplate.star_count - 1),
                  }
                : null,
            }))
          }
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Failed to unstar template' })
          // Revert optimistic update
          await get().fetchTemplates()
          throw error
        }
      },

      useTemplate: async (id: string, params?: { workflow_name?: string; folder_id?: string }) => {
        set({ isLoading: true, error: null })
        try {
          const workflow = await api.useTemplate(id, params)

          // Increment use count optimistically
          const templates = get().templates.map(t =>
            t.id === id ? { ...t, uses: t.uses + 1 } : t
          )
          set({ templates, isLoading: false })

          return workflow
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to use template',
            isLoading: false,
          })
          throw error
        }
      },

      setCategory: (category: string | null) => {
        set({ category })
        get().fetchTemplates(true) // Reset to page 1
      },

      setSearch: (search: string) => {
        set({ search })
        // Debounce search in the component
      },

      setSortBy: (sortBy) => {
        set({ sortBy })
        get().fetchTemplates(true)
      },

      setSortOrder: (sortOrder) => {
        set({ sortOrder })
        get().fetchTemplates(true)
      },

      setMyTemplatesOnly: (myTemplatesOnly) => {
        set({ myTemplatesOnly })
        get().fetchTemplates(true)
      },

      setPage: (page) => {
        set({ page })
        get().fetchTemplates()
      },

      setCurrentTemplate: (template) => {
        set({ currentTemplate: template })
      },

      clearError: () => {
        set({ error: null })
      },

      reset: () => {
        set({
          templates: [],
          currentTemplate: null,
          isLoading: false,
          error: null,
          total: 0,
          page: 1,
          totalPages: 0,
          category: null,
          search: '',
          sortBy: 'created_at',
          sortOrder: 'desc',
          myTemplatesOnly: false,
        })
      },
    }),
    { name: 'template-store' }
  )
)
