'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  Award, GitCompareArrows, Heart, Layers, ListChecks, Sparkles, TrendingDown, TrendingUp,
} from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { NoPlayer } from '@/components/ui/NoPlayer'
import { analyticsApi } from '@/lib/api'
import { getCurrentPlayerId } from '@/lib/currentPlayer'
import { myPlayer } from '@/lib/mock'
import type { RankedChoice } from '@/types'

const ease = [0.22, 1, 0.36, 1] as const

/** Derive a friendly archetype label from the community-agreement score. */
function archetypeFor(compatibility: number): string {
  if (compatibility >= 65) return 'Empático'
  if (compatibility >= 45) return 'Diplomático'
  if (compatibility >= 30) return 'Impulsivo'
  return 'Utilitarista'
}

const ARCHETYPE_DESCRIPTIONS: Record<string, string> = {
  Empático: 'Prioriza o bem-estar das pessoas ao redor, mesmo quando isso traz consequências pessoais.',
  Diplomático: 'Evita conflito e busca o equilíbrio, negociando as decisões difíceis.',
  Impulsivo: 'Decide guiado pela emoção e pelo instinto do momento.',
  Utilitarista: 'Busca o maior benefício coletivo, mesmo com um custo pessoal alto.',
}

export default function MyDashboardPage() {
  const [pid, setPid] = useState<string | null>(null)
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    setPid(getCurrentPlayerId())
    setChecked(true)
  }, [])

  const { data } = useQuery({
    queryKey: ['analytics', 'summary', pid],
    queryFn: () => analyticsApi.playerSummary(pid!),
    enabled: !!pid,
    retry: 2,
  })

  if (checked && !pid) {
    return (
      <div className="space-y-8">
        <PageHeader
          eyebrow="Meu jogo"
          title="Meu Dashboard"
          description="Sua jornada em Arcadia Bay comparada a milhares de outros jogadores."
        />
        <NoPlayer />
      </div>
    )
  }

  const compatibility = data?.compatibility ?? myPlayer.compatibility
  const archetype = data ? archetypeFor(compatibility) : myPlayer.archetype
  const view = {
    name: data && pid ? `Jogador ${pid.slice(0, 4).toUpperCase()}` : myPlayer.name,
    handle: pid ? `@${pid.slice(0, 8)}` : myPlayer.handle,
    archetype,
    archetypeDescription: ARCHETYPE_DESCRIPTIONS[archetype] ?? myPlayer.archetypeDescription,
    compatibility,
    ending: data?.ending ?? myPlayer.ending,
    totalChoices: data?.total_choices ?? myPlayer.totalChoices,
    completedEpisodes: data?.completed_episodes ?? myPlayer.completedEpisodes,
    rareChoices: data?.rare_choices ?? myPlayer.rareChoices,
    popularChoices: data?.popular_choices ?? myPlayer.popularChoices,
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Meu jogo"
        title="Meu Dashboard"
        description="Sua jornada em Arcadia Bay comparada a milhares de outros jogadores."
        actions={
          <Link href="/compare" className="btn-secondary h-9 text-[13px]">
            <GitCompareArrows className="h-4 w-4" />
            Comparar
          </Link>
        }
      />

      {/* Profile + compatibility */}
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardBody className="flex flex-col gap-5 sm:flex-row sm:items-center">
            <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border border-amber/25 bg-amber/10 font-display text-2xl font-medium text-amber">
              {view.name.split(' ').map((w) => w[0]).join('').slice(0, 2)}
            </div>
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="font-display text-2xl font-medium tracking-tight">{view.name}</h2>
                <span className="text-sm text-content-faint">{view.handle}</span>
              </div>
              <div className="mt-2 flex items-center gap-2">
                <Badge accent="teal">
                  <Heart className="h-3 w-3" /> Perfil {view.archetype}
                </Badge>
                <span className="text-2xs text-content-faint">definido por clustering</span>
              </div>
              <p className="mt-3 max-w-md text-sm leading-relaxed text-content-secondary">
                {view.archetypeDescription}
              </p>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="flex h-full flex-col items-center justify-center text-center">
            <CompatibilityRing value={view.compatibility} />
            <p className="mt-4 text-sm text-content-secondary">Compatibilidade com a comunidade</p>
          </CardBody>
        </Card>
      </div>

      {/* Summary stats */}
      <div className="grid gap-4 sm:grid-cols-3">
        <SummaryStat icon={ListChecks} label="Escolhas registradas" value={view.totalChoices} />
        <SummaryStat icon={Layers} label="Episódios concluídos" value={`${view.completedEpisodes}/5`} />
        <SummaryStat icon={Award} label="Escolhas raras" value={view.rareChoices.length} />
      </div>

      {/* Ending */}
      <Card className="overflow-hidden">
        <div className="relative flex items-center gap-4 p-6">
          <div aria-hidden className="pointer-events-none absolute inset-0">
            <div className="absolute right-0 top-0 h-full w-1/2 bg-[radial-gradient(ellipse_at_right,rgba(224,122,95,0.14),transparent_70%)]" />
          </div>
          <div className="relative flex h-11 w-11 items-center justify-center rounded-lg border border-sunset/25 bg-sunset/10 text-sunset">
            <Sparkles className="h-5 w-5" />
          </div>
          <div className="relative">
            <p className="text-2xs uppercase tracking-[0.14em] text-content-faint">Final obtido</p>
            <p className="mt-1 font-display text-xl font-medium tracking-tight">{view.ending}</p>
          </div>
        </div>
      </Card>

      {/* Rare + popular choices */}
      <div className="grid gap-4 lg:grid-cols-2">
        <ChoicesCard
          title="Suas escolhas mais raras"
          icon={TrendingDown}
          choices={view.rareChoices}
          accent="sunset"
        />
        <ChoicesCard
          title="Suas escolhas mais populares"
          icon={TrendingUp}
          choices={view.popularChoices}
          accent="teal"
        />
      </div>
    </div>
  )
}

function CompatibilityRing({ value }: { value: number }) {
  const r = 46
  const c = 2 * Math.PI * r
  return (
    <div className="relative h-32 w-32">
      <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
        <circle cx="60" cy="60" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10" />
        <motion.circle
          cx="60"
          cy="60"
          r={r}
          fill="none"
          stroke="#4ECDC4"
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: c - (c * value) / 100 }}
          transition={{ duration: 1, ease }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="font-display text-3xl font-medium tracking-tight">{value}%</span>
      </div>
    </div>
  )
}

function SummaryStat({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof ListChecks
  label: string
  value: string | number
}) {
  return (
    <Card>
      <CardBody className="flex items-center gap-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-line bg-white/[0.02] text-content-secondary">
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

function ChoicesCard({
  title,
  icon: Icon,
  choices,
  accent,
}: {
  title: string
  icon: typeof TrendingUp
  choices: RankedChoice[]
  accent: 'teal' | 'sunset'
}) {
  return (
    <Card>
      <CardHeader title={title} icon={Icon} />
      <CardBody className="space-y-3">
        {choices.map((c) => (
          <div key={c.label} className="flex items-center justify-between gap-4 rounded-lg border border-line bg-bg px-4 py-3">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium">{c.label}</p>
              <p className="text-2xs text-content-faint">Episódio {c.episode}</p>
            </div>
            <Badge accent={accent}>{c.pct}% dos jogadores</Badge>
          </div>
        ))}
      </CardBody>
    </Card>
  )
}
