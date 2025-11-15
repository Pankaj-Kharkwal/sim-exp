import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

const actionButtonVariants = cva(
  'relative inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 overflow-hidden group',
  {
    variants: {
      variant: {
        primary: [
          'bg-gradient-to-r from-primary via-purple-600 to-primary bg-size-200 bg-pos-0',
          'text-primary-foreground shadow-lg shadow-primary/20',
          'hover:bg-pos-100 hover:shadow-xl hover:shadow-primary/30 hover:scale-[1.02]',
          'active:scale-[0.98]',
        ].join(' '),
        secondary: [
          'bg-gradient-to-r from-secondary to-accent',
          'text-secondary-foreground shadow-md',
          'hover:shadow-lg hover:scale-[1.02]',
          'active:scale-[0.98]',
        ].join(' '),
        glass: [
          'bg-background/60 backdrop-blur-xl border border-border/40',
          'text-foreground shadow-lg',
          'hover:bg-background/80 hover:border-border/60 hover:shadow-xl',
          'hover:scale-[1.02] active:scale-[0.98]',
        ].join(' '),
        gradient: [
          'bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500',
          'text-white shadow-lg shadow-emerald-500/20',
          'hover:shadow-xl hover:shadow-emerald-500/30 hover:scale-[1.02]',
          'active:scale-[0.98]',
        ].join(' '),
        glow: [
          'bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600',
          'text-white shadow-lg shadow-purple-500/50',
          'hover:shadow-2xl hover:shadow-purple-500/60 hover:scale-[1.02]',
          'active:scale-[0.98]',
          'before:absolute before:inset-0 before:rounded-xl before:bg-gradient-to-r before:from-violet-600 before:via-purple-600 before:to-fuchsia-600 before:opacity-0 before:transition-opacity before:duration-300',
          'hover:before:opacity-100 before:blur-xl before:-z-10',
        ].join(' '),
        success: [
          'bg-gradient-to-r from-emerald-500 to-green-500',
          'text-white shadow-lg shadow-emerald-500/20',
          'hover:shadow-xl hover:shadow-emerald-500/30 hover:scale-[1.02]',
          'active:scale-[0.98]',
        ].join(' '),
        danger: [
          'bg-gradient-to-r from-red-500 to-rose-500',
          'text-white shadow-lg shadow-red-500/20',
          'hover:shadow-xl hover:shadow-red-500/30 hover:scale-[1.02]',
          'active:scale-[0.98]',
        ].join(' '),
        outline: [
          'border-2 border-primary bg-transparent',
          'text-primary hover:bg-primary hover:text-primary-foreground',
          'transition-all duration-200',
        ].join(' '),
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        xs: 'h-7 px-2.5 text-xs',
        sm: 'h-9 px-4 text-sm',
        md: 'h-10 px-5 text-sm',
        lg: 'h-12 px-6 text-base',
        xl: 'h-14 px-8 text-lg',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

export interface ActionButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof actionButtonVariants> {
  loading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
}

export const ActionButton = forwardRef<HTMLButtonElement, ActionButtonProps>(
  ({ className, variant, size, loading, leftIcon, rightIcon, children, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(actionButtonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && <Loader2 className="h-4 w-4 animate-spin" />}
        {!loading && leftIcon && <span className="shrink-0">{leftIcon}</span>}
        {children}
        {!loading && rightIcon && <span className="shrink-0">{rightIcon}</span>}

        {/* Shimmer effect */}
        {(variant === 'primary' || variant === 'glow') && (
          <span className="absolute inset-0 -z-10 block h-full w-full animate-shimmer bg-gradient-to-r from-transparent via-white/10 to-transparent bg-[length:200%_100%]" />
        )}
      </button>
    )
  }
)

ActionButton.displayName = 'ActionButton'

// Floating Action Button Component
export interface FABProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode
  label?: string
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left'
}

export const FAB = forwardRef<HTMLButtonElement, FABProps>(
  ({ icon, label, position = 'bottom-right', className, ...props }, ref) => {
    const positionClasses = {
      'bottom-right': 'bottom-6 right-6',
      'bottom-left': 'bottom-6 left-6',
      'top-right': 'top-6 right-6',
      'top-left': 'top-6 left-6',
    }

    return (
      <button
        ref={ref}
        className={cn(
          'fixed z-50 flex items-center gap-2 rounded-full bg-gradient-to-r from-primary to-purple-600 px-4 py-3 text-white shadow-2xl shadow-primary/40 transition-all hover:scale-110 hover:shadow-3xl hover:shadow-primary/60 active:scale-95',
          positionClasses[position],
          className
        )}
        {...props}
      >
        <span className="flex h-6 w-6 items-center justify-center">{icon}</span>
        {label && <span className="text-sm font-semibold">{label}</span>}
      </button>
    )
  }
)

FAB.displayName = 'FAB'

// Button Group Component
export function ButtonGroup({ children, className }: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn('inline-flex items-center rounded-xl shadow-sm', className)}>
      {children}
    </div>
  )
}
