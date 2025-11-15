declare module '@studio-freight/lenis' {
  export interface LenisOptions {
    duration?: number
    smoothWheel?: boolean
    smoothTouch?: boolean
    [key: string]: unknown
  }

  export default class Lenis {
    constructor(options?: LenisOptions)
    raf(time: number): void
    destroy(): void
  }
}
