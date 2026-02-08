'use client'

import { useQuery } from '@tanstack/react-query'
import { Activity, AlertTriangle, CheckCircle2, Gauge, Zap } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { StatCard } from '@/components/ui/StatCard'
import { TrendChart } from '@/components/charts/TrendChart'
import { ColumnChart } from '@/components/charts/ColumnChart'
import { platformApi } from '@/lib/api'
import { eventsTrend, observability as mockObs } from '@/lib/mock'
import { formatCompact, formatNumber } from '@/lib/format'

const jobsByHour = [
  { hour: '00h', jobs: 42 },
  { hour: '04h', jobs: 88 },
  { hour: '08h', jobs: 64 },
  { hour: '12h', jobs: 112 },
  { hour: '16h', jobs: 96 },
  { hour: '20h', jobs: 74 },
]

export default function ObservabilityPage() {
  const { data } = useQuery({
    queryKey: ['platform', 'observability'],
    queryFn: () => platformApi.observability(),
    retry: 2,
    refetchInterval: 10000,
  })

  const obs = data
    ? {
        throughputPerMin: data.throughput_per_min,
        eventsLastHour: data.events_last_hour,
        jobsExecuted24h: data.jobs_executed_24h,
        failures24h: data.failures_24h,
        successRate: data.success_rate,
      }
    : mockObs

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Dados & plataforma"
        title="Observabilidade"
        description="Métricas de sistema, throughput e execução de jobs — alimentado por Prometheus e Grafana."
        icon={Activity}
        actions={
          <a
            href="http://localhost:3001"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary h-9 text-[13px]"
          >
            Abrir Grafana
          </a>
        }
      />

      {/* Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard icon={Zap} label="Throughput" value={`${formatCompact(obs.throughputPerMin)}/min`} accent="teal" />
        <StatCard icon={Gauge} label="Eventos (última hora)" value={formatCompact(obs.eventsLastHour)} accent="amber" />
        <StatCard icon={CheckCircle2} label="Jobs executados (24h)" value={formatNumber(obs.jobsExecuted24h)} accent="sky" />
        <StatCard icon={AlertTriangle} label="Falhas (24h)" value={obs.failures24h} hint={`Taxa de sucesso ${obs.successRate}%`} accent="sunset" />
      </div>

      {/* Charts */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Eventos por período" icon={Activity} />
          <CardBody>
            <TrendChart data={eventsTrend} xKey="date" yKey="events" accent="teal" />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Jobs executados por hora" icon={CheckCircle2} />
          <CardBody>
            <ColumnChart data={jobsByHour} xKey="hour" yKey="jobs" accent="sky" />
          </CardBody>
        </Card>
      </div>

      {/* Success rate bar */}
      <Card>
        <CardHeader title="Taxa de sucesso do processamento" icon={Gauge} />
        <CardBody>
          <div className="flex items-center gap-4">
            <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-white/[0.05]">
              <div className="h-full rounded-full bg-teal" style={{ width: `${obs.successRate}%` }} />
            </div>
            <span className="font-display text-2xl font-medium tabular-nums text-teal">{obs.successRate}%</span>
          </div>
          <p className="mt-3 text-2xs text-content-faint">
            {obs.failures24h} falhas em {formatNumber(obs.jobsExecuted24h)} jobs nas últimas 24 horas.
          </p>
        </CardBody>
      </Card>
    </div>
  )
}
