import { integrationPartners } from '@/constants/landing'

export function IntegrationsSection() {
  return (
    <div className='overflow-hidden rounded-[32px] border border-white/30 bg-white/60 p-6 shadow-glass backdrop-blur-2xl dark:border-white/10 dark:bg-white/5'>
      <p className='text-xs uppercase tracking-[0.4em] text-neutral-500'>Integrations</p>
      <div className='mt-4 flex gap-8 whitespace-nowrap text-lg font-medium text-brand-peacock dark:text-white'>
        <div className='flex animate-marquee gap-8'>
          {integrationPartners.concat(integrationPartners).map((partner, idx) => (
            <a
              key={`${partner.name}-${idx}`}
              href={partner.href}
              className='rounded-full border border-brand-emerald/30 px-6 py-2 text-sm uppercase tracking-[0.35em] transition hover:border-brand-emerald hover:text-brand-emerald'
            >
              {partner.name}
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}
