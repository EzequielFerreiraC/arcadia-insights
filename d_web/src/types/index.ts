/** Shared domain types for the Arcadia Insights front-end. */

export interface Episode {
  id: number
  title: string
  slug: string
  image: string
}

export interface TimelineChoice {
  label: string
  option: string
  consequence: string
  communityPct: number
}

export interface TimelineEpisode {
  episode: number
  title: string
  choices: TimelineChoice[]
}

export interface CompareRow {
  episode: number
  choice: string
  you: string
  community: number
}

export interface RankedChoice {
  label: string
  episode: number
  pct: number
}

export interface EpisodeDistribution {
  episode: string
  choices: number
}

export interface GameDistribution {
  game: string
  players: number
}

export interface TrendPoint {
  date: string
  events: number
}

export interface PlayerProfileCluster {
  name: string
  description: string
  players: number
  occurrence: number
  typicalChoices: string[]
  accent: Accent
}

export interface EndingPrediction {
  ending: string
  probability: number
  accent: Accent
}

export interface LeaderboardEntry {
  rank: number
  name: string
  handle: string
  avgRarity: number
  rareCount: number
}

export interface NarrativePath {
  label: string
  detail: string
  frequency: number
}

export interface UploadRecord {
  id: string
  filename: string
  size: string
  status: 'processing' | 'done' | 'failed' | 'queued'
  stage: string
  uploadedAt: string
}

export interface CatalogTable {
  name: string
  layer: 'Bronze' | 'Silver' | 'Gold'
  rows: number
  format: string
  partitions: number
  updated: string
}

export interface PipelineHealth {
  name: string
  status: 'healthy' | 'degraded' | 'down'
  detail: string
  metric: string
}

export type Accent = 'teal' | 'amber' | 'sky' | 'sunset' | 'violet'
