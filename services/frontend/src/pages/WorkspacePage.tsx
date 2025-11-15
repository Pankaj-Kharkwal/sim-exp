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
  Bell,
  Search,
  Plus,
  TrendingUp,
  CheckCircle2,
} from 'lucide-react'
import { Sidebar, SidebarLogo, SidebarFooter } from '@/components/layout/Sidebar'
import { ActionButton } from '@/components/layout/ActionButtons'
import { MetricCard } from '@/components/layout/Cards'
import { Header, PageContainer, ContentSection, Grid } from '@/components/layout/Header'
import { Badge } from '@/components/ui/badge'

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
      <div className="flex h-screen">
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

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto">
          <div className="space-y-6 p-8">
            {/* Beautiful Header */}
            <Header
              title="Sim Workflow Studio"
              subtitle="Workspace · Canvas"
              badge={workspaceId ? `ID · ${workspaceId.slice(0, 8)}` : undefined}
              actions={
                <>
                  <ActionButton variant="ghost" size="icon">
                    <Search className="h-4 w-4" />
                  </ActionButton>
                  <ActionButton variant="ghost" size="icon">
                    <Bell className="h-4 w-4" />
                  </ActionButton>
                  <ActionButton
                    variant="primary"
                    leftIcon={<Plus className="h-4 w-4" />}
                    onClick={() => navigate(`/workspace/${workspaceId}/workflows/new`)}
                  >
                    New Workflow
                  </ActionButton>
                </>
              }
            />

            {/* Metrics Section */}
            <ContentSection
              title="Workspace Insights"
              description="Monitor your workflows and resources at a glance"
            >
              <Grid cols={3} gap={6}>
                <MetricCard
                  title="Active Workflows"
                  value={0}
                  icon={Workflow}
                  subtitle="Drafts waiting to run"
                  variant="glass"
                />
                <MetricCard
                  title="Knowledge Bases"
                  value={0}
                  icon={Database}
                  subtitle="Connect docs for RAG"
                  variant="glass"
                />
                <MetricCard
                  title="System Status"
                  value="Live"
                  icon={CheckCircle2}
                  trend="up"
                  trendValue="+100%"
                  subtitle="All systems operational"
                  variant="glow"
                />
              </Grid>
            </ContentSection>

            {/* Main Content Outlet */}
            <ContentSection>
              <div className="min-h-[400px] rounded-2xl border border-border/40 bg-gradient-to-br from-background/95 via-background/90 to-background/60 p-6 shadow-lg backdrop-blur-xl">
                <Outlet />
              </div>
            </ContentSection>
          </div>
        </main>
      </div>
    </PageContainer>
  )
}
