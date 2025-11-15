import { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'

export interface HeaderProps {
  title: string
  subtitle?: string
  badge?: string
  actions?: ReactNode
  className?: string
}

export function Header({
  title,
  subtitle,
  badge,
  actions,
  className
}: HeaderProps) {
  return (
    <header
      className={cn(
        'relative overflow-hidden rounded-2xl border border-border/40 bg-gradient-to-br from-background/95 via-background/90 to-background/60 p-6 shadow-lg backdrop-blur-xl transition-all',
        className
      )}
    >
      {/* Aurora effect */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute -bottom-10 -left-10 h-40 w-40 rounded-full bg-purple-500/10 blur-3xl" />
      </div>

      <div className="relative z-10 flex flex-wrap items-center justify-between gap-4">
        <div>
          {subtitle && (
            <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {subtitle}
            </p>
          )}
          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-2xl font-bold text-foreground">{title}</h1>
            {badge && (
              <Badge
                variant="secondary"
                className="border-primary/20 bg-gradient-to-r from-primary/10 to-purple-500/10 text-primary shadow-sm"
              >
                {badge}
              </Badge>
            )}
          </div>
        </div>

        {actions && (
          <div className="flex flex-wrap items-center gap-2">
            {actions}
          </div>
        )}
      </div>
    </header>
  )
}

// Page Container Component
export interface PageContainerProps {
  children: ReactNode
  className?: string
}

export function PageContainer({ children, className }: PageContainerProps) {
  return (
    <div
      className={cn(
        'relative min-h-screen overflow-hidden bg-gradient-to-br from-background via-background/98 to-accent/5',
        className
      )}
    >
      {/* Global aurora effects */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-1/4 top-0 h-96 w-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute -right-1/4 bottom-0 h-96 w-96 rounded-full bg-purple-500/5 blur-3xl" />
      </div>

      <div className="relative z-10">{children}</div>
    </div>
  )
}

// Content Section Component
export interface ContentSectionProps {
  title?: string
  description?: string
  action?: ReactNode
  children: ReactNode
  className?: string
}

export function ContentSection({
  title,
  description,
  action,
  children,
  className
}: ContentSectionProps) {
  return (
    <section className={cn('space-y-4', className)}>
      {(title || description || action) && (
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            {title && (
              <h2 className="text-xl font-semibold text-foreground">{title}</h2>
            )}
            {description && (
              <p className="mt-1 text-sm text-muted-foreground">{description}</p>
            )}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </section>
  )
}

// Grid Layout Component
export interface GridProps {
  children: ReactNode
  cols?: 1 | 2 | 3 | 4 | 6
  gap?: 2 | 3 | 4 | 6 | 8
  className?: string
}

export function Grid({ children, cols = 3, gap = 4, className }: GridProps) {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
    6: 'grid-cols-2 md:grid-cols-3 lg:grid-cols-6',
  }

  const gridGap = {
    2: 'gap-2',
    3: 'gap-3',
    4: 'gap-4',
    6: 'gap-6',
    8: 'gap-8',
  }

  return (
    <div className={cn('grid', gridCols[cols], gridGap[gap], className)}>
      {children}
    </div>
  )
}
