'use client'

import { useQuery } from '@tanstack/react-query'
import { Crown, Trophy } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { analyticsApi } from '@/lib/api'
import { leaderboard as mockLeaderboard } from '@/lib/mock'
import { cn } from '@/lib/utils'

interface Entry {
  rank: number
  name: string
  handle: string
  avgRarity: number
  rareCount: number
}

const FLAG: Record<string, string> = {
  BR: 'Brasil', US: 'EUA', GB: 'Reino Unido', FR: 'França', DE: 'Alemanha',
  JP: 'Japão', CA: 'Canadá', AU: 'Austrália', PT: 'Portugal', ES: 'Espanha',
  MX: 'México', IT: 'Itália',
}

export default function LeaderboardPage() {
  const { data } = useQuery({
    queryKey: ['analytics', 'leaderboard'],
    queryFn: () => analyticsApi.leaderboard(10),
    retry: 2,
  })

  const entries: Entry[] = data
    ? data.map((e, i) => ({
        rank: i + 1,
        name: `${FLAG[e.country] ?? e.country} · ${e.player_id.slice(0, 4)}`,
        handle: `@${e.player_id.slice(0, 8)}`,
        avgRarity: Math.round(e.avg_rarity),
        rareCount: e.rare_count,
      }))
    : mockLeaderboard

  const [first, ...rest] = entries

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Comunidade"
        title="Leaderboard de Escolhas Raras"
        description="Quem toma as decisões mais incomuns de Arcadia Bay. Quanto mais raro, mais alto o ranking."
        icon={Trophy}
      />

      {/* Champion */}
      {first && (
      <Card className="overflow-hidden">
        <div className="relative flex items-center gap-5 p-6">
          <div aria-hidden className="pointer-events-none absolute inset-0">
            <div className="absolute left-0 top-0 h-full w-1/2 bg-[radial-gradient(ellipse_at_left,rgba(240,169,78,0.16),transparent_70%)]" />
          </div>
          <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl border border-amber/30 bg-amber/10 text-amber">
            <Crown className="h-8 w-8" />
          </div>
          <div className="relative flex-1">
            <p className="text-2xs uppercase tracking-[0.14em] text-content-faint">1º lugar</p>
            <p className="mt-1 font-display text-2xl font-medium tracking-tight">{first.name}</p>
            <p className="text-sm text-content-faint">{first.handle}</p>
          </div>
          <div className="relative text-right">
            <p className="font-display text-4xl font-medium tracking-tightest text-amber">{first.avgRarity}%</p>
            <p className="text-2xs text-content-tertiary">raridade média</p>
          </div>
        </div>
      </Card>
      )}

      {/* Rest */}
      <Card className="overflow-hidden">
        <CardHeader title="Ranking geral" />
        <div className="divide-y divide-line">
          {rest.map((entry) => (
            <div key={entry.rank} className="flex items-center gap-4 px-6 py-4">
              <span
                className={cn(
                  'flex h-8 w-8 shrink-0 items-center justify-center rounded-full border font-display text-sm font-semibold',
                  entry.rank <= 3 ? 'border-amber/25 bg-amber/10 text-amber' : 'border-line bg-white/[0.02] text-content-tertiary',
                )}
              >
                {entry.rank}
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium">{entry.name}</p>
                <p className="text-2xs text-content-faint">{entry.handle} · {entry.rareCount} escolhas raras</p>
              </div>
              <div className="text-right">
                <p className="font-display text-lg font-medium tabular-nums">{entry.avgRarity}%</p>
                <p className="text-2xs text-content-faint">raridade</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
