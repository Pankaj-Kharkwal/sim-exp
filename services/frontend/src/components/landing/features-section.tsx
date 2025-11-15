import { motion } from 'framer-motion'
import { featureCards } from '@/constants/landing'

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({ opacity: 1, y: 0, transition: { delay: i * 0.08 } }),
}

export function FeaturesSection() {
  return (
    <div className='grid gap-6 md:grid-cols-2'>
      {featureCards.map((card, index) => (
        <motion.article
          key={card.id}
          custom={index}
          initial='hidden'
          whileInView='visible'
          viewport={{ once: true, amount: 0.5 }}
          variants={cardVariants}
          className='group flex flex-col rounded-3xl border border-white/40 bg-white/70 p-6 shadow-glass backdrop-blur-2xl transition hover:-translate-y-1 hover:shadow-rose-glow dark:border-white/10 dark:bg-white/5'
        >
          <card.icon className='mb-4 h-10 w-10 text-brand-emerald' />
          <h3 className='font-display text-2xl text-brand-peacock dark:text-white'>{card.title}</h3>
          <p className='mt-2 text-base text-neutral-600 dark:text-neutral-200'>{card.description}</p>
          <ul className='mt-4 space-y-2 text-sm text-neutral-500 dark:text-neutral-300'>
            {card.bullets.map((item) => (
              <li key={item} className='flex items-center gap-2'>
                <span className='h-1.5 w-1.5 rounded-full bg-brand-emerald' />
                {item}
              </li>
            ))}
          </ul>
        </motion.article>
      ))}
    </div>
  )
}
