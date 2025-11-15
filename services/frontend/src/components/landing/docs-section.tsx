import { docsCards } from '@/constants/landing'

export function DocsSection() {
  return (
    <div className='grid gap-6 md:grid-cols-2'>
      {docsCards.map((card) => (
        <article
          key={card.title}
          className='flex h-full flex-col rounded-[28px] border border-white/40 bg-white/75 p-6 shadow-glass backdrop-blur-2xl dark:border-white/10 dark:bg-white/5'
        >
          <p className='text-xs uppercase tracking-[0.3em] text-brand-emerald'>{card.title}</p>
          <h3 className='mt-2 font-display text-2xl text-brand-peacock dark:text-white'>{card.description}</h3>
          <pre className='mt-6 flex-1 rounded-2xl bg-neutral-900/90 p-4 text-sm text-white shadow-inner dark:bg-black/60'>
            <code>{card.code}</code>
          </pre>
          <a
            href='#docs'
            className='mt-6 inline-flex items-center gap-2 text-sm font-semibold text-brand-emerald'
          >
            {card.cta} →
          </a>
        </article>
      ))}
    </div>
  )
}
