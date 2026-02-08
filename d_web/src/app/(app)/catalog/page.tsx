'use client'

import { useQuery } from '@tanstack/react-query'
import { Database, GitBranch, Layers, Timer, Workflow } from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { StatCard } from '@/components/ui/StatCard'
import { StatusPill } from '@/components/ui/StatusPill'
import { Badge } from '@/components/ui/Badge'
import { platformApi } from '@/lib/api'
import { catalogMetrics as mockMetrics, catalogTables as mockTables, pipelineHealth as mockPipes } from '@/lib/mock'
import { formatCompact, formatNumber, formatRelativeTime } from '@/lib/format'
import type { Accent } from '@/types'

const layerAccent: Record<string, Accent> = {
  Bronze: 'sunset',
  Silver: 'sky',
  Gold: 'amber',
}

export default function CatalogPage() {
  const { data } = useQuery({
    queryKey: ['platform', 'catalog'],
    queryFn: () => platformApi.catalog(),
    retry: 2,
    refetchInterval: 15000,
  })

  const metrics = data
    ? {
        totalRecords: data.metrics.total_records,
        eventsProcessed24h: data.metrics.events_processed_24h,
        avgPipelineLatencyMs: data.metrics.avg_pipeline_latency_ms,
        dataLakePartitions: data.metrics.data_lake_partitions,
      }
    : mockMetrics

  const tables = data?.tables ?? mockTables.map((t) => ({ ...t, updated: t.updated }))
  const pipelines = data?.pipelines ?? mockPipes

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Dados & plataforma"
        title="Data Catalog"
        description="Inventário das tabelas do data lake medallion e a saúde dos pipelines que as alimentam."
        icon={Database}
      />

      {/* Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard icon={Layers} label="Registros totais" value={formatCompact(metrics.totalRecords)} accent="teal" />
        <StatCard icon={Workflow} label="Eventos (24h)" value={formatCompact(metrics.eventsProcessed24h)} accent="amber" />
        <StatCard icon={Timer} label="Latência média" value={`${metrics.avgPipelineLatencyMs} ms`} accent="sky" />
        <StatCard icon={GitBranch} label="Partições do lake" value={metrics.dataLakePartitions} accent="sunset" />
      </div>

      {/* Pipeline health */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {pipelines.map((p) => (
          <Card key={p.name}>
            <CardBody className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold">{p.name}</h3>
                <StatusPill status={p.status} pulse={p.status === 'healthy'} />
              </div>
              <p className="text-2xs text-content-tertiary">{p.detail}</p>
              <p className="font-mono text-2xs text-content-faint">{p.metric}</p>
            </CardBody>
          </Card>
        ))}
      </div>

      {/* Tables */}
      <Card className="overflow-hidden">
        <CardHeader title="Tabelas do data lake" icon={Database} />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-line text-2xs uppercase tracking-[0.12em] text-content-faint">
                <th className="px-6 py-3 font-semibold">Tabela</th>
                <th className="px-6 py-3 font-semibold">Camada</th>
                <th className="px-6 py-3 font-semibold">Registros</th>
                <th className="px-6 py-3 font-semibold">Formato</th>
                <th className="px-6 py-3 font-semibold">Partições</th>
                <th className="px-6 py-3 font-semibold">Atualizado</th>
              </tr>
            </thead>
            <tbody>
              {tables.map((t) => (
                <tr key={t.name} className="border-b border-line/60 transition-colors hover:bg-white/[0.02]">
                  <td className="px-6 py-3.5 font-mono text-[13px]">{t.name}</td>
                  <td className="px-6 py-3.5"><Badge accent={layerAccent[t.layer] ?? 'teal'}>{t.layer}</Badge></td>
                  <td className="px-6 py-3.5 tabular-nums text-content-secondary">{formatNumber(t.rows)}</td>
                  <td className="px-6 py-3.5 text-content-secondary">{t.format}</td>
                  <td className="px-6 py-3.5 tabular-nums text-content-tertiary">{t.partitions}</td>
                  <td className="px-6 py-3.5 text-content-tertiary">{t.updated ? formatRelativeTime(t.updated) : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
