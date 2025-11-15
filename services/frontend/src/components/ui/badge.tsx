import type * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        // Default badge - neutral
        default: 'bg-surface-3 text-text-secondary border-border',
        // Primary badge - brand color
        primary: 'bg-primary text-white border-transparent',
        // Semantic status badges
        success: 'bg-success-bg text-green-700 dark:text-green-400 border-success-border',
        warning: 'bg-warning-bg text-amber-700 dark:text-amber-400 border-warning-border',
        error: 'bg-error-bg text-red-700 dark:text-red-400 border-error-border',
        info: 'bg-info-bg text-blue-700 dark:text-blue-400 border-info-border',
        // Legacy variants for backward compatibility
        secondary: 'bg-surface-3 text-text-secondary border-border',
        destructive: 'bg-error-bg text-red-700 dark:text-red-400 border-error-border',
        outline: 'border-border bg-transparent text-text-primary',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
