'use client'

import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Info, Sparkles } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { NoPlayer } from '@/components/ui/NoPlayer'
import { mlApi } from '@/lib/api'
import { getCurrentPlayerId } from '@/lib/currentPlayer'
import { endingFactors as mockFactors, endingPredictions as mockPredictions } from '@/lib/mock'
import { accentBar, accentChip } from '@/lib/accents'
import { cn } from '@/lib/utils'
import type { Accent } from '@/types'

const ease = [0.22, 1, 0.36, 1] as const
const ENDING_ACCENT: Accent[] = ['sunset', 'sky', 'amber', 'teal']

export default function PredictionPage() {
  const [pid, setPid] = useState<string | null>(null)
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    setPid(getCurrentPlayerId())
    setChecked(true)
  }, [])

  const { data } = useQuery({
    queryKey: ['ml', 'prediction', pid],
    queryFn: () => mlApi.prediction(pid!),
    enabled: !!pid,
    retry: 2,
  })

  if (checked && !pid) {
    return (
      <div className="space-y-8">
        <PageHeader
          eyebrow="Meu jogo"
          title="Predição de Final"
          description="O modelo estima qual final você tende a escolher com base no seu padrão de decisões."
          icon={Sparkles}
        />
        <NoPlayer message="Envie um save para o modelo prever o seu final." />
      </div>
    )
  }

  const predictions = data
    ? data.predictions.map((p, i) => ({ ending: p.ending, probability: p.probability, accent: ENDING_ACCENT[i % ENDING_ACCENT.length] }))
    : mockPredictions
  const factors = data ? data.factors : mockFactors
  const top = predictions[0]

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Meu jogo"
        title="Predição de Final"
        description="O modelo estima qual final você tende a escolher com base no seu padrão de decisões."
        icon={Sparkles}
      />

      {/* Headline prediction */}
      <Card className="overflow-hidden">
        <div className="relative p-8 text-center">
          <div aria-hidden className="pointer-events-none absolute inset-0">
            <div className="absolute left-1/2 top-0 h-full w-[520px] -translate-x-1/2 bg-[radial-gradient(ellipse_at_top,rgba(224,122,95,0.16),transparent_65%)]" />
          </div>
          <div className="relative">
            <p className="text-2xs uppercase tracking-[0.14em] text-content-faint">Final mais provável</p>
            <p className="mt-3 font-display text-3xl font-medium tracking-tight sm:text-4xl">{top.ending}</p>
            <p className="mt-2 font-display text-5xl font-medium tracking-tightest text-sunset">{top.probability}%</p>
          </div>
        </div>
      </Card>

      {/* Probabilities */}
      <Card>
        <CardHeader title="Probabilidade por final" icon={Sparkles} />
        <CardBody className="space-y-5">
          {predictions.map((e, i) => (
            <div key={e.ending} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">{e.ending}</span>
                <span className="tabular-nums text-content-secondary">{e.probability}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-white/[0.05]">
                <motion.div
                  initial={{ width: 0 }}
                  whileInView={{ width: `${e.probability}%` }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.8, ease, delay: i * 0.1 }}
                  className={cn('h-full rounded-full', accentBar[e.accent])}
                />
              </div>
            </div>
          ))}
        </CardBody>
      </Card>

      {/* Explanation */}
      <Card>
        <CardHeader title="Como o modelo chegou a essa previsão" icon={Info} />
        <CardBody className="space-y-3">
          {factors.map((f) => (
            <div key={f.factor} className="flex items-center justify-between gap-4 rounded-lg border border-line bg-bg px-4 py-3">
              <p className="text-sm">{f.factor}</p>
              <div className="flex items-center gap-2">
                <span className={cn('rounded-md border px-2 py-0.5 text-2xs font-medium', weightChip(f.weight))}>
                  peso {f.weight}
                </span>
                <span className="text-2xs text-content-faint">→ {f.direction}</span>
              </div>
            </div>
          ))}
          <p className="pt-1 text-2xs text-content-faint">
            Modelo: Random Forest treinado sobre o histórico de escolhas · atualizado via pipeline de ML.
          </p>
        </CardBody>
      </Card>
    </div>
  )
}

function weightChip(weight: string): string {
  if (weight === 'alto') return accentChip.sunset
  if (weight === 'médio') return accentChip.amber
  return accentChip.sky
}
