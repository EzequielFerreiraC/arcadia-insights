'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  ArrowRight, Boxes, Camera, Cpu, Database, GitBranch,
  LineChart, Radio, Sparkles, Upload, Workflow,
} from 'lucide-react'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import { Butterfly } from '@/components/brand/Logo'
import { analyticsApi } from '@/lib/api'
import { globalStats } from '@/lib/mock'
import { formatCompact } from '@/lib/format'

const ease = [0.22, 1, 0.36, 1] as const

const img = (id: string, w = 1200) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=80`

export default function HomePage() {
  const { data: g } = useQuery({
    queryKey: ['analytics', 'global'],
    queryFn: () => analyticsApi.global(),
    retry: 2,
  })

  const stats = [
    { value: g ? formatCompact(g.total_players) : formatCompact(globalStats.totalPlayers), label: 'Jogadores analisados' },
    { value: g ? formatCompact(g.total_choices) : formatCompact(globalStats.totalChoices), label: 'Escolhas processadas' },
    { value: g ? `${Math.round(g.most_common_choice.pct)}%` : `${globalStats.mostCommonChoice.pct}%`, label: 'Escolha mais comum' },
    { value: g ? formatCompact(g.total_saves) : formatCompact(globalStats.totalSaves), label: 'Saves recebidos' },
  ]

  return (
    <main className="relative overflow-clip">
      <Navbar />

      {/* ============ HERO ============ */}
      <section className="relative min-h-[92vh] overflow-hidden">
        {/* Atmospheric background — golden-hour Pacific coast */}
        <div aria-hidden className="absolute inset-0">
          <Image
            src="/images/life-is-strange-wallpaper.jpg"
            alt=""
            fill
            priority
            sizes="100vw"
            className="img-graded object-cover object-center"
          />
          <div className="absolute inset-0 golden-wash" />
          <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-bg" />
        </div>

        {/* Floating butterflies */}
        <Butterfly className="pointer-events-none absolute left-[8%] top-[26%] h-9 w-9 animate-flutter opacity-80 drop-shadow-[0_0_16px_rgba(78,205,196,0.5)]" />
        <Butterfly className="pointer-events-none absolute right-[12%] top-[38%] h-12 w-12 animate-float opacity-70 drop-shadow-[0_0_18px_rgba(109,179,212,0.5)] [animation-delay:-3s]" />

        <div className="container-page relative flex min-h-[92vh] flex-col justify-center pt-24 pb-28">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease }}
          >
            <span className="eyebrow rounded-full border border-amber/25 bg-amber/[0.06] px-3 py-1.5 backdrop-blur-sm">
              <span className="h-1.5 w-1.5 rounded-full bg-amber shadow-[0_0_10px] shadow-amber" />
              Choice Analytics Platform
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease, delay: 0.05 }}
            className="mt-6 max-w-4xl font-display text-5xl font-medium leading-[1.02] tracking-tightest text-content-primary sm:text-6xl md:text-[76px]"
          >
            Toda escolha<br className="hidden sm:block" /> conta em{' '}
            <span className="text-gradient italic">Arcadia Bay</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease, delay: 0.1 }}
            className="mt-6 max-w-xl text-pretty text-lg leading-relaxed text-content-secondary"
          >
            Arcadia Insights transforma as decisões de milhões de jogadores de{' '}
            <em className="text-content-primary not-italic">Life is Strange</em> em
            analytics — ingestão em tempo real, data lake em camadas e machine learning.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease, delay: 0.15 }}
            className="mt-9 flex flex-wrap items-center gap-3"
          >
            <Link href="/upload" className="btn-primary group h-11 px-6 text-[15px]">
              <Upload className="h-4 w-4" />
              Enviar Save
            </Link>
            <Link
              href="/dashboard"
              className="btn-secondary h-11 px-6 text-[15px] backdrop-blur-sm"
            >
              Explorar dashboard
            </Link>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.9, ease, delay: 0.35 }}
            className="mt-10 text-[15px] italic text-content-tertiary"
          >
            &ldquo;o efeito borboleta começa com um clique.&rdquo;
          </motion.p>
        </div>
      </section>

      {/* ============ STATS BAR ============ */}
      <section className="relative border-y border-line bg-bg-subtle/60">
        <div className="container-page grid grid-cols-2 gap-px py-2 md:grid-cols-4">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, ease, delay: i * 0.06 }}
              className="px-4 py-6 text-center"
            >
              <p className="font-display text-3xl font-medium tracking-tight text-content-primary sm:text-4xl">
                {s.value}
              </p>
              <p className="mt-1 text-2xs uppercase tracking-[0.14em] text-content-faint">{s.label}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ============ HOW UPLOAD WORKS ============ */}
      <section className="border-b border-line">
        <div className="container-page py-24">
          <SectionHeader
            eyebrow="Como funciona"
            title="Do seu save ao insight"
            description="Envie o save do jogo e deixe a plataforma cuidar do resto — ingestão event-driven, data lake em camadas e analytics prontos em minutos."
          />

          <div className="mt-14 grid gap-4 md:grid-cols-4">
            {howItWorks.map((step, i) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ duration: 0.5, ease, delay: i * 0.08 }}
                className="surface relative p-6"
              >
                <span className="font-display text-3xl font-medium text-content-faint">0{i + 1}</span>
                <div className="mt-3 flex h-9 w-9 items-center justify-center rounded-lg border border-amber/25 bg-amber/[0.08] text-amber">
                  <step.icon className="h-[18px] w-[18px]" />
                </div>
                <h3 className="mt-4 text-base font-semibold">{step.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-content-secondary">{step.description}</p>
              </motion.div>
            ))}
          </div>

          <div className="mt-8">
            <Link href="/upload" className="btn-primary group h-11 px-6 text-[15px]">
              <Upload className="h-4 w-4" />
              Enviar Save
            </Link>
          </div>
        </div>
      </section>

      {/* ============ EPISODES / POLAROID GALLERY ============ */}
      <section className="relative border-b border-line">
        <div className="container-page py-24">
          <SectionHeader
            eyebrow="Momentos analisados"
            title="Cinco episódios, milhares de finais"
            description="Cada episódio registra pontos de decisão que ramificam a história. A plataforma acompanha como os jogadores se dividem em cada um deles."
          />

          <div className="mt-16 flex snap-x snap-mandatory gap-6 overflow-x-auto pb-6 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden lg:grid lg:grid-cols-5 lg:gap-4 lg:overflow-visible">
            {episodes.map((ep, i) => (
              <motion.figure
                key={ep.title}
                initial={{ opacity: 0, y: 24, rotate: ep.rotate }}
                whileInView={{ opacity: 1, y: 0, rotate: ep.rotate }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ duration: 0.55, ease, delay: i * 0.08 }}
                whileHover={{ rotate: 0, y: -6, scale: 1.02, zIndex: 10 }}
                className="polaroid group relative min-w-[240px] flex-shrink-0 snap-center lg:min-w-0"
              >
                <div className="relative aspect-[4/5] overflow-hidden bg-bg-elevated">
                  <PolaroidImage src={ep.image} alt={ep.title} index={i} />
                  <span className="absolute left-2 top-2 rounded bg-black/50 px-1.5 py-0.5 text-2xs font-medium text-white/90 backdrop-blur-sm">
                    EP{i + 1}
                  </span>
                </div>
                <figcaption className="mt-3">{ep.title}</figcaption>
              </motion.figure>
            ))}
          </div>
        </div>
      </section>

      {/* ============ FEATURES ============ */}
      <section className="border-b border-line">
        <div className="container-page py-24">
          <SectionHeader
            eyebrow="A plataforma"
            title="Engenharia de dados de ponta a ponta"
            description="Clean Architecture, Domain-Driven Design e event-driven — cada camada isolada, testável e pronta para escalar."
          />

          <div className="mt-14 grid gap-4 md:grid-cols-3">
            {features.map((f, i) => (
              <FeatureCard key={f.title} feature={f} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ============ MEDALLION + PIPELINE ============ */}
      <section className="border-b border-line">
        <div className="container-page py-24">
          <SectionHeader
            eyebrow="Data Lake"
            title="Arquitetura Medallion"
            description="Os dados fluem de bruto a curado em três camadas, com rastreabilidade e reprocessamento completos."
          />

          <div className="mt-14 grid gap-4 lg:grid-cols-3">
            {layers.map((l, i) => (
              <motion.div
                key={l.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ duration: 0.5, ease, delay: i * 0.08 }}
                className="surface p-6"
              >
                <div className="flex items-center gap-3">
                  <span className={`grid h-8 w-8 place-items-center rounded-md text-xs font-bold text-bg ${l.chip}`}>
                    {l.name[0]}
                  </span>
                  <h3 className="text-base font-semibold">{l.name}</h3>
                </div>
                <p className="mt-4 text-sm leading-relaxed text-content-secondary">{l.description}</p>
                <div className="mt-5 flex flex-wrap gap-1.5">
                  {l.tags.map((t) => (
                    <span
                      key={t}
                      className="rounded-md border border-line bg-white/[0.02] px-2 py-0.5 text-2xs text-content-tertiary"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.7, ease }}
            className="mt-8 rounded-2xl border border-line-strong bg-bg-subtle p-2 shadow-glow"
          >
            <div className="hairline-top overflow-hidden rounded-xl border border-line bg-bg">
              <PipelineMock />
            </div>
          </motion.div>
        </div>
      </section>

      {/* ============ CTA ============ */}
      <section className="relative overflow-hidden border-b border-line">
        <div aria-hidden className="absolute inset-0">
          <Image
            src={img('photo-1505142468610-359e7d316be0', 1920)}
            alt=""
            fill
            sizes="100vw"
            className="img-graded object-cover object-center opacity-40"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-bg via-bg/80 to-bg" />
        </div>

        <div className="container-page relative py-28 text-center">
          <Butterfly className="mx-auto h-12 w-12 animate-float opacity-90 drop-shadow-[0_0_20px_rgba(240,169,78,0.4)]" />
          <h2 className="mx-auto mt-6 max-w-2xl font-display text-4xl font-medium tracking-tight sm:text-5xl">
            Pronto para rebobinar os dados?
          </h2>
          <p className="mx-auto mt-4 max-w-md text-content-secondary">
            Estatísticas de jogadores, distribuição de escolhas e clusters
            comportamentais — atualizados em tempo real.
          </p>
          <div className="mt-9 flex items-center justify-center gap-3">
            <Link href="/dashboard" className="btn-primary group h-11 px-6 text-[15px]">
              Abrir dashboard
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Link>
          </div>
          <p className="mt-8 text-[15px] italic text-content-tertiary">nunca é tarde para uma nova timeline.</p>
        </div>
      </section>

      <Footer />
    </main>
  )
}

/* ---------------- Sub-components ---------------- */

function SectionHeader({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string
  title: string
  description: string
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.6, ease }}
      className="max-w-2xl"
    >
      <span className="eyebrow">{eyebrow}</span>
      <h2 className="mt-3 font-display text-3xl font-medium tracking-tight sm:text-[40px]">{title}</h2>
      <p className="mt-4 text-content-secondary">{description}</p>
    </motion.div>
  )
}

function FeatureCard({ feature, index }: { feature: Feature; index: number }) {
  const Icon = feature.icon
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.5, ease, delay: index * 0.06 }}
      className="group surface p-6 transition-colors hover:border-line-strong"
    >
      <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-amber/25 bg-amber/[0.08] text-amber transition-colors group-hover:text-amber-soft">
        <Icon className="h-[18px] w-[18px]" />
      </div>
      <h3 className="mt-5 text-base font-semibold">{feature.title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-content-secondary">{feature.description}</p>
    </motion.div>
  )
}

/** Episode polaroid image with a graceful gradient fallback while real art is added. */
function PolaroidImage({ src, alt, index }: { src: string; alt: string; index: number }) {
  const [failed, setFailed] = useState(false)
  const gradients = [
    'from-teal/30 to-sky/20',
    'from-amber/30 to-sunset/20',
    'from-sunset/30 to-violet/20',
    'from-sky/30 to-teal/20',
    'from-violet/30 to-amber/20',
  ]

  if (failed) {
    return (
      <div className={`absolute inset-0 grid place-items-center bg-gradient-to-br ${gradients[index % gradients.length]}`}>
        <span className="font-display text-4xl font-medium text-white/70">EP{index + 1}</span>
      </div>
    )
  }

  return (
    <Image
      src={src}
      alt={alt}
      fill
      sizes="(max-width: 1024px) 240px, 220px"
      onError={() => setFailed(true)}
      className="img-graded object-cover transition-transform duration-500 group-hover:scale-105"
    />
  )
}

function PipelineMock() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[220px_1fr]">
      <aside className="hidden border-r border-line p-4 lg:block">
        <div className="flex items-center gap-2 px-2">
          <span className="h-2.5 w-2.5 rounded-full bg-[#ff5f57]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#febc2e]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#28c840]" />
        </div>
        <nav className="mt-6 space-y-1">
          {['Ingestão', 'Data Lake', 'Transformação', 'ML Pipeline', 'Analytics'].map((item, i) => (
            <div
              key={item}
              className={`rounded-md px-3 py-2 text-[13px] ${
                i === 1 ? 'bg-white/[0.06] text-content-primary' : 'text-content-tertiary'
              }`}
            >
              {item}
            </div>
          ))}
        </nav>
      </aside>

      <div className="p-6">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <p className="text-2xs font-semibold uppercase tracking-[0.14em] text-content-faint">
              Pipeline em execução
            </p>
            <p className="mt-1 text-sm font-medium">saves.uploaded → choices.extracted</p>
          </div>
          <span className="inline-flex items-center gap-2 rounded-full border border-teal/25 bg-teal/10 px-2.5 py-1 text-2xs font-medium text-teal">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-teal" />
            Live
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
          {stages.map((s, i) => (
            <div key={s.label} className="relative">
              <div className="rounded-lg border border-line bg-bg-subtle p-3">
                <div className="flex h-7 w-7 items-center justify-center rounded-md border border-line bg-white/[0.02] text-content-secondary">
                  <s.icon className="h-3.5 w-3.5" />
                </div>
                <p className="mt-3 text-[13px] font-medium">{s.label}</p>
                <p className="mt-0.5 text-2xs text-content-tertiary">{s.tech}</p>
              </div>
              {i < stages.length - 1 && (
                <div className="absolute right-[-9px] top-1/2 hidden h-px w-3 -translate-y-1/2 bg-line-strong sm:block" />
              )}
            </div>
          ))}
        </div>

        <div className="mt-6 grid grid-cols-3 gap-3">
          {metrics.map((m) => (
            <div key={m.label} className="rounded-lg border border-line bg-bg-subtle p-4">
              <p className="font-display text-2xl font-medium tracking-tight">{m.value}</p>
              <p className="mt-1 text-2xs text-content-tertiary">{m.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

/* ---------------- Data ---------------- */

type Feature = {
  icon: typeof Cpu
  title: string
  description: string
}

const howItWorks = [
  { icon: Upload, title: 'Envie o save', description: 'Arraste o arquivo do jogo. A API valida e registra o upload em segundos.' },
  { icon: Radio, title: 'Evento no Kafka', description: 'Um evento saves.uploaded dispara o pipeline de forma assíncrona e resiliente.' },
  { icon: Database, title: 'Data Lake', description: 'As escolhas são extraídas e armazenadas nas camadas Bronze, Silver e Gold.' },
  { icon: LineChart, title: 'Analytics', description: 'Seu dashboard, comparações e predições ficam prontos e atualizados.' },
]

const episodes = [
  { title: 'Chrysalis', image: '/images/episodes/a_episode.jpg', rotate: -3 },
  { title: 'Out of Time', image: '/images/episodes/b_episode.png', rotate: 2 },
  { title: 'Chaos Theory', image: '/images/episodes/c_episode.jpg', rotate: -2 },
  { title: 'Dark Room', image: '/images/episodes/d_episode.jpg', rotate: 3 },
  { title: 'Polarized', image: '/images/episodes/e_episode.png', rotate: -1 },
]

const features: Feature[] = [
  {
    icon: Cpu,
    title: 'REST API assíncrona',
    description: 'FastAPI com SQLAlchemy 2.0 async, PostgreSQL e padrão Repository para acesso desacoplado.',
  },
  {
    icon: Workflow,
    title: 'Event streaming',
    description: 'Apache Kafka processa saves e extrai escolhas de forma assíncrona e resiliente.',
  },
  {
    icon: Database,
    title: 'Data lake medallion',
    description: 'MinIO com camadas Bronze, Silver e Gold. Batch processing com Apache Spark.',
  },
  {
    icon: Sparkles,
    title: 'Machine learning',
    description: 'Random Forest para predição de escolhas e K-Means para clustering de jogadores.',
  },
  {
    icon: LineChart,
    title: 'Analytics OLAP',
    description: 'ClickHouse para queries analíticas de alta performance sobre milhões de registros.',
  },
  {
    icon: GitBranch,
    title: 'Orquestração',
    description: 'Airflow coordena DAGs de ETL/ELT com observabilidade via Prometheus e Grafana.',
  },
]

const layers = [
  {
    name: 'Bronze',
    chip: 'bg-sunset',
    description: 'Dados brutos em JSON, particionados por data. Imutáveis e totalmente rastreáveis.',
    tags: ['Kafka', 'MinIO', 'JSON', 'Partitioned'],
  },
  {
    name: 'Silver',
    chip: 'bg-sky',
    description: 'Dados limpos e validados em Parquet. Schema enforcement e deduplicação.',
    tags: ['Spark', 'Parquet', 'Validated', 'Deduped'],
  },
  {
    name: 'Gold',
    chip: 'bg-amber',
    description: 'Agregações otimizadas para analytics: estatísticas, métricas diárias e KPIs.',
    tags: ['ClickHouse', 'KPIs', 'Aggregated', 'Curated'],
  },
]

const stages = [
  { icon: Workflow, label: 'Ingest', tech: 'Kafka' },
  { icon: Boxes, label: 'Store', tech: 'MinIO' },
  { icon: Cpu, label: 'Process', tech: 'Spark' },
  { icon: Database, label: 'Serve', tech: 'ClickHouse' },
  { icon: Camera, label: 'Visualize', tech: 'Next.js' },
]

const metrics = [
  { value: '12', label: 'Serviços orquestrados' },
  { value: '3', label: 'Camadas do data lake' },
  { value: '5', label: 'Episódios cobertos' },
]
