import { cn } from '@/lib/utils'
import { accentBar } from '@/lib/accents'
import type { Accent } from '@/types'

/** A labelled horizontal bar with value + percentage — the workhorse chart. */
export function BarRow({
  label,
  value,
  total = 100,
  suffix,
  accent = 'teal',
  animate = true,
}: {
  label: string
  value: number
  total?: number
  suffix?: string
  accent?: Accent
  animate?: boolean
}) {
  const pct = Math.min(100, Math.round((value / total) * 100))
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-content-secondary">{label}</span>
        <span className="tabular-nums text-content-tertiary">{suffix ?? `${pct}%`}</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-white/[0.05]">
        <div
          className={cn('h-full rounded-full transition-[width] duration-700 ease-out', accentBar[accent])}
          style={{ width: animate ? `${pct}%` : `${pct}%` }}
        />
      </div>
    </div>
  )
}

export function BarList({
  items,
  accent = 'teal',
}: {
  items: Array<{ label: string; value: number; suffix?: string }>
  accent?: Accent
}) {
  return (
    <div className="space-y-4">
      {items.map((it) => (
        <BarRow key={it.label} label={it.label} value={it.value} suffix={it.suffix} accent={accent} />
      ))}
    </div>
  )
}
