import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Utility function to merge Tailwind CSS classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format a date into a human-readable format
 */
export function formatDateTime(date: Date, timezone?: string): string {
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    timeZone: timezone || undefined,
  })
}

/**
 * Format a date into a short format
 */
export function formatDate(date: Date): string {
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

/**
 * Format a duration in milliseconds to a human-readable format
 */
export function formatDuration(durationMs: number): string {
  if (durationMs < 1000) {
    return `${durationMs}ms`
  }

  const seconds = Math.floor(durationMs / 1000)
  if (seconds < 60) {
    return `${seconds}s`
  }

  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  if (minutes < 60) {
    return `${minutes}m ${remainingSeconds}s`
  }

  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return `${hours}h ${remainingMinutes}m`
}

/**
 * Validates a name by removing any characters that could cause issues
 */
export function validateName(name: string): string {
  return name
    .replace(/[^a-zA-Z0-9_\s]/g, '')
    .replace(/\s+/g, ' ')
}

/**
 * Generate a short request ID
 */
export function generateRequestId(): string {
  return crypto.randomUUID().slice(0, 8)
}

export const noop = () => {}

/**
 * Redacts API keys from a string (placeholder).
 */
export function redactApiKeys(str: string): string {
  // In a real implementation, this would find and replace API keys.
  return str;
}
