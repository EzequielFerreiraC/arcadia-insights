/**
 * Mock analytics data for pages that are not yet wired to a live backend.
 * Content references Life is Strange (Season 1) choices for authenticity.
 * Real player/health data still comes from the FastAPI backend via `api.ts`.
 */
import type {
  CatalogTable,
  CompareRow,
  EndingPrediction,
  Episode,
  EpisodeDistribution,
  GameDistribution,
  LeaderboardEntry,
  NarrativePath,
  PipelineHealth,
  PlayerProfileCluster,
  RankedChoice,
  TimelineEpisode,
  TrendPoint,
  UploadRecord,
} from '@/types'

export const episodes: Episode[] = [
  { id: 1, title: 'Chrysalis', slug: 'chrysalis', image: 'photo-1441974231531-c6227db76b6e' },
  { id: 2, title: 'Out of Time', slug: 'out-of-time', image: 'photo-1507525428034-b723cf961d3e' },
  { id: 3, title: 'Chaos Theory', slug: 'chaos-theory', image: 'photo-1470252649378-9c29740c9fa8' },
  { id: 4, title: 'Dark Room', slug: 'dark-room', image: 'photo-1500375592092-40eb2168fd21' },
  { id: 5, title: 'Polarized', slug: 'polarized', image: 'photo-1505142468610-359e7d316be0' },
]

/** Quick global figures used on the home page. */
export const globalStats = {
  totalPlayers: 128_540,
  totalChoices: 2_431_880,
  mostCommonChoice: { label: 'Salvar Kate Marsh', pct: 82 },
  totalSaves: 184_920,
}

/** Demo "my dashboard" player summary. */
export const myPlayer = {
  name: 'Max Caulfield',
  handle: '@rewind',
  archetype: 'Empático',
  archetypeDescription:
    'Prioriza o bem-estar das pessoas ao redor, mesmo quando isso traz consequências pessoais.',
  compatibility: 72,
  ending: 'Sacrifice Arcadia Bay',
  totalChoices: 42,
  completedEpisodes: 5,
  rareChoices: [
    { label: 'Acusar Nathan Prescott', episode: 4, pct: 4 },
    { label: 'Não confortar Victoria', episode: 4, pct: 11 },
    { label: 'Esconder-se de Chloe', episode: 3, pct: 17 },
  ] as RankedChoice[],
  popularChoices: [
    { label: 'Salvar Kate Marsh', episode: 2, pct: 82 },
    { label: 'Regar a planta da Lisa', episode: 1, pct: 74 },
    { label: 'Beijar Chloe', episode: 3, pct: 63 },
  ] as RankedChoice[],
}

export const timeline: TimelineEpisode[] = [
  {
    episode: 1,
    title: 'Chrysalis',
    choices: [
      { label: 'Encontro no banheiro', option: 'Não reportar Nathan', consequence: 'Nathan permanece livre', communityPct: 51 },
      { label: 'Planta da Lisa', option: 'Regar a planta', consequence: 'Lisa sobrevive ao episódio', communityPct: 74 },
      { label: 'Diário da Kate', option: 'Assinar a petição', consequence: 'Kate se sente apoiada', communityPct: 88 },
    ],
  },
  {
    episode: 2,
    title: 'Out of Time',
    choices: [
      { label: 'Telhado do dormitório', option: 'Salvar Kate', consequence: 'Kate sobrevive', communityPct: 82 },
      { label: 'Ferrovia', option: 'Ajudar Alyssa', consequence: 'Alyssa evita acidentes futuros', communityPct: 69 },
    ],
  },
  {
    episode: 3,
    title: 'Chaos Theory',
    choices: [
      { label: 'Quarto da Chloe', option: 'Confiar em Chloe', consequence: 'Aprofunda a amizade', communityPct: 63 },
      { label: 'Fim do episódio', option: 'Culpar Nathan', consequence: 'Investigação muda de rumo', communityPct: 34 },
    ],
  },
  {
    episode: 4,
    title: 'Dark Room',
    choices: [
      { label: 'Cadeira de rodas', option: 'Contar a verdade a Chloe', consequence: 'Confronto emocional', communityPct: 57 },
      { label: 'Festa Vortex', option: 'Acusar Nathan', consequence: 'Escolha extremamente rara', communityPct: 4 },
    ],
  },
  {
    episode: 5,
    title: 'Polarized',
    choices: [
      { label: 'Farol', option: 'Sacrificar Arcadia Bay', consequence: 'Chloe sobrevive', communityPct: 53 },
    ],
  },
]

export const compareRows: CompareRow[] = [
  { episode: 2, choice: 'Salvar Kate', you: 'Sim', community: 82 },
  { episode: 4, choice: 'Culpar Nathan', you: 'Não', community: 34 },
  { episode: 1, choice: 'Regar a planta da Lisa', you: 'Sim', community: 74 },
  { episode: 3, choice: 'Beijar Chloe', you: 'Sim', community: 63 },
  { episode: 3, choice: 'Encobrir o desastre da piscina', you: 'Não', community: 41 },
  { episode: 5, choice: 'Sacrificar Arcadia Bay', you: 'Sim', community: 53 },
]

export const mostPopular: RankedChoice[] = [
  { label: 'Assinar a petição da Kate', episode: 1, pct: 88 },
  { label: 'Salvar Kate Marsh', episode: 2, pct: 82 },
  { label: 'Regar a planta da Lisa', episode: 1, pct: 74 },
  { label: 'Ajudar Alyssa', episode: 2, pct: 69 },
  { label: 'Beijar Chloe', episode: 3, pct: 63 },
]

export const leastPopular: RankedChoice[] = [
  { label: 'Acusar Nathan Prescott', episode: 4, pct: 4 },
  { label: 'Não confortar Victoria', episode: 4, pct: 11 },
  { label: 'Não salvar Kate', episode: 2, pct: 18 },
  { label: 'Culpar Chloe pelo desastre', episode: 3, pct: 22 },
  { label: 'Recusar ajuda a Alyssa', episode: 2, pct: 31 },
]

export const episodeDistribution: EpisodeDistribution[] = [
  { episode: 'Ep 1', choices: 612_400 },
  { episode: 'Ep 2', choices: 548_900 },
  { episode: 'Ep 3', choices: 481_250 },
  { episode: 'Ep 4', choices: 432_100 },
  { episode: 'Ep 5', choices: 357_230 },
]

export const gameDistribution: GameDistribution[] = [
  { game: 'Season 1', players: 71_200 },
  { game: 'Before the Storm', players: 24_800 },
  { game: 'True Colors', players: 19_640 },
  { game: 'Double Exposure', players: 12_900 },
]

export const eventsTrend: TrendPoint[] = [
  { date: 'Seg', events: 42_100 },
  { date: 'Ter', events: 51_800 },
  { date: 'Qua', events: 48_300 },
  { date: 'Qui', events: 63_200 },
  { date: 'Sex', events: 78_900 },
  { date: 'Sáb', events: 94_500 },
  { date: 'Dom', events: 88_700 },
]

export const narrativePaths: NarrativePath[] = [
  { label: 'Salvar Kate → Confiar em Chloe', detail: '87% dos jogadores que salvaram Kate também confiaram em Chloe.', frequency: 87 },
  { label: 'Regar a planta → Assinar petição', detail: 'Caminho "empático" mais comum do Episódio 1.', frequency: 71 },
  { label: 'Acusar Nathan → Sacrificar Chloe', detail: 'Rota rara com forte carga moral.', frequency: 6 },
  { label: 'Não salvar Kate → Culpar Chloe', detail: 'Caminho "utilitarista" incomum.', frequency: 9 },
]

export const profiles: PlayerProfileCluster[] = [
  {
    name: 'Empático',
    description: 'Prioriza pessoas e relações acima do resultado prático.',
    players: 46_200,
    occurrence: 36,
    typicalChoices: ['Salvar Kate', 'Regar a planta', 'Confortar Victoria'],
    accent: 'teal',
  },
  {
    name: 'Utilitarista',
    description: 'Busca o maior benefício coletivo, mesmo com custo pessoal.',
    players: 28_900,
    occurrence: 22,
    typicalChoices: ['Sacrificar Chloe', 'Denunciar Nathan', 'Encobrir o desastre'],
    accent: 'amber',
  },
  {
    name: 'Impulsivo',
    description: 'Decide rápido, guiado por emoção e instinto do momento.',
    players: 31_500,
    occurrence: 25,
    typicalChoices: ['Culpar Nathan', 'Confrontar David', 'Beijar Chloe'],
    accent: 'sunset',
  },
  {
    name: 'Diplomático',
    description: 'Evita conflito e negocia para manter o equilíbrio.',
    players: 21_940,
    occurrence: 17,
    typicalChoices: ['Não reportar Nathan', 'Mediar a discussão', 'Apaziguar Victoria'],
    accent: 'sky',
  },
]

export const endingPredictions: EndingPrediction[] = [
  { ending: 'Sacrifice Arcadia Bay', probability: 87, accent: 'sunset' },
  { ending: 'Sacrifice Chloe', probability: 13, accent: 'sky' },
]

export const endingFactors = [
  { factor: 'Confiar em Chloe (Ep. 3)', weight: 'alto', direction: 'Arcadia Bay' },
  { factor: 'Salvar Kate (Ep. 2)', weight: 'médio', direction: 'Arcadia Bay' },
  { factor: 'Perfil Empático', weight: 'alto', direction: 'Arcadia Bay' },
  { factor: 'Tempo médio por decisão', weight: 'baixo', direction: 'neutro' },
]

export const leaderboard: LeaderboardEntry[] = [
  { rank: 1, name: 'João Ferreira', handle: '@rewinder', avgRarity: 91, rareCount: 12 },
  { rank: 2, name: 'Maria Alves', handle: '@bluejay', avgRarity: 88, rareCount: 10 },
  { rank: 3, name: 'Lucas Prado', handle: '@stormchaser', avgRarity: 84, rareCount: 9 },
  { rank: 4, name: 'Ana Beatriz', handle: '@chrysalis', avgRarity: 79, rareCount: 8 },
  { rank: 5, name: 'Pedro Santos', handle: '@polaroid', avgRarity: 76, rareCount: 7 },
]

export const uploadHistory: UploadRecord[] = [
  { id: 'sv_9a21', filename: 'lis_ep5_finale.sav', size: '2.4 MB', status: 'done', stage: 'Gold', uploadedAt: '2026-07-08T12:40:00Z' },
  { id: 'sv_8f04', filename: 'lis_ep4_darkroom.sav', size: '2.1 MB', status: 'processing', stage: 'Silver', uploadedAt: '2026-07-08T12:12:00Z' },
  { id: 'sv_7c88', filename: 'lis_ep3_chaos.sav', size: '1.9 MB', status: 'done', stage: 'Gold', uploadedAt: '2026-07-08T11:05:00Z' },
  { id: 'sv_7b10', filename: 'lis_ep2_corrupt.sav', size: '0.4 MB', status: 'failed', stage: 'Bronze', uploadedAt: '2026-07-08T10:22:00Z' },
]

export const supportedFormats = [
  { ext: '.sav', label: 'Save nativo de Life is Strange' },
  { ext: '.json', label: 'Export estruturado de escolhas' },
  { ext: '.zip', label: 'Pacote com múltiplos saves' },
]

export const catalogTables: CatalogTable[] = [
  { name: 'bronze.saves_raw', layer: 'Bronze', rows: 184_920, format: 'JSON', partitions: 92, updated: '2026-07-08T12:40:00Z' },
  { name: 'silver.choices', layer: 'Silver', rows: 2_431_880, format: 'Parquet', partitions: 45, updated: '2026-07-08T12:35:00Z' },
  { name: 'silver.players', layer: 'Silver', rows: 128_540, format: 'Parquet', partitions: 12, updated: '2026-07-08T12:35:00Z' },
  { name: 'gold.choice_stats', layer: 'Gold', rows: 640, format: 'ClickHouse', partitions: 5, updated: '2026-07-08T12:30:00Z' },
  { name: 'gold.player_clusters', layer: 'Gold', rows: 4, format: 'ClickHouse', partitions: 1, updated: '2026-07-08T12:30:00Z' },
]

export const catalogMetrics = {
  totalRecords: 2_745_980,
  eventsProcessed24h: 512_400,
  avgPipelineLatencyMs: 340,
  dataLakePartitions: 155,
}

export const pipelineHealth: PipelineHealth[] = [
  { name: 'Kafka', status: 'healthy', detail: 'saves.uploaded · choices.extracted', metric: '3 tópicos · lag 0' },
  { name: 'Airflow', status: 'healthy', detail: 'DAG medallion_etl', metric: 'último run OK · 04:00' },
  { name: 'Spark', status: 'degraded', detail: 'silver_transformation', metric: '1 executor reiniciado' },
  { name: 'ClickHouse', status: 'healthy', detail: 'gold analytics', metric: 'p95 42 ms' },
]

export const observability = {
  throughputPerMin: 4_260,
  eventsLastHour: 255_600,
  jobsExecuted24h: 1_284,
  failures24h: 7,
  successRate: 99.4,
}
