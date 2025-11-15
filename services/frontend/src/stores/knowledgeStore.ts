import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import * as api from '../lib/api'
import type { KnowledgeBase, Document } from '../lib/api'

interface KnowledgeState {
  knowledgeBases: KnowledgeBase[]
  currentKnowledgeBase: KnowledgeBase | null
  documents: Document[]
  currentDocument: Document | null
  searchResults: any[]
  isLoading: boolean
  error: string | null
  uploadProgress: number

  // Knowledge Base Actions
  fetchKnowledgeBases: () => Promise<void>
  fetchKnowledgeBase: (id: string) => Promise<void>
  createKnowledgeBase: (data: {
    name: string
    description?: string
  }) => Promise<KnowledgeBase>
  updateKnowledgeBase: (
    id: string,
    data: { name?: string; description?: string }
  ) => Promise<void>
  deleteKnowledgeBase: (id: string) => Promise<void>

  // Document Actions
  fetchDocuments: (knowledgeBaseId: string) => Promise<void>
  fetchDocument: (knowledgeBaseId: string, documentId: string) => Promise<void>
  uploadDocument: (
    knowledgeBaseId: string,
    file: File,
    metadata?: Record<string, any>
  ) => Promise<Document>
  updateDocument: (
    knowledgeBaseId: string,
    documentId: string,
    data: { name?: string; tags?: string[]; metadata?: Record<string, any> }
  ) => Promise<void>
  deleteDocument: (knowledgeBaseId: string, documentId: string) => Promise<void>
  processDocument: (knowledgeBaseId: string, documentId: string) => Promise<void>

  // Search Actions
  searchKnowledgeBase: (
    knowledgeBaseId: string,
    query: string,
    options?: { limit?: number; threshold?: number }
  ) => Promise<void>

  // Utility Actions
  clearError: () => void
  setCurrentKnowledgeBase: (kb: KnowledgeBase | null) => void
  setCurrentDocument: (doc: Document | null) => void
}

export const useKnowledgeStore = create<KnowledgeState>()(
  devtools(
    (set, get) => ({
      knowledgeBases: [],
      currentKnowledgeBase: null,
      documents: [],
      currentDocument: null,
      searchResults: [],
      isLoading: false,
      error: null,
      uploadProgress: 0,

      // Knowledge Base Actions
      fetchKnowledgeBases: async () => {
        set({ isLoading: true, error: null })
        try {
          const knowledgeBases = await api.listKnowledgeBases()
          set({ knowledgeBases, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      fetchKnowledgeBase: async (id: string) => {
        set({ isLoading: true, error: null })
        try {
          const knowledgeBase = await api.getKnowledgeBase(id)
          set({ currentKnowledgeBase: knowledgeBase, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      createKnowledgeBase: async (data) => {
        set({ isLoading: true, error: null })
        try {
          const knowledgeBase = await api.createKnowledgeBase(data)
          set((state) => ({
            knowledgeBases: [...state.knowledgeBases, knowledgeBase],
            currentKnowledgeBase: knowledgeBase,
            isLoading: false,
          }))
          return knowledgeBase
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      updateKnowledgeBase: async (id: string, data: { name?: string; description?: string }) => {
        set({ isLoading: true, error: null })
        try {
          const updated = await api.updateKnowledgeBase(id, data)
          set((state) => ({
            knowledgeBases: state.knowledgeBases.map((kb) =>
              kb.id === id ? { ...kb, ...updated } : kb
            ),
            currentKnowledgeBase:
              state.currentKnowledgeBase?.id === id
                ? { ...state.currentKnowledgeBase, ...updated }
                : state.currentKnowledgeBase,
            isLoading: false,
          }))
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      deleteKnowledgeBase: async (id: string) => {
        set({ isLoading: true, error: null })
        try {
          await api.deleteKnowledgeBase(id)
          set((state) => ({
            knowledgeBases: state.knowledgeBases.filter((kb) => kb.id !== id),
            currentKnowledgeBase:
              state.currentKnowledgeBase?.id === id
                ? null
                : state.currentKnowledgeBase,
            isLoading: false,
          }))
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      // Document Actions
      fetchDocuments: async (knowledgeBaseId: string) => {
        set({ isLoading: true, error: null })
        try {
          const documents = await api.listDocuments(knowledgeBaseId)
          set({ documents, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      fetchDocument: async (knowledgeBaseId: string, documentId: string) => {
        set({ isLoading: true, error: null })
        try {
          const document = await api.getDocument(knowledgeBaseId, documentId)
          set({ currentDocument: document, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      uploadDocument: async (
        knowledgeBaseId: string,
        file: File,
        metadata?: Record<string, any>
      ) => {
        set({ isLoading: true, error: null, uploadProgress: 0 })
        try {
          const document = await api.uploadDocument(
            knowledgeBaseId,
            file,
            metadata,
            (progress) => {
              set({ uploadProgress: progress })
            }
          )
          set((state) => ({
            documents: [...state.documents, document],
            currentDocument: document,
            isLoading: false,
            uploadProgress: 100,
          }))
          return document
        } catch (error: any) {
          set({ error: error.message, isLoading: false, uploadProgress: 0 })
          throw error
        }
      },

      updateDocument: async (
        knowledgeBaseId: string,
        documentId: string,
        data: { name?: string; tags?: string[]; metadata?: Record<string, any> }
      ) => {
        set({ isLoading: true, error: null })
        try {
          const updated = await api.updateDocument(
            knowledgeBaseId,
            documentId,
            data
          )
          set((state) => ({
            documents: state.documents.map((doc) =>
              doc.id === documentId ? updated : doc
            ),
            currentDocument:
              state.currentDocument?.id === documentId
                ? updated
                : state.currentDocument,
            isLoading: false,
          }))
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      deleteDocument: async (knowledgeBaseId: string, documentId: string) => {
        set({ isLoading: true, error: null })
        try {
          await api.deleteDocument(knowledgeBaseId, documentId)
          set((state) => ({
            documents: state.documents.filter((doc) => doc.id !== documentId),
            currentDocument:
              state.currentDocument?.id === documentId
                ? null
                : state.currentDocument,
            isLoading: false,
          }))
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      processDocument: async (knowledgeBaseId: string, documentId: string) => {
        set({ isLoading: true, error: null })
        try {
          await api.processDocument(knowledgeBaseId, documentId)
          set({ isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      // Search Actions
      searchKnowledgeBase: async (
        knowledgeBaseId: string,
        query: string,
        options?: { limit?: number; threshold?: number }
      ) => {
        set({ isLoading: true, error: null })
        try {
          const results = await api.searchKnowledgeBase(
            knowledgeBaseId,
            query,
            options?.limit
          )
          set({ searchResults: results.results, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      // Utility Actions
      clearError: () => set({ error: null }),
      setCurrentKnowledgeBase: (kb) => set({ currentKnowledgeBase: kb }),
      setCurrentDocument: (doc) => set({ currentDocument: doc }),
    }),
    { name: 'knowledge-store' }
  )
)
