import { footerColumns } from '@/constants/landing'

export function LandingFooter() {
  return (
    <footer className='border-t border-white/20 bg-white/60 py-12 text-sm text-neutral-600 backdrop-blur-2xl dark:border-white/5 dark:bg-white/5 dark:text-neutral-300'>
      <div className='mx-auto flex w-full max-w-[1280px] flex-col gap-8 px-4 md:px-8 lg:flex-row lg:items-start'>
        <div className='flex-1 space-y-3'>
          <p className='font-display text-xl text-brand-peacock dark:text-white'>Pankh AI</p>
          <p>Featherlight AI-native workflows for teams that fly faster.</p>
          <p className='text-xs text-neutral-500'>© {new Date().getFullYear()} Pankh Labs. All rights reserved.</p>
        </div>
        <div className='grid flex-1 gap-6 sm:grid-cols-2 lg:grid-cols-4'>
          {footerColumns.map((column) => (
            <div key={column.title}>
              <p className='text-xs uppercase tracking-[0.3em] text-brand-emerald'>{column.title}</p>
              <ul className='mt-3 space-y-2 text-sm'>
                {column.links.map((link) => (
                  <li key={link.label}>
                    <a href={link.href} className='transition hover:text-brand-emerald'>
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </footer>
  )
}
