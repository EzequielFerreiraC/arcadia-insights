'use client'

import { useQuery } from '@tanstack/react-query'
import { Users } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { mlApi } from '@/lib/api'
import { profiles as mockProfiles } from '@/lib/mock'
import { accentBar, accentChip } from '@/lib/accents'
import { formatCompact } from '@/lib/format'
import { cn } from '@/lib/utils'
import type { Accent } from '@/types'

const ACCENTS: Accent[] = ['teal', 'amber', 'sunset', 'sky']

export default function ProfilesPage() {
  const { data } = useQuery({
    queryKey: ['ml', 'profiles'],
    queryFn: () => mlApi.profiles(),
    retry: 2,
  })

  const profiles = data
    ? data.map((p, i) => ({
        name: p.name,
        description: p.description,
        players: p.players,
        occurrence: p.occurrence,
        typicalChoices: p.typical_choices,
        accent: ACCENTS[i % ACCENTS.length],
      }))
    : mockProfiles

  const totalPlayers = profiles.reduce((sum, p) => sum + p.players, 0)

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Comunidade"
        title="Perfis de Jogadores"
        description="Agrupamentos comportamentais gerados por clustering (K-Means) sobre os padrões de escolha."
        icon={Users}
      />

      <div className="grid gap-4 sm:grid-cols-2">
        {profiles.map((p) => (
          <Card key={p.name}>
            <CardBody className="space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className={cn('inline-flex h-10 w-10 items-center justify-center rounded-lg border', accentChip[p.accent])}>
                    <Users className="h-5 w-5" />
                  </div>
                  <h2 className="mt-3 font-display text-xl font-medium tracking-tight">{p.name}</h2>
                </div>
                <div className="text-right">
                  <p className="font-display text-2xl font-medium tracking-tight">{formatCompact(p.players)}</p>
                  <p className="text-2xs text-content-faint">jogadores</p>
                </div>
              </div>

              <p className="text-sm leading-relaxed text-content-secondary">{p.description}</p>

              <div>
                <div className="flex items-center justify-between text-2xs text-content-tertiary">
                  <span>Taxa de ocorrência</span>
                  <span className="tabular-nums">{p.occurrence}%</span>
                </div>
                <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-white/[0.05]">
                  <div className={cn('h-full rounded-full', accentBar[p.accent])} style={{ width: `${p.occurrence}%` }} />
                </div>
              </div>

              <div>
                <p className="mb-2 text-2xs uppercase tracking-[0.12em] text-content-faint">Escolhas típicas</p>
                <div className="flex flex-wrap gap-1.5">
                  {p.typicalChoices.map((c) => (
                    <Badge key={c} accent={p.accent}>{c}</Badge>
                  ))}
                </div>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>

      <p className="text-2xs text-content-faint">
        Total segmentado: {formatCompact(totalPlayers)} jogadores · modelo K-Means re-treinado sob demanda.
      </p>
    </div>
  )
}
