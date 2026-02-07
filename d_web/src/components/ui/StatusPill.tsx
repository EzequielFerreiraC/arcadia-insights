import { cn } from '@/lib/utils'

type Status = 'healthy' | 'degraded' | 'down' | 'done' | 'processing' | 'failed' | 'queued' | 'online' | 'offline'

const styles: Record<Status, { dot: string; text: string; ring: string; label: string }> = {
  healthy: { dot: 'bg-teal', text: 'text-teal', ring: 'border-teal/25 bg-teal/10', label: 'Saudável' },
  online: { dot: 'bg-teal', text: 'text-teal', ring: 'border-teal/25 bg-teal/10', label: 'Online' },
  done: { dot: 'bg-teal', text: 'text-teal', ring: 'border-teal/25 bg-teal/10', label: 'Concluído' },
  processing: { dot: 'bg-amber', text: 'text-amber', ring: 'border-amber/25 bg-amber/10', label: 'Processando' },
  queued: { dot: 'bg-sky', text: 'text-sky', ring: 'border-sky/25 bg-sky/10', label: 'Na fila' },
  degraded: { dot: 'bg-amber', text: 'text-amber', ring: 'border-amber/25 bg-amber/10', label: 'Degradado' },
  failed: { dot: 'bg-sunset', text: 'text-sunset', ring: 'border-sunset/25 bg-sunset/10', label: 'Falhou' },
  down: { dot: 'bg-sunset', text: 'text-sunset', ring: 'border-sunset/25 bg-sunset/10', label: 'Offline' },
  offline: { dot: 'bg-sunset', text: 'text-sunset', ring: 'border-sunset/25 bg-sunset/10', label: 'Offline' },
}

export function StatusPill({
  status,
  label,
  pulse = false,
}: {
  status: Status
  label?: string
  pulse?: boolean
}) {
  const s = styles[status]
  return (
    <span className={cn('inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-2xs font-medium', s.ring, s.text)}>
      <span className={cn('h-1.5 w-1.5 rounded-full', s.dot, pulse && 'animate-pulse')} />
      {label ?? s.label}
    </span>
  )
}
