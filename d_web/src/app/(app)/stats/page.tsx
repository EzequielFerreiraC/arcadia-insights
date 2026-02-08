'use client'

import { useQuery } from '@tanstack/react-query'
import { BarChart3, Gamepad2, LineChart, ThumbsDown, ThumbsUp, TrendingUp } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { StatCard } from '@/components/ui/StatCard'
import { BarList } from '@/components/ui/BarList'
import { ColumnChart } from '@/components/charts/ColumnChart'
import { DonutChart } from '@/components/charts/DonutChart'
import { TrendChart } from '@/components/charts/TrendChart'
import { analyticsApi } from '@/lib/api'
import {
  episodeDistribution as mockEpisodes, eventsTrend, gameDistribution,
  globalStats as mockGlobal, leastPopular, mostPopular,
} from '@/lib/mock'
import { formatCompact } from '@/lib/format'

export default function StatsPage() {
  const { data: global } = useQuery({ queryKey: ['analytics', 'global'], queryFn: () => analyticsApi.global(), retry: 2 })
  const { data: popular } = useQuery({ queryKey: ['analytics', 'popular'], queryFn: () => analyticsApi.popularChoices(5), retry: 2 })
  const { data: rare } = useQuery({ queryKey: ['analytics', 'rare'], queryFn: () => analyticsApi.rareChoices(5), retry: 2 })
  const { data: episodes } = useQuery({ queryKey: ['analytics', 'episodes'], queryFn: () => analyticsApi.episodeDistribution(), retry: 2 })

  const totalChoices = global ? formatCompact(global.total_choices) : formatCompact(mockGlobal.totalChoices)
  const totalPlayers = global ? formatCompact(global.total_players) : formatCompact(mockGlobal.totalPlayers)
  const commonPct = global ? `${Math.round(global.most_common_choice.pct)}%` : `${mockGlobal.mostCommonChoice.pct}%`
  const commonLabel = global ? global.most_common_choice.label : mockGlobal.mostCommonChoice.label
  const totalSaves = global ? formatCompact(global.total_saves) : formatCompact(mockGlobal.totalSaves)

  const popularItems = (popular ?? mostPopular).map((c) =>
    'choice_text' in c ? { label: c.choice_text, value: c.pct } : { label: c.label, value: c.pct },
  )
  const rareItems = (rare ?? leastPopular).map((c) =>
    'choice_text' in c ? { label: c.choice_text, value: c.pct } : { label: c.label, value: c.pct },
  )
  const episodeData = episodes ?? mockEpisodes

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Comunidade"
        title="Estatísticas Globais"
        description="Analytics agregados de todas as escolhas processadas na plataforma."
      />

      {/* KPIs */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard icon={BarChart3} label="Escolhas processadas" value={totalChoices} accent="teal" />
        <StatCard icon={TrendingUp} label="Jogadores analisados" value={totalPlayers} accent="amber" />
        <StatCard icon={ThumbsUp} label="Escolha mais comum" value={commonPct} hint={commonLabel} accent="sky" />
        <StatCard icon={Gamepad2} label="Saves recebidos" value={totalSaves} accent="sunset" />
      </div>

      {/* Popular vs unpopular */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Escolhas mais populares" icon={ThumbsUp} />
          <CardBody>
            <BarList accent="teal" items={popularItems} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Escolhas menos populares" icon={ThumbsDown} />
          <CardBody>
            <BarList accent="sunset" items={rareItems} />
          </CardBody>
        </Card>
      </div>

      {/* Distributions */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Distribuição por episódio" icon={BarChart3} />
          <CardBody>
            <ColumnChart data={episodeData} xKey="episode" yKey="choices" accent="amber" />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Distribuição por jogo" icon={Gamepad2} />
          <CardBody>
            <DonutChart data={gameDistribution} nameKey="game" valueKey="players" />
          </CardBody>
        </Card>
      </div>

      {/* Time series */}
      <Card>
        <CardHeader title="Eventos processados na semana" icon={LineChart} />
        <CardBody>
          <TrendChart data={eventsTrend} xKey="date" yKey="events" accent="teal" />
        </CardBody>
      </Card>
    </div>
  )
}
