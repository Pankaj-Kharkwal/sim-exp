import { Button } from '@/components/ui/button'
import { pricingPlans } from '@/constants/landing'
import { motion } from 'framer-motion'

export function PricingSection() {
  return (
    <div className='grid gap-6 md:grid-cols-3'>
      {pricingPlans.map((plan, idx) => (
        <motion.article
          key={plan.id}
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.4 }}
          transition={{ delay: idx * 0.1 }}
          className={`flex h-full flex-col rounded-[32px] border p-6 ${
            plan.highlighted
              ? 'border-transparent bg-gradient-to-br from-brand-emerald/70 to-brand-royal/60 text-white shadow-rose-glow'
              : 'border-white/40 bg-white/70 text-brand-peacock shadow-glass dark:border-white/10 dark:bg-white/5'
          }`}
        >
          <div>
            <p className='text-xs uppercase tracking-[0.4em] opacity-80'>{plan.name}</p>
            <p className='mt-2 text-4xl font-bold'>
              {plan.price}
              {plan.price !== 'Custom' && <span className='text-base font-medium opacity-80'> / seat</span>}
            </p>
            <p className='mt-2 text-sm opacity-80'>{plan.description}</p>
          </div>
          <ul className='mt-6 space-y-2 text-sm opacity-90'>
            {plan.perks.map((perk) => (
              <li key={perk} className='flex items-center gap-2'>
                <span className='h-1.5 w-1.5 rounded-full bg-current' />
                {perk}
              </li>
            ))}
          </ul>
          <div className='mt-auto pt-6'>
            <Button
              className={`w-full rounded-full ${
                plan.highlighted
                  ? 'bg-white text-brand-peacock hover:bg-white/90'
                  : 'btn-ripple border border-brand-emerald/40 bg-white/80 text-brand-peacock hover:border-brand-royal/60'
              }`}
            >
              {plan.cta}
            </Button>
          </div>
        </motion.article>
      ))}
    </div>
  )
}
