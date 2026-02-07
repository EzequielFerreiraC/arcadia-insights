import { cn } from '@/lib/utils'

export function Card({
  className,
  children,
}: {
  className?: string
  children: React.ReactNode
}) {
  return <div className={cn('surface', className)}>{children}</div>
}

export function CardHeader({
  title,
  icon: Icon,
  action,
}: {
  title: string
  icon?: React.ComponentType<{ className?: string }>
  action?: React.ReactNode
}) {
  return (
    <div className="flex items-center justify-between border-b border-line px-6 py-4">
      <div className="flex items-center gap-2.5">
        {Icon && <Icon className="h-4 w-4 text-content-faint" />}
        <h2 className="text-sm font-semibold">{title}</h2>
      </div>
      {action}
    </div>
  )
}

export function CardBody({
  className,
  children,
}: {
  className?: string
  children: React.ReactNode
}) {
  return <div className={cn('p-6', className)}>{children}</div>
}
