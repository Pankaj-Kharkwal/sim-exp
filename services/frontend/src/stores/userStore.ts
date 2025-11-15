import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import * as api from '@/lib/api'
import { socketManager } from '@/lib/socket'

interface User {
  id: string
  email: string
  name: string
  email_verified?: boolean
  image?: string | null
}

interface UserState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  signup: (email: string, password: string, name: string) => Promise<void>
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  fetchCurrentUser: () => Promise<void>
  refreshAccessToken: () => Promise<void>
  clearError: () => void
}

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,

        signup: async (email, password, name) => {
          set({ isLoading: true, error: null })
          try {
            const response = await api.signup({ email, password, name })

            // Store tokens in localStorage
            localStorage.setItem('access_token', response.token)
            if (response.refresh_token) {
              localStorage.setItem('refresh_token', response.refresh_token)
            }

            set({
              token: response.token,
              refreshToken: response.refresh_token || null,
              user: response.user,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            })
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Signup failed'
            set({
              isLoading: false,
              error: errorMessage,
              isAuthenticated: false,
            })
            throw error
          }
        },

        login: async (email, password) => {
          set({ isLoading: true, error: null })
          try {
            const response = await api.login({ username: email, password })

            // Store tokens in localStorage
            localStorage.setItem('access_token', response.access_token)
            if (response.refresh_token) {
              localStorage.setItem('refresh_token', response.refresh_token)
            }

            set({
              token: response.access_token,
              refreshToken: response.refresh_token || null,
              isLoading: false,
              error: null,
            })

            // Fetch user details after login
            await get().fetchCurrentUser()

            // Initialize Socket.IO connection
            const token = response.access_token
            socketManager.connect()
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Login failed'
            set({
              isLoading: false,
              error: errorMessage,
              isAuthenticated: false,
            })
            throw error
          }
        },

        fetchCurrentUser: async () => {
          const token = get().token || localStorage.getItem('access_token')
          if (!token) {
            set({ isAuthenticated: false, user: null })
            return
          }

          set({ isLoading: true, error: null })
          try {
            const user = await api.getCurrentUser()
            set({
              user,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            })
          } catch (error) {
            // Token might be invalid, logout
            get().logout()
            set({ isLoading: false })
          }
        },

        logout: () => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          socketManager.disconnect()
          set({
            user: null,
            token: null,
            refreshToken: null,
            isAuthenticated: false,
            error: null,
          })
        },

        refreshAccessToken: async () => {
          const refreshToken = get().refreshToken || localStorage.getItem('refresh_token')
          if (!refreshToken) {
            get().logout()
            return
          }

          try {
            const response = await api.refreshToken(refreshToken)

            // Store new tokens
            localStorage.setItem('access_token', response.access_token)
            if (response.refresh_token) {
              localStorage.setItem('refresh_token', response.refresh_token)
            }

            set({
              token: response.access_token,
              refreshToken: response.refresh_token || null,
            })
          } catch (error) {
            // Refresh failed, logout user
            get().logout()
          }
        },

        clearError: () => set({ error: null }),
      }),
      {
        name: 'user-storage',
        partialize: (state) => ({
          token: state.token,
          refreshToken: state.refreshToken,
          user: state.user,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    ),
    { name: 'user-store' }
  )
)
