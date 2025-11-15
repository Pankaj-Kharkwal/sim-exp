import { motion } from 'framer-motion'
import { productShowcases } from '@/constants/landing'

export function ProductSection() {
  return (
    <div className='grid gap-6 lg:grid-cols-3'>
      {productShowcases.map((product) => (
        <motion.article
          key={product.id}
          className='flex h-full flex-col rounded-[32px] border border-white/30 bg-white/70 p-6 shadow-glass backdrop-blur-2xl dark:border-white/10 dark:bg-white/5'
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6 }}
        >
          <div className={`inline-flex w-fit items-center rounded-full bg-gradient-to-r ${product.gradient} px-3 py-1 text-xs font-semibold uppercase tracking-[0.4em] text-white`}>
            {product.eyebrow}
          </div>
          <h3 className='mt-4 font-display text-2xl text-brand-peacock dark:text-white'>{product.title}</h3>
          <p className='mt-2 text-base text-neutral-600 dark:text-neutral-200'>{product.description}</p>
          <ul className='mt-6 space-y-3 text-sm text-neutral-500 dark:text-neutral-300'>
            {product.highlights.map((highlight) => (
              <li key={highlight} className='flex items-center gap-2'>
                <span className='h-1.5 w-1.5 rounded-full bg-brand-emerald' />
                {highlight}
              </li>
            ))}
          </ul>
          <div className='mt-auto pt-6 text-sm text-brand-emerald'>Explore playground →</div>
        </motion.article>
      ))}
    </div>
  )
}
