import { useParams, useNavigate, Outlet } from 'react-router-dom'
import {
  Home,
  Workflow,
  Database,
  Activity,
  Settings,
  LayoutTemplate,
  Wrench,
  Sparkles,
} from 'lucide-react'
import { Sidebar, SidebarLogo, SidebarFooter } from '@/components/layout/Sidebar'
import { PageContainer } from '@/components/layout/Header'

export default function WorkspacePage() {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  // Sidebar navigation structure
  const sidebarSections = [
    {
      items: [
        { icon: Home, label: 'Home', path: `/workspace/${workspaceId}` },
        { icon: Workflow, label: 'Workflows', path: `/workspace/${workspaceId}/workflows`, badge: 'Beta', variant: 'new' as const },
        { icon: LayoutTemplate, label: 'Templates', path: `/workspace/${workspaceId}/templates` },
        { icon: Database, label: 'Knowledge', path: `/workspace/${workspaceId}/knowledge` },
      ],
    },
    {
      title: 'Tools & Settings',
      items: [
        { icon: Wrench, label: 'Tools', path: `/workspace/${workspaceId}/tools`, badge: 'Pro', variant: 'pro' as const },
        { icon: Activity, label: 'Logs', path: `/workspace/${workspaceId}/logs` },
        { icon: Settings, label: 'Settings', path: `/workspace/${workspaceId}/settings` },
      ],
    },
  ]

  // Get user info from localStorage
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  return (
    <PageContainer>
      {/* Aurora Background */}
      <div className="aurora-background" />

      <div className="flex h-screen relative z-10">
        {/* Modular Sidebar */}
        <Sidebar
          logo={<SidebarLogo title="Sim Workspace" icon={<Sparkles className="h-5 w-5 text-white" />} />}
          sections={sidebarSections}
          footer={
            <SidebarFooter
              user={user ? {
                name: user.full_name || user.email?.split('@')[0] || 'User',
                email: user.email || 'user@example.com',
              } : undefined}
              onLogout={handleLogout}
            />
          }
        />

        {/* Main Content Area - Clean and Simple */}
        <main className="flex-1 overflow-auto">
          <div className="p-8">
            <Outlet />
          </div>
        </main>
      </div>
    </PageContainer>
  )
}
