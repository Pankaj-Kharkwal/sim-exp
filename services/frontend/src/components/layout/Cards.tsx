import { HTMLAttributes, ReactNode, forwardRef } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'
import { LucideIcon } from 'lucide-react'

const cardVariants = cva(
  'relative rounded-2xl transition-all duration-300',
  {
    variants: {
      variant: {
        glass: [
          'bg-background/60 backdrop-blur-xl border border-border/40',
          'shadow-lg hover:shadow-xl hover:border-border/60',
        ].join(' '),
        gradient: [
          'bg-gradient-to-br from-background via-background/95 to-accent/20',
          'border border-border/40 shadow-lg hover:shadow-xl',
        ].join(' '),
        solid: 'bg-card border border-border shadow-md hover:shadow-lg',
        outline: 'border-2 border-border hover:border-primary/50',
        glow: [
          'bg-gradient-to-br from-primary/5 via-purple-500/5 to-background',
          'border border-primary/20 shadow-xl shadow-primary/10',
          'hover:shadow-2xl hover:shadow-primary/20',
        ].join(' '),
      },
      hover: {
        lift: 'hover:-translate-y-1',
        scale: 'hover:scale-[1.02]',
        glow: 'hover:ring-2 hover:ring-primary/20',
        none: '',
      },
      padding: {
        none: '',
        sm: 'p-4',
        md: 'p-6',
        lg: 'p-8',
      },
    },
    defaultVariants: {
      variant: 'glass',
      hover: 'lift',
      padding: 'md',
    },
  }
)

export interface CardProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, hover, padding, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(cardVariants({ variant, hover, padding }), className)}
        {...props}
      >
        {children}
      </div>
    )
  }
)

Card.displayName = 'Card'

// Metric Card Component
export interface MetricCardProps {
  title: string
  value: string | number
  icon?: LucideIcon
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  subtitle?: string
  variant?: 'glass' | 'gradient' | 'glow'
  className?: string
}

export function MetricCard({
  title,
  value,
  icon: Icon,
  trend,
  trendValue,
  subtitle,
  variant = 'glass',
  className,
}: MetricCardProps) {
  const trendColors = {
    up: 'text-emerald-500',
    down: 'text-red-500',
    neutral: 'text-amber-500',
  }

  return (
    <Card variant={variant} hover="lift" className={cn('group', className)}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            {title}
          </p>
          <p className="mt-2 text-3xl font-bold">{value}</p>
          {subtitle && (
            <p className="mt-1 text-xs text-muted-foreground">{subtitle}</p>
          )}
        </div>
        {Icon && (
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/10 to-purple-500/10 text-primary transition-transform group-hover:scale-110">
            <Icon className="h-6 w-6" />
          </div>
        )}
      </div>
      {trend && trendValue && (
        <div className="mt-4 flex items-center gap-2">
          <Badge variant="secondary" className={cn('text-xs', trendColors[trend])}>
            {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {trendValue}
          </Badge>
          <span className="text-xs text-muted-foreground">vs last period</span>
        </div>
      )}
    </Card>
  )
}

// Feature Card Component
export interface FeatureCardProps {
  icon: ReactNode
  title: string
  description: string
  badge?: string
  onClick?: () => void
  className?: string
}

export function FeatureCard({
  icon,
  title,
  description,
  badge,
  onClick,
  className,
}: FeatureCardProps) {
  return (
    <Card
      variant="glass"
      hover="scale"
      onClick={onClick}
      className={cn(
        'group cursor-pointer',
        onClick && 'hover:border-primary/40',
        className
      )}
    >
      <div className="flex flex-col items-center text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/10 to-purple-500/10 text-primary transition-all group-hover:scale-110 group-hover:from-primary/20 group-hover:to-purple-500/20">
          {icon}
        </div>
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold">{title}</h3>
          {badge && (
            <Badge variant="secondary" className="text-xs">
              {badge}
            </Badge>
          )}
        </div>
        <p className="mt-2 text-sm text-muted-foreground">{description}</p>
      </div>
    </Card>
  )
}

// Stat Card with Progress
export interface StatCardProps {
  label: string
  value: number
  max: number
  unit?: string
  color?: 'primary' | 'success' | 'warning' | 'danger'
  className?: string
}

export function StatCard({
  label,
  value,
  max,
  unit,
  color = 'primary',
  className,
}: StatCardProps) {
  const percentage = (value / max) * 100

  const colorClasses = {
    primary: 'bg-primary',
    success: 'bg-emerald-500',
    warning: 'bg-amber-500',
    danger: 'bg-red-500',
  }

  return (
    <Card variant="glass" className={className}>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-muted-foreground">{label}</span>
          <span className="text-2xl font-bold">
            {value}
            {unit && <span className="text-sm text-muted-foreground"> {unit}</span>}
          </span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-secondary">
          <div
            className={cn(
              'h-full rounded-full transition-all duration-500',
              colorClasses[color]
            )}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
        <p className="text-xs text-muted-foreground">
          {percentage.toFixed(1)}% of {max} {unit}
        </p>
      </div>
    </Card>
  )
}

// Pricing Card Component
export interface PricingCardProps {
  name: string
  price: string | number
  period?: string
  description: string
  features: string[]
  highlighted?: boolean
  cta: string
  onCTAClick?: () => void
  badge?: string
  className?: string
}

export function PricingCard({
  name,
  price,
  period = '/month',
  description,
  features,
  highlighted,
  cta,
  onCTAClick,
  badge,
  className,
}: PricingCardProps) {
  return (
    <Card
      variant={highlighted ? 'glow' : 'glass'}
      hover={highlighted ? 'glow' : 'lift'}
      className={cn(
        'flex flex-col',
        highlighted && 'border-primary/40 ring-2 ring-primary/20',
        className
      )}
    >
      {badge && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2">
          <Badge className="bg-gradient-to-r from-primary to-purple-600 text-white shadow-lg">
            {badge}
          </Badge>
        </div>
      )}

      <div className="flex-1 space-y-6">
        <div>
          <h3 className="text-2xl font-bold">{name}</h3>
          <p className="mt-2 text-sm text-muted-foreground">{description}</p>
        </div>

        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-bold">${price}</span>
          <span className="text-sm text-muted-foreground">{period}</span>
        </div>

        <ul className="space-y-3">
          {features.map((feature, idx) => (
            <li key={idx} className="flex items-start gap-3">
              <svg
                className="mt-0.5 h-5 w-5 shrink-0 text-primary"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span className="text-sm">{feature}</span>
            </li>
          ))}
        </ul>
      </div>

      <button
        onClick={onCTAClick}
        className={cn(
          'mt-6 w-full rounded-xl py-3 font-semibold transition-all',
          highlighted
            ? 'bg-gradient-to-r from-primary to-purple-600 text-white shadow-lg hover:shadow-xl hover:scale-105'
            : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
        )}
      >
        {cta}
      </button>
    </Card>
  )
}
