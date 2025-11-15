import {
  LandingNav,
  Hero,
  SectionHeading,
  FeaturesSection,
  ProductSection,
  BlocksSection,
  WorkflowSection,
  IntegrationsSection,
  PricingSection,
  TestimonialsSection,
  DocsSection,
  CTASection,
  LandingFooter,
} from '@/components/landing'
import { useLenis } from '@/hooks/useLenis'
import { useAOS } from '@/hooks/useAOS'

export default function LandingPage() {
  useLenis()
  useAOS()

  return (
    <div className='relative min-h-screen bg-transparent text-brand-peacock'>
      <div className='parallax-bg' aria-hidden='true' />
      <LandingNav />
      <main className='relative z-10 flex flex-col gap-20 pb-20'>
        <Hero />

        <section id='why' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Why Pankh'
            title='Luxury-grade AI workflows grounded in Krutrim intelligence'
            description='Pair AI-native ergonomics with enterprise guardrails. Every block, workflow, and metric inherits the Krutrim Pankh palette and motion system.'
          />
          <div className='mt-8'>
            <FeaturesSection />
          </div>
        </section>

        <section id='integrations' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <IntegrationsSection />
        </section>

        <section id='product' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Product'
            title='Home, Product, Workflow Builder, Gluon & more in one design language'
            description='Preview every surface—hero, product, blocks, and observability dashboards—crafted with feather gradients and glass surfaces.'
          />
          <div className='mt-8'>
            <ProductSection />
          </div>
        </section>

        <section id='blocks' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Blocks Library'
            title='Remixable building blocks with motion-aware cards'
            description='Organize your RAG, automation, creative, and trust layers within glass cards enriched by rose-gold borders.'
          />
          <div className='mt-8'>
            <BlocksSection />
          </div>
        </section>

        <section id='workflow' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Workflow Builder'
            title='Featherlight multi-LLM orchestration'
            description='Map every stage from orchestration to Gluon analytics with Lenis-powered scroll and Framer Motion reveals.'
          />
          <div className='mt-8'>
            <WorkflowSection />
          </div>
        </section>

        <section id='gluon' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Gluon Observability'
            title='Span-by-span observability built into the brand system'
            description='Design dark-mode dashboards with rose-gold counters, anomaly badges, and responsive tiles to monitor every agent.'
          />
          <div className='mt-8 rounded-[36px] border border-white/20 bg-white/70 p-6 text-neutral-600 shadow-glass backdrop-blur-2xl dark:border-white/5 dark:bg-white/5 dark:text-neutral-200'>
            <p>
              Gluon telemetry cards, metric reels, and alert drawers now share the same gradients,
              typography, and spacing grid used on marketing surfaces. Plug the JSON spec into your
              dashboard or Next.js app to render glassmorphic analytics instantly.
            </p>
          </div>
        </section>

        <section id='pricing' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Pricing'
            title='Feather, Flight, and Constellation plans'
            description='Rose-gold gradients, frosted borders, and glowing CTAs ready for your billing pages.'
          />
          <div className='mt-8'>
            <PricingSection />
          </div>
        </section>

        <section id='testimonials' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Testimonials'
            title='Trusted by teams shipping at 144Hz'
            description='Carousel-ready cards with neon glows to celebrate your champions.'
          />
          <div className='mt-8'>
            <TestimonialsSection />
          </div>
        </section>

        <section id='docs' className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <SectionHeading
            eyebrow='Docs & SDK'
            title='Page-by-page wireframes + starter code'
            description='Drop-in glass cards that showcase CLI snippets, Blocks SDK samples, and onboarding steps.'
          />
          <div className='mt-8'>
            <DocsSection />
          </div>
        </section>

        <section className='mx-auto w-full max-w-[1280px] px-4 md:px-8'>
          <CTASection />
        </section>
      </main>
      <LandingFooter />
    </div>
  )
}
