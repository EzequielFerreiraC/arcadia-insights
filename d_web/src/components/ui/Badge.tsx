import { cn } from '@/lib/utils'
import { accentChip } from '@/lib/accents'
import type { Accent } from '@/types'

export function Badge({
  children,
  accent = 'teal',
  className,
}: {
  children: React.ReactNode
  accent?: Accent
  className?: string
}) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 text-2xs font-medium',
        accentChip[accent],
        className,
      )}
    >
      {children}
    </span>
  )
}
