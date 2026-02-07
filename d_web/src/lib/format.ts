const decimal = new Intl.NumberFormat('pt-BR')
const compact = new Intl.NumberFormat('pt-BR', {
  notation: 'compact',
  maximumFractionDigits: 1,
})

export const formatNumber = (n: number): string => decimal.format(n)
export const formatCompact = (n: number): string => compact.format(n)
export const formatPercent = (n: number, digits = 0): string => `${n.toFixed(digits)}%`

export function formatDate(value: string | Date): string {
  const d = typeof value === 'string' ? new Date(value) : value
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
}

export function formatRelativeTime(value: string | Date): string {
  const d = typeof value === 'string' ? new Date(value) : value
  const diff = Date.now() - d.getTime()
  const mins = Math.round(diff / 60000)
  if (mins < 1) return 'agora'
  if (mins < 60) return `${mins} min atrás`
  const hours = Math.round(mins / 60)
  if (hours < 24) return `${hours} h atrás`
  const days = Math.round(hours / 24)
  return `${days} d atrás`
}
