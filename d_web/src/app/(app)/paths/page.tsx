'use client'

import { useQuery } from '@tanstack/react-query'
import { Route, TrendingDown, TrendingUp } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { analyticsApi } from '@/lib/api'
import { narrativePaths as mockPaths } from '@/lib/mock'
import { cn } from '@/lib/utils'

export default function PathsPage() {
  const { data } = useQuery({
    queryKey: ['analytics', 'paths'],
    queryFn: () => analyticsApi.paths(),
    retry: 2,
  })

  const all = data ?? mockPaths
  const frequent = all.filter((p) => p.frequency >= 50).sort((a, b) => b.frequency - a.frequency)
  const rare = all.filter((p) => p.frequency < 50).sort((a, b) => a.frequency - b.frequency)
  const highlight = frequent[0] ?? all[0]

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Comunidade"
        title="Análise de Caminhos"
        description="Rotas narrativas que emergem quando milhares de decisões são cruzadas."
      />

      {/* Highlight */}
      {highlight && (
        <Card className="overflow-hidden">
          <div className="relative p-8">
            <div aria-hidden className="pointer-events-none absolute inset-0">
              <div className="absolute left-0 top-0 h-full w-2/3 bg-[radial-gradient(ellipse_at_left,rgba(78,205,196,0.12),transparent_70%)]" />
            </div>
            <div className="relative flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-teal/25 bg-teal/10 text-teal">
                <Route className="h-6 w-6" />
              </div>
              <div>
                <p className="font-display text-2xl font-medium leading-snug tracking-tight sm:text-3xl">
                  {Math.round(highlight.frequency)}% dos jogadores
                </p>
                <p className="font-display text-lg font-medium leading-snug tracking-tight text-content-secondary sm:text-xl">
                  {highlight.detail}
                </p>
              </div>
            </div>
          </div>
        </Card>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Caminhos mais frequentes" icon={TrendingUp} />
          <CardBody className="space-y-3">
            {frequent.map((p) => (
              <PathRow key={p.label} label={p.label} detail={p.detail} frequency={p.frequency} tone="teal" />
            ))}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Caminhos raros" icon={TrendingDown} />
          <CardBody className="space-y-3">
            {rare.map((p) => (
              <PathRow key={p.label} label={p.label} detail={p.detail} frequency={p.frequency} tone="sunset" />
            ))}
          </CardBody>
        </Card>
      </div>
    </div>
  )
}

function PathRow({
  label,
  detail,
  frequency,
  tone,
}: {
  label: string
  detail: string
  frequency: number
  tone: 'teal' | 'sunset'
}) {
  return (
    <div className="rounded-lg border border-line bg-bg p-4">
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm font-semibold">{label}</p>
        <span className={cn('font-display text-lg font-medium tabular-nums', tone === 'teal' ? 'text-teal' : 'text-sunset')}>
          {Math.round(frequency)}%
        </span>
      </div>
      <p className="mt-1 text-2xs text-content-tertiary">{detail}</p>
      <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/[0.05]">
        <div
          className={cn('h-full rounded-full', tone === 'teal' ? 'bg-teal' : 'bg-sunset')}
          style={{ width: `${frequency}%` }}
        />
      </div>
    </div>
  )
}
