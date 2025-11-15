import * as React from 'react'
import { cn } from '@/lib/utils'

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<'input'>>(
  ({ className, type, autoComplete = 'off', ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-lg border border-border bg-bg px-3 py-2 text-base text-text-primary file:border-0 file:bg-transparent file:font-medium file:text-text-primary file:text-sm placeholder:text-text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50 transition-colors md:text-sm',
          className
        )}
        ref={ref}
        autoComplete={autoComplete}
        autoCorrect='off'
        autoCapitalize='off'
        spellCheck='false'
        {...props}
      />
    )
  }
)
Input.displayName = 'Input'

export { Input }
