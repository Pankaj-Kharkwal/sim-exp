import { ReactNode, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { ChevronLeft, ChevronRight, LucideIcon } from 'lucide-react'

export interface SidebarNavItem {
  icon: LucideIcon
  label: string
  path: string
  badge?: string | number
  variant?: 'default' | 'pro' | 'new'
}

export interface SidebarSection {
  title?: string
  items: SidebarNavItem[]
}

export interface SidebarProps {
  logo?: ReactNode
  sections: SidebarSection[]
  footer?: ReactNode
  defaultCollapsed?: boolean
  className?: string
}

export function Sidebar({
  logo,
  sections,
  footer,
  defaultCollapsed = false,
  className
}: SidebarProps) {
  const [collapsed, setCollapsed] = useState(defaultCollapsed)
  const location = useLocation()

  return (
    <aside
      className={cn(
        'relative flex h-screen flex-col border-r border-border/40 bg-gradient-to-b from-background/95 to-background/60 backdrop-blur-xl transition-all duration-300',
        collapsed ? 'w-16' : 'w-64',
        className
      )}
    >
      {/* Aurora effect */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-4 top-0 h-72 w-72 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute -right-4 bottom-0 h-72 w-72 rounded-full bg-purple-500/5 blur-3xl" />
      </div>

      {/* Header */}
      <div className="relative z-10 flex h-16 items-center justify-between gap-2 px-4">
        {!collapsed && logo}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className="h-8 w-8 shrink-0"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Navigation */}
      <ScrollArea className="relative z-10 flex-1 px-3">
        <nav className="space-y-6 py-4">
          {sections.map((section, idx) => (
            <div key={idx}>
              {section.title && !collapsed && (
                <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {section.title}
                </p>
              )}
              <div className="space-y-1">
                {section.items.map((item) => (
                  <SidebarNavLink
                    key={item.path}
                    item={item}
                    collapsed={collapsed}
                    isActive={
                      location.pathname === item.path ||
                      location.pathname.startsWith(`${item.path}/`)
                    }
                  />
                ))}
              </div>
              {idx < sections.length - 1 && (
                <Separator className="my-4 bg-border/40" />
              )}
            </div>
          ))}
        </nav>
      </ScrollArea>

      {/* Footer */}
      {footer && (
        <div className="relative z-10 border-t border-border/40 p-4">
          {footer}
        </div>
      )}
    </aside>
  )
}

interface SidebarNavLinkProps {
  item: SidebarNavItem
  collapsed: boolean
  isActive: boolean
}

function SidebarNavLink({ item, collapsed, isActive }: SidebarNavLinkProps) {
  const content = (
    <Link to={item.path}>
      <Button
        variant={isActive ? 'secondary' : 'ghost'}
        className={cn(
          'group relative w-full justify-start gap-3 overflow-hidden transition-all',
          collapsed ? 'aspect-square w-10 justify-center p-0' : 'h-10 px-3',
          isActive && [
            'bg-gradient-to-r from-primary/10 to-purple-500/10',
            'text-primary shadow-sm',
            'before:absolute before:left-0 before:h-full before:w-1 before:bg-gradient-to-b before:from-primary before:to-purple-500',
          ],
          !isActive && 'hover:bg-accent/50 hover:text-accent-foreground'
        )}
      >
        <item.icon className={cn(
          'h-4 w-4 shrink-0 transition-transform',
          isActive && 'text-primary',
          !collapsed && 'group-hover:scale-110'
        )} />
        {!collapsed && (
          <>
            <span className="flex-1 text-left text-sm font-medium">
              {item.label}
            </span>
            {item.badge && (
              <Badge
                variant={item.variant === 'pro' ? 'default' : 'secondary'}
                className={cn(
                  'h-5 px-1.5 text-[10px] font-semibold',
                  item.variant === 'pro' && 'bg-gradient-to-r from-amber-500 to-orange-500',
                  item.variant === 'new' && 'bg-gradient-to-r from-emerald-500 to-teal-500'
                )}
              >
                {item.badge}
              </Badge>
            )}
          </>
        )}
      </Button>
    </Link>
  )

  if (collapsed) {
    return (
      <TooltipProvider delayDuration={0}>
        <Tooltip>
          <TooltipTrigger asChild>{content}</TooltipTrigger>
          <TooltipContent side="right" className="flex items-center gap-2">
            <span>{item.label}</span>
            {item.badge && (
              <Badge variant="secondary" className="h-5 px-1.5 text-[10px]">
                {item.badge}
              </Badge>
            )}
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    )
  }

  return content
}

// Sidebar Logo Component
export function SidebarLogo({ title, icon }: { title: string; icon?: ReactNode }) {
  return (
    <div className="flex items-center gap-3">
      {icon || (
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600 shadow-lg">
          <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"
            />
          </svg>
        </div>
      )}
      <div>
        <p className="text-sm font-bold leading-none">{title}</p>
        <p className="text-xs text-muted-foreground">Workspace</p>
      </div>
    </div>
  )
}

// Sidebar Footer Component
export function SidebarFooter({ user, onLogout }: {
  user?: { name: string; email: string; avatar?: string }
  onLogout?: () => void
}) {
  return (
    <div className="space-y-3">
      {user && (
        <div className="rounded-xl bg-gradient-to-r from-background/50 to-accent/20 p-3 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-primary to-purple-600 text-sm font-bold text-white">
              {user.avatar || user.name[0]}
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="truncate text-sm font-medium">{user.name}</p>
              <p className="truncate text-xs text-muted-foreground">{user.email}</p>
            </div>
          </div>
        </div>
      )}
      {onLogout && (
        <Button
          variant="ghost"
          className="w-full justify-start gap-2 text-muted-foreground hover:text-foreground"
          onClick={onLogout}
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Logout
        </Button>
      )}
    </div>
  )
}
