import { useEffect } from 'react'

// Lenis scroll library - commented out due to import resolution issues
// Uncomment when needed and ensure @studio-freight/lenis is properly installed
// import Lenis from '@studio-freight/lenis'

export function useLenis(options?: any) {
  // Smooth scroll hook - currently disabled
  // Re-enable by uncommenting the Lenis import above
  useEffect(() => {
    // TODO: Implement Lenis scroll when library import is resolved
  }, [options])
}
