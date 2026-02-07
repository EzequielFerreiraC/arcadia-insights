import type { Accent } from '@/types'

/** Icon chip styles (border + tinted bg + text) per accent. */
export const accentChip: Record<Accent, string> = {
  teal: 'text-teal border-teal/25 bg-teal/10',
  amber: 'text-amber border-amber/25 bg-amber/10',
  sky: 'text-sky border-sky/25 bg-sky/10',
  sunset: 'text-sunset border-sunset/25 bg-sunset/10',
  violet: 'text-violet-soft border-violet/25 bg-violet/10',
}

/** Solid fill (bars, dots) per accent. */
export const accentBar: Record<Accent, string> = {
  teal: 'bg-teal',
  amber: 'bg-amber',
  sky: 'bg-sky',
  sunset: 'bg-sunset',
  violet: 'bg-violet',
}

/** Hex values for chart libraries. */
export const accentHex: Record<Accent, string> = {
  teal: '#4ECDC4',
  amber: '#f0a94e',
  sky: '#6db3d4',
  sunset: '#e07a5f',
  violet: '#8b5cf6',
}

export const chartPalette = ['#4ECDC4', '#f0a94e', '#6db3d4', '#e07a5f', '#8b5cf6']
