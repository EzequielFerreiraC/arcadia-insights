import { cn } from '@/lib/utils'
import { accentChip } from '@/lib/accents'
import type { Accent } from '@/types'

export function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  accent = 'teal',
  className,
}: {
  icon: React.ComponentType<{ className?: string }>
  label: string
  value: string | number
  hint?: string
  accent?: Accent
  className?: string
}) {
  return (
    <div className={cn('surface p-5', className)}>
      <div className={cn('inline-flex h-9 w-9 items-center justify-center rounded-lg border', accentChip[accent])}>
        <Icon className="h-[18px] w-[18px]" />
      </div>
      <p className="mt-4 font-display text-3xl font-medium tracking-tight sm:text-4xl">{value}</p>
      <p className="mt-1 text-sm text-content-tertiary">{label}</p>
      {hint && <p className="mt-2 text-2xs text-content-faint">{hint}</p>}
    </div>
  )
}
