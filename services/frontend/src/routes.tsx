import { createBrowserRouter, Navigate } from 'react-router-dom'

// Lazy load pages for better performance
import { lazy } from 'react'

const LandingPage = lazy(() => import('@/pages/LandingPage'))
const ChatPage = lazy(() => import('@/pages/ChatPage'))
const LoginPage = lazy(() => import('@/pages/LoginPage'))
const SignupPage = lazy(() => import('@/pages/SignupPage'))
const WorkspacePage = lazy(() => import('@/pages/WorkspacePage'))
const WorkspaceHomePage = lazy(() => import('@/pages/WorkspaceHomePage'))
const WorkflowsListPage = lazy(() => import('@/pages/WorkflowsListPage'))
const WorkflowEditorPage = lazy(() => import('@/pages/WorkflowEditorPage'))
const TemplatesPage = lazy(() => import('@/pages/TemplatesPage'))
const ToolsPage = lazy(() => import('@/pages/ToolsPage'))
const KnowledgePage = lazy(() => import('@/pages/KnowledgePage'))
const LogsPage = lazy(() => import('@/pages/LogsPage'))
const SettingsPage = lazy(() => import('@/pages/SettingsPage'))

export const router = createBrowserRouter([
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/signup',
    element: <SignupPage />,
  },
  {
    path: '/dashboard',
    element: <Navigate to="/workspace/default" replace />,
  },
  {
    path: '/chat',
    element: <ChatPage />,
  },
  {
    path: '/chat/:identifier',
    element: <ChatPage />,
  },
  {
    path: '/workspace/:workspaceId',
    element: <WorkspacePage />,
    children: [
      {
        index: true,
        element: <WorkspaceHomePage />,
      },
      {
        path: 'workflows',
        element: <WorkflowsListPage />,
      },
      {
        path: 'templates',
        element: <TemplatesPage />,
      },
      {
        path: 'tools',
        element: <ToolsPage />,
      },
      {
        path: 'knowledge',
        element: <KnowledgePage />,
      },
      {
        path: 'logs',
        element: <LogsPage />,
      },
      {
        path: 'settings',
        element: <SettingsPage />,
      },
    ],
  },
  {
    path: '/workspace/:workspaceId/workflows/:workflowId',
    element: <WorkflowEditorPage />,
  },
])
