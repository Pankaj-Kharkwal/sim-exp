import { useMemo } from 'react'
import { motion } from 'framer-motion'
import { testimonials } from '@/constants/landing'

export function TestimonialsSection() {
  const duplicated = useMemo(() => testimonials.concat(testimonials), [])

  return (
    <div className='relative overflow-hidden rounded-[32px] border border-white/30 bg-white/70 p-6 shadow-glass backdrop-blur-2xl dark:border-white/10 dark:bg-white/5'>
      <motion.div
        className='flex gap-6'
        initial={{ x: 0 }}
        animate={{ x: '-50%' }}
        transition={{ duration: 28, ease: 'linear', repeat: Infinity }}
      >
        {duplicated.map((testimonial, idx) => (
          <article
            key={`${testimonial.author}-${idx}`}
            className='w-[320px] rounded-3xl border border-white/50 bg-white/80 p-5 dark:border-white/10 dark:bg-white/5'
          >
            <p className='text-sm text-neutral-600 dark:text-neutral-200'>“{testimonial.quote}”</p>
            <div className='mt-4'>
              <p className='font-semibold text-brand-peacock dark:text-white'>{testimonial.author}</p>
              <p className='text-xs uppercase tracking-[0.3em] text-neutral-500'>
                {testimonial.role} · {testimonial.company}
              </p>
            </div>
            <p className='mt-4 rounded-full bg-brand-emerald/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.3em] text-brand-emerald'>
              {testimonial.highlight}
            </p>
          </article>
        ))}
      </motion.div>
    </div>
  )
}
