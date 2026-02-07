import { cn } from '@/lib/utils'

export function EmptyState({
  icon: Icon,
  title,
  message,
  action,
  className,
}: {
  icon?: React.ComponentType<{ className?: string }>
  title?: string
  message: string
  action?: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn('flex flex-col items-center gap-3 py-10 text-center', className)}>
      {Icon && (
        <div className="flex h-11 w-11 items-center justify-center rounded-full border border-line bg-white/[0.02]">
          <Icon className="h-5 w-5 text-content-faint" />
        </div>
      )}
      {title && <h3 className="text-sm font-medium text-content-secondary">{title}</h3>}
      <p className="max-w-sm text-sm text-content-tertiary">{message}</p>
      {action}
    </div>
  )
}
