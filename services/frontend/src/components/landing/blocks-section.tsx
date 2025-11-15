import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'
import { blockCategories } from '@/constants/landing'

export function BlocksSection() {
  return (
    <div className='rounded-[36px] border border-white/30 bg-white/60 p-6 shadow-glass backdrop-blur-2xl dark:border-white/10 dark:bg-white/5'>
      <div className='grid gap-6 md:grid-cols-2'>
        {blockCategories.map((category, idx) => (
          <motion.div
            key={category.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ delay: idx * 0.1 }}
            className='flex h-full flex-col rounded-3xl border border-white/30 bg-white/80 p-6 dark:border-white/10 dark:bg-white/[0.04]'
          >
            <div className='flex items-center justify-between'>
              <h3 className='font-display text-xl text-brand-peacock dark:text-white'>{category.title}</h3>
              <ArrowRight className='h-5 w-5 text-brand-emerald' />
            </div>
            <p className='mt-3 text-sm text-neutral-600 dark:text-neutral-300'>{category.description}</p>
            <div className='mt-6 flex flex-wrap gap-4'>
              {category.metrics.map((metric) => (
                <div key={metric.label} className='rounded-2xl border border-brand-emerald/20 bg-brand-emerald/5 px-4 py-3 text-sm text-brand-peacock dark:text-brand-emerald'>
                  <p className='text-xs uppercase tracking-[0.3em] text-neutral-500'>{metric.label}</p>
                  <p className='text-lg font-semibold'>{metric.value}</p>
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
