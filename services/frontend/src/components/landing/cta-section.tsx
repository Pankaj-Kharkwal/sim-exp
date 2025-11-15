import { Button } from '@/components/ui/button'

export function CTASection() {
  return (
    <div className='rounded-[40px] border border-transparent bg-gradient-to-br from-brand-peacock to-brand-royal p-10 text-white shadow-rose-glow'>
      <div className='flex flex-col gap-6 text-center md:flex-row md:items-center md:text-left'>
        <div className='flex-1 space-y-3'>
          <p className='text-xs uppercase tracking-[0.4em] text-white/70'>Ready to deploy</p>
          <h3 className='font-display text-4xl'>Generate the full Pankh design system now</h3>
          <p className='text-white/80'>
            Invite your team, remix building blocks, and monitor every action through Gluon dashboards.
          </p>
        </div>
        <div className='flex flex-col gap-4 md:w-64'>
          <Button className='h-14 rounded-full bg-white text-brand-peacock hover:bg-white/90'>Create workspace</Button>
          <Button variant='ghost' className='h-14 rounded-full border border-white/40 text-white hover:bg-white/10'>
            Download deck
          </Button>
        </div>
      </div>
    </div>
  )
}
