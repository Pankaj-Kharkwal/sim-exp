import { useEffect, useState } from 'react'
import { Moon, Sun } from 'lucide-react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

export function ThemeToggle({ className }: { className?: string }) {
  const [mounted, setMounted] = useState(false)
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    setMounted(true)
    const stored = window.localStorage.getItem('pankh-theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const nextDark = stored ? stored === 'dark' : prefersDark
    setIsDark(nextDark)
    document.documentElement.classList.toggle('dark', nextDark)
    document.body.classList.toggle('dark', nextDark)
  }, [])

  const toggle = () => {
    const next = !isDark
    setIsDark(next)
    window.localStorage.setItem('pankh-theme', next ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', next)
    document.body.classList.toggle('dark', next)
  }

  if (!mounted) {
    return (
      <div
        className={cn(
          'h-10 w-10 rounded-full border border-white/30 bg-white/20 backdrop-blur-md',
          className
        )}
      />
    )
  }

  return (
    <button
      type='button'
      aria-label='Toggle theme'
      aria-pressed={isDark}
      onClick={toggle}
      className={cn(
        'relative flex h-11 w-20 items-center rounded-full border border-white/20 bg-white/10 px-2 text-white transition hover:border-white/40',
        'dark:border-white/10 dark:bg-black/30',
        className
      )}
    >
      <motion.span
        layout
        className='absolute inset-y-1 w-8 rounded-full bg-white shadow-glass dark:bg-brand-emerald'
        transition={{ type: 'spring', stiffness: 300, damping: 20 }}
        style={{
          left: isDark ? 'calc(100% - 2.75rem)' : '0.5rem',
        }}
      />
      <Sun className={cn('relative z-10 h-4 w-4', isDark ? 'opacity-40' : 'opacity-100')} />
      <Moon className={cn('relative z-10 ml-auto h-4 w-4', isDark ? 'opacity-100' : 'opacity-40')} />
    </button>
  )
}
