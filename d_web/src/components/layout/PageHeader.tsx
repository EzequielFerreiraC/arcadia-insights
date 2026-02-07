import { cn } from '@/lib/utils'

export function PageHeader({
  eyebrow,
  title,
  description,
  actions,
  icon: Icon,
  className,
}: {
  eyebrow?: string
  title: string
  description?: string
  actions?: React.ReactNode
  icon?: React.ComponentType<{ className?: string }>
  className?: string
}) {
  return (
    <div className={cn('flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between', className)}>
      <div>
        {eyebrow && <span className="eyebrow">{eyebrow}</span>}
        <h1 className="mt-2 flex items-center gap-2.5 font-display text-3xl font-medium tracking-tight">
          {Icon && <Icon className="h-7 w-7 text-amber" />}
          {title}
        </h1>
        {description && <p className="mt-1.5 max-w-2xl text-sm text-content-tertiary">{description}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  )
}

/** Smaller section title used within a page. */
export function SectionTitle({
  title,
  description,
  className,
}: {
  title: string
  description?: string
  className?: string
}) {
  return (
    <div className={className}>
      <h2 className="font-display text-xl font-medium tracking-tight">{title}</h2>
      {description && <p className="mt-1 text-sm text-content-tertiary">{description}</p>}
    </div>
  )
}
