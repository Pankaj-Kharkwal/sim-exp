import type { ReactNode } from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

type SectionHeadingProps = {
  eyebrow?: string
  title: string
  description?: string
  align?: 'left' | 'center'
  actions?: ReactNode
  className?: string
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = 'left',
  actions,
  className,
}: SectionHeadingProps) {
  return (
    <motion.div
      className={cn(
        'flex w-full flex-col gap-4',
        align === 'center' ? 'text-center items-center' : 'text-left',
        className
      )}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.5 }}
      transition={{ duration: 0.6 }}
    >
      {eyebrow && (
        <span className='text-xs font-semibold uppercase tracking-[0.4em] text-brand-emerald'>
          {eyebrow}
        </span>
      )}
      <div className='max-w-3xl space-y-4'>
        <h2 className='font-display text-3xl font-semibold text-brand-peacock dark:text-white sm:text-4xl'>
          {title}
        </h2>
        {description && <p className='text-lg text-neutral-600 dark:text-neutral-200'>{description}</p>}
      </div>
      {actions && <div className='mt-4'>{actions}</div>}
    </motion.div>
  )
}
