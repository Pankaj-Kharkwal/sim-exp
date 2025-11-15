import { motion } from 'framer-motion'
import { workflowStages } from '@/constants/landing'

export function WorkflowSection() {
  return (
    <div className='relative overflow-hidden rounded-[36px] border border-white/30 bg-gradient-to-br from-brand-peacock/10 via-brand-emerald/10 to-brand-aqua/10 p-8 shadow-glass backdrop-blur-3xl dark:border-white/10 dark:from-brand-peacock/20 dark:via-brand-emerald/20 dark:to-brand-aqua/20'>
      <div className='absolute inset-y-0 left-1/2 w-px -translate-x-1/2 bg-gradient-to-b from-transparent via-white/50 to-transparent opacity-60' />
      <div className='relative grid gap-10 md:grid-cols-2'>
        {workflowStages.map((stage) => (
          <motion.div
            key={stage.step}
            className='rounded-3xl border border-white/40 bg-white/80 p-6 text-left dark:border-white/10 dark:bg-white/5'
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ delay: stage.step * 0.05 }}
          >
            <div className='flex items-center gap-3'>
              <span className='flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-emerald to-brand-aqua font-semibold text-white'>
                {stage.step}
              </span>
              <span className='rounded-full bg-brand-emerald/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.3em] text-brand-emerald'>
                {stage.badge}
              </span>
            </div>
            <h3 className='mt-4 font-display text-2xl text-brand-peacock dark:text-white'>{stage.title}</h3>
            <p className='mt-2 text-sm text-neutral-600 dark:text-neutral-200'>{stage.description}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
