import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import Lottie from 'lottie-react'
import gsap from 'gsap'
import { ArrowRight, Sparkles } from 'lucide-react'
import { useSpring, animated } from '@react-spring/web'
import { Button } from '@/components/ui/button'
import featherAnimation from '@/assets/lottie/feather-glow.json'
import { heroStats } from '@/constants/landing'

const heroVariants = {
  initial: { opacity: 0, y: 32 },
  animate: { opacity: 1, y: 0 },
}

export function Hero() {
  const gradientRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (!gradientRef.current) return
    const ctx = gsap.context(() => {
      gsap.to(gradientRef.current, {
        backgroundPosition: '200% 50%',
        duration: 16,
        repeat: -1,
        ease: 'sine.inOut',
        yoyo: true,
      })
    }, gradientRef)
    return () => ctx.revert()
  }, [])

  const [progress, api] = useSpring(() => ({ value: 0 }))

  useEffect(() => {
    api.start({
      value: 1,
      config: { tension: 90, friction: 18, precision: 0.5 },
    })
  }, [api])

  return (
    <section id='home' className='relative overflow-hidden pt-16 sm:pt-20'>
      <div className='absolute inset-0 -z-10 opacity-70 blur-[120px]' ref={gradientRef} style={{ backgroundImage: 'var(--gradient-feather)' }} />
      <div className='mx-auto flex w-full max-w-[1280px] flex-col gap-12 px-4 md:flex-row md:items-center md:px-8'>
        <motion.div
          className='relative flex-1 space-y-8 rounded-[32px] border border-white/20 bg-white/80 p-8 shadow-glass backdrop-blur-3xl dark:bg-neutral-charcoal/80'
          variants={heroVariants}
          initial='initial'
          animate='animate'
          transition={{ duration: 0.8, delay: 0.1 }}
        >
          <div className='inline-flex items-center gap-2 rounded-full border border-white/30 bg-white/50 px-4 py-1 text-xs uppercase tracking-[0.32em] text-brand-peacock dark:border-white/10 dark:bg-white/5 dark:text-white/80'>
            <Sparkles className='h-4 w-4 text-brand-emerald' />
            Feather-grade studio
          </div>
          <div>
            <h1 className='font-display text-4xl leading-tight text-brand-peacock sm:text-5xl md:text-6xl dark:text-white'>
              Krutrim-native agent workflows that glide across every surface
            </h1>
            <p className='mt-6 max-w-2xl text-lg text-neutral-600 dark:text-neutral-200'>
              Compose AI systems with glassmorphic clarity, swap blocks with a single drag, and watch Gluon trace every action with living telemetry.
            </p>
          </div>
          <div className='flex flex-col gap-4 sm:flex-row'>
            <Button className='btn-ripple h-14 flex-1 rounded-full bg-gradient-to-r from-brand-emerald via-brand-aqua to-brand-royal text-lg text-white shadow-glow'>
              Design your workflow
              <ArrowRight className='h-5 w-5' />
            </Button>
            <Button variant='outline' className='btn-ripple h-14 flex-1 rounded-full border border-brand-emerald/40 bg-white/60 text-lg text-brand-peacock hover:border-brand-royal/60 dark:border-white/20 dark:bg-white/10 dark:text-white'>
              Watch product tour
            </Button>
          </div>
          <div className='grid gap-4 rounded-2xl border border-white/30 bg-white/30 p-4 text-sm shadow-inner dark:border-white/10 dark:bg-white/5'>
            {heroStats.map((stat) => (
              <div key={stat.label} className='flex items-center justify-between rounded-xl bg-white/35 p-4 dark:bg-white/5'>
                <div>
                  <p className='text-xs uppercase tracking-[0.3em] text-neutral-500 dark:text-neutral-400'>{stat.label}</p>
                  <animated.p className='text-2xl font-semibold text-brand-peacock dark:text-white'>
                    {progress.value.to((val) => {
                      const current = Math.round(val * stat.target)
                      if (stat.value.includes('%')) return `${current}%`
                      if (stat.value.includes('+')) return `${current}+`
                      if (stat.value.includes('ms')) return `${current}ms`
                      return current
                    })}
                  </animated.p>
                </div>
                <p className='text-sm text-neutral-500 dark:text-neutral-300'>{stat.helper}</p>
              </div>
            ))}
          </div>
        </motion.div>
        <motion.div
          className='flex flex-1 items-center justify-center rounded-[36px] border border-white/30 bg-white/40 p-10 shadow-xl shadow-brand-peacock/10 ring-1 ring-white/70 dark:border-white/10 dark:bg-white/5 dark:ring-white/5'
          variants={heroVariants}
          initial='initial'
          animate='animate'
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <Lottie animationData={featherAnimation} loop className='h-full max-h-[420px] w-full max-w-[420px]' />
        </motion.div>
      </div>
    </section>
  )
}
