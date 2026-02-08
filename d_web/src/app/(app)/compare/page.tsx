'use client'

import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Check, GitCompareArrows, Minus, Users } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { NoPlayer } from '@/components/ui/NoPlayer'
import { analyticsApi, type CompareRow } from '@/lib/api'
import { getCurrentPlayerId } from '@/lib/currentPlayer'
import { cn } from '@/lib/utils'

/** Turn a raw option key (e.g. "nao_regar") into a readable label. */
function humanizeOption(option: string): string {
  return option.replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase())
}

export default function ComparePage() {
  const [pid, setPid] = useState<string | null>(null)
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    setPid(getCurrentPlayerId())
    setChecked(true)
  }, [])

  const { data } = useQuery({
    queryKey: ['analytics', 'compare', pid],
    queryFn: () => analyticsApi.playerCompare(pid!),
    enabled: !!pid,
    retry: 2,
  })

  if (checked && !pid) {
    return (
      <div className="space-y-8">
        <PageHeader
          eyebrow="Meu jogo"
          title="Comparação com a Comunidade"
          description="Cada decisão sua lado a lado com o percentual global de todos os jogadores."
        />
        <NoPlayer message="Envie um save para comparar as suas escolhas com a comunidade." />
      </div>
    )
  }

  const rows: CompareRow[] = data ?? []
  const aligned = rows.filter((r) => r.community_pct >= 50).length
  const compatibility =
    rows.length > 0 ? Math.round(rows.reduce((s, r) => s + r.community_pct, 0) / rows.length) : 0

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Meu jogo"
        title="Comparação com a Comunidade"
        description="Cada decisão sua lado a lado com o percentual global de todos os jogadores."
      />

      {/* Summary */}
      <div className="grid gap-4 sm:grid-cols-3">
        <SummaryCard icon={GitCompareArrows} accent="teal" value={`${compatibility}%`} label="Compatibilidade média" />
        <SummaryCard icon={Users} accent="sky" value={`${aligned}/${rows.length}`} label="Escolhas com a maioria" />
        <SummaryCard icon={Minus} accent="sunset" value={rows.length - aligned} label="Escolhas contra a maioria" />
      </div>

      {/* Comparison table */}
      <Card className="overflow-hidden">
        <CardHeader title="Suas escolhas vs. comunidade" icon={GitCompareArrows} />
        <div className="hidden grid-cols-[1fr_140px_1fr] gap-4 border-b border-line px-6 py-3 text-2xs font-semibold uppercase tracking-[0.12em] text-content-faint sm:grid">
          <span>Escolha</span>
          <span>Sua opção</span>
          <span>Comunidade</span>
        </div>
        {rows.length === 0 ? (
          <div className="px-6 py-12 text-center text-sm text-content-tertiary">
            Envie um save para ver sua comparação com a comunidade.
          </div>
        ) : (
          <div className="divide-y divide-line">
            {rows.map((row) => (
              <CompareItem key={row.choice_id} row={row} />
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}

function SummaryCard({
  icon: Icon,
  accent,
  value,
  label,
}: {
  icon: typeof Users
  accent: 'teal' | 'sky' | 'sunset'
  value: string | number
  label: string
}) {
  const chip =
    accent === 'teal'
      ? 'border-teal/25 bg-teal/10 text-teal'
      : accent === 'sky'
        ? 'border-sky/25 bg-sky/10 text-sky'
        : 'border-sunset/25 bg-sunset/10 text-sunset'
  return (
    <Card>
      <CardBody className="flex items-center gap-4">
        <div className={cn('flex h-10 w-10 items-center justify-center rounded-lg border', chip)}>
          <Icon className="h-5 w-5" />
        </div>
        <div>
          <p className="font-display text-2xl font-medium tracking-tight">{value}</p>
          <p className="text-2xs text-content-tertiary">{label}</p>
        </div>
      </CardBody>
    </Card>
  )
}

function CompareItem({ row }: { row: CompareRow }) {
  const aligned = row.community_pct >= 50
  return (
    <div className="grid grid-cols-1 items-center gap-3 px-6 py-4 sm:grid-cols-[1fr_140px_1fr] sm:gap-4">
      <div className="min-w-0">
        <p className="truncate text-sm font-medium">{row.choice_text}</p>
        <p className="text-2xs text-content-faint">Episódio {row.episode}</p>
      </div>

      <div className="flex sm:justify-start">
        <span className="inline-flex items-center gap-1.5 rounded-md border border-line bg-white/[0.03] px-2.5 py-1 text-2xs font-medium text-content-secondary">
          {humanizeOption(row.option_selected)}
        </span>
      </div>

      <div className="flex items-center gap-3">
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/[0.05]">
          <div
            className={cn('h-full rounded-full', aligned ? 'bg-teal' : 'bg-amber')}
            style={{ width: `${row.community_pct}%` }}
          />
        </div>
        <span className="w-12 shrink-0 text-right text-sm tabular-nums text-content-secondary">
          {Math.round(row.community_pct)}%
        </span>
        {aligned ? (
          <Check className="h-4 w-4 shrink-0 text-teal" />
        ) : (
          <Minus className="h-4 w-4 shrink-0 text-content-faint" />
        )}
      </div>
    </div>
  )
}
