import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
  {
    variants: {
      variant: {
        // Primary action button - uses new primary color
        primary: 'bg-primary text-white hover:bg-primary-hover active:bg-primary-active shadow-sm',
        // Default kept for backward compatibility
        default: 'bg-primary text-white hover:bg-primary-hover active:bg-primary-active shadow-sm',
        // Secondary button - uses surface colors
        secondary: 'bg-surface-3 text-text-primary border border-border hover:bg-surface-4 active:bg-surface-5',
        // Outline button - transparent with border
        outline: 'border border-border bg-transparent hover:bg-surface-2 active:bg-surface-3',
        // Ghost button - minimal styling
        ghost: 'hover:bg-surface-2 hover:text-text-primary',
        // Destructive button - for dangerous actions
        destructive: 'bg-error text-white hover:bg-red-600 active:bg-red-700',
        // Link button
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        xs: 'h-7 px-2 text-xs',
        sm: 'h-8 px-3 text-sm',
        default: 'h-10 px-4 text-sm',
        lg: 'h-11 px-5 text-base',
        xl: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return (
      <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
    )
  }
)
Button.displayName = 'Button'

export { Button, buttonVariants }
