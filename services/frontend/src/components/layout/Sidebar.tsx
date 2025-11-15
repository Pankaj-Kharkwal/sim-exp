import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'

interface SidebarItem {
  icon: React.ComponentType<{ className?: string }>
  label: string
  path: string
  badge?: string
  variant?: 'new' | 'pro'
}

interface SidebarSection {
  title?: string
  items: SidebarItem[]
}

interface SidebarProps {
  logo?: ReactNode
  sections: SidebarSection[]
  footer?: ReactNode
}

export function Sidebar({ logo, sections, footer }: SidebarProps) {
  const location = useLocation()

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-card">
      {/* Logo */}
      {logo && <div className="border-b p-4">{logo}</div>}

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {sections.map((section, idx) => (
          <div key={idx} className="space-y-2">
            {section.title && (
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide px-2">
                {section.title}
              </h3>
            )}
            <div className="space-y-1">
              {section.items.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={cn(
                      'flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    <span className="flex-1">{item.label}</span>
                    {item.badge && (
                      <span
                        className={cn(
                          'px-2 py-0.5 text-xs rounded-full font-semibold',
                          item.variant === 'new'
                            ? 'bg-green-500/20 text-green-600'
                            : item.variant === 'pro'
                            ? 'bg-purple-500/20 text-purple-600'
                            : 'bg-blue-500/20 text-blue-600'
                        )}
                      >
                        {item.badge}
                      </span>
                    )}
                  </Link>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      {footer && <div className="border-t p-4">{footer}</div>}
    </div>
  )
}

interface SidebarLogoProps {
  title: string
  icon?: ReactNode
}

export function SidebarLogo({ title, icon }: SidebarLogoProps) {
  return (
    <div className="flex items-center gap-2">
      {icon}
      <span className="text-lg font-semibold">{title}</span>
    </div>
  )
}

interface User {
  name: string
  email: string
}

interface SidebarFooterProps {
  user?: User
  onLogout?: () => void
}

export function SidebarFooter({ user, onLogout }: SidebarFooterProps) {
  if (!user) {
    return (
      <div className="text-sm text-muted-foreground">
        Not logged in
      </div>
    )
  }

  return (
    <div className="flex items-center justify-between gap-3">
      <div className="flex items-center gap-3 min-w-0">
        <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-semibold">
          {user.name.charAt(0).toUpperCase()}
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium truncate">{user.name}</p>
          <p className="text-xs text-muted-foreground truncate">{user.email}</p>
        </div>
      </div>
      {onLogout && (
        <button
          onClick={onLogout}
          className="text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          Logout
        </button>
      )}
    </div>
  )
}
