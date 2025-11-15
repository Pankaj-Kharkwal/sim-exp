import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { motion, useScroll, useTransform } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { navLinks } from '@/constants/landing'
import { ThemeToggle } from './theme-toggle'

export function LandingNav() {
  const { scrollY } = useScroll()
  const bgOpacity = useTransform(scrollY, [0, 120], [0, 0.9])
  const borderOpacity = useTransform(scrollY, [0, 120], [0, 0.35])
  const navBg = useTransform(bgOpacity, (value) => `rgba(8,12,14,${value})`)
  const navBorder = useTransform(borderOpacity, (value) => `rgba(255,255,255,${value})`)

  const internalLinks = useMemo(() => navLinks, [])

  return (
    <motion.header
      className='sticky top-0 z-40 w-full border-b border-transparent backdrop-blur-xl'
      style={{
        backgroundColor: navBg,
        borderColor: navBorder,
      }}
    >
      <div className='mx-auto flex w-full max-w-[1280px] items-center justify-between gap-6 px-4 py-4 md:px-8'>
        <Link to='/' className='flex items-center gap-3'>
          <div className='h-11 w-11 rounded-2xl bg-gradient-to-br from-brand-peacock via-brand-emerald to-brand-aqua p-[1px]'>
            <div className='flex h-full w-full items-center justify-center rounded-2xl bg-white/80 dark:bg-neutral-charcoal/90'>
              <span className='font-display text-xl font-semibold text-brand-peacock'>P</span>
            </div>
          </div>
          <div>
            <p className='font-display text-lg font-semibold tracking-tight text-brand-peacock dark:text-white'>
              Pankh AI
            </p>
            <p className='text-xs uppercase tracking-[0.32em] text-brand-emerald/80 dark:text-brand-emerald/90'>
              Krutrim native
            </p>
          </div>
        </Link>
        <nav className='hidden flex-1 items-center justify-center gap-6 text-sm font-medium text-neutral-700 dark:text-neutral-200 lg:flex'>
          {internalLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className='group/nav relative px-2 py-1 transition hover:text-brand-emerald focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-emerald/60'
            >
              {link.label}
              <span className='absolute inset-x-2 -bottom-1 h-px origin-center scale-x-0 bg-gradient-to-r from-brand-peacock via-brand-aqua to-brand-royal transition-all duration-300 group-hover/nav:scale-x-100' />
            </a>
          ))}
        </nav>
        <div className='flex items-center gap-2'>
          <ThemeToggle className='hidden md:flex' />
          <Link to='/login' className='hidden md:block'>
            <Button variant='ghost' className='btn-ripple border-none text-sm text-white/80 hover:text-white'>
              Console
            </Button>
          </Link>
          <Link to='/signup'>
            <Button
              className={cn(
                'btn-ripple rounded-full bg-gradient-to-r from-brand-emerald via-brand-aqua to-brand-royal text-white shadow-glow',
                'hover:opacity-90'
              )}
            >
              Launch Studio
            </Button>
          </Link>
        </div>
      </div>
    </motion.header>
  )
}
