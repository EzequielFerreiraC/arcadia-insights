'use client'

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Users } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { analyticsApi, type TimelineRow } from '@/lib/api'
import { timeline as mockTimeline } from '@/lib/mock'

const ease = [0.22, 1, 0.36, 1] as const

const EPISODE_TITLES: Record<number, string> = {
  1: 'Chrysalis',
  2: 'Out of Time',
  3: 'Chaos Theory',
  4: 'Dark Room',
  5: 'Polarized',
}

function humanizeOption(option: string): string {
  return option.replace(/_/g, ' ').replace(/^nao /, 'não ').replace(/^\w/, (c) => c.toUpperCase())
}

interface EpisodeGroup {
  episode: number
  title: string
  choices: { label: string; option: string; communityPct: number }[]
}

function groupRows(rows: TimelineRow[]): EpisodeGroup[] {
  const byEp = new Map<number, EpisodeGroup>()
  for (const r of rows) {
    if (!byEp.has(r.episode)) {
      byEp.set(r.episode, { episode: r.episode, title: EPISODE_TITLES[r.episode] ?? `Episódio ${r.episode}`, choices: [] })
    }
    byEp.get(r.episode)!.choices.push({
      label: r.choice_text,
      option: humanizeOption(r.option_selected),
      communityPct: r.community_pct,
    })
  }
  return Array.from(byEp.values()).sort((a, b) => a.episode - b.episode)
}

export default function TimelinePage() {
  const { data } = useQuery({
    queryKey: ['analytics', 'timeline'],
    queryFn: () => analyticsApi.timeline(),
    retry: 2,
  })

  const episodes: EpisodeGroup[] = data
    ? groupRows(data)
    : mockTimeline.map((ep) => ({
        episode: ep.episode,
        title: ep.title,
        choices: ep.choices.map((c) => ({ label: c.label, option: c.option, communityPct: c.communityPct })),
      }))

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Meu jogo"
        title="Timeline de Decisões"
        description="A jornada por Arcadia Bay, episódio por episódio, com a escolha da maioria em cada ponto de decisão."
      />

      <div className="relative">
        {/* vertical line */}
        <div aria-hidden className="absolute left-[19px] top-2 bottom-2 w-px bg-line-strong sm:left-[23px]" />

        <div className="space-y-8">
          {episodes.map((ep, i) => (
            <motion.section
              key={ep.episode}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ duration: 0.5, ease, delay: i * 0.05 }}
              className="relative pl-12 sm:pl-14"
            >
              <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-full border border-amber/25 bg-bg font-display text-sm font-semibold text-amber sm:h-12 sm:w-12">
                {ep.episode}
              </div>

              <div className="flex items-center gap-3">
                <h2 className="font-display text-xl font-medium tracking-tight">
                  Episódio {ep.episode} · {ep.title}
                </h2>
                <span className="text-2xs text-content-faint">{ep.choices.length} decisões</span>
              </div>

              <div className="mt-4 space-y-3">
                {ep.choices.map((c) => (
                  <Card key={c.label}>
                    <CardBody className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div className="min-w-0">
                        <p className="text-2xs uppercase tracking-[0.12em] text-content-faint">{c.label}</p>
                        <p className="mt-1 flex items-center gap-1.5 text-sm font-semibold">
                          <Users className="h-3.5 w-3.5 text-content-tertiary" />
                          Maioria: {c.option}
                        </p>
                      </div>
                      <Badge accent={c.communityPct >= 50 ? 'teal' : 'sunset'}>
                        {Math.round(c.communityPct)}% da comunidade
                      </Badge>
                    </CardBody>
                  </Card>
                ))}
              </div>
            </motion.section>
          ))}
        </div>
      </div>
    </div>
  )
}
