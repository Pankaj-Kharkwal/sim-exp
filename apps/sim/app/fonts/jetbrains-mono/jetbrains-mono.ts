import { JetBrains_Mono } from 'next/font/google'

export const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
  // Variable font supports weights from 100-800
  weight: ['400', '500', '600'],
  fallback: ['Consolas', 'Monaco', 'Courier New', 'monospace'],
})
