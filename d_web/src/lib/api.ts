import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Player {
  id: string
  country: string
  platform: string
  game_version: string
  created_at: string
  updated_at: string
  total_saves: number
  total_choices: number
}

export interface PlayerCreate {
  country: string
  platform: string
  game_version: string
}

export const playersApi = {
  async getAll(skip = 0, limit = 10): Promise<Player[]> {
    const response = await apiClient.get(`/api/v1/players/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async getById(id: string): Promise<Player> {
    const response = await apiClient.get(`/api/v1/players/${id}`)
    return response.data
  },

  async create(data: PlayerCreate): Promise<Player> {
    const response = await apiClient.post('/api/v1/players/', data)
    return response.data
  },
}

export const healthApi = {
  async check(): Promise<{ status: string }> {
    const response = await apiClient.get('/health')
    return response.data
  },
}

/* ============ Saves ============ */

export interface SaveRecord {
  id: string
  player_id: string
  filename: string
  file_size_bytes: number
  checksum: string
  status: 'uploaded' | 'processing' | 'processed' | 'failed'
  s3_path: string | null
  uploaded_at: string
  processed_at: string | null
  choices_extracted: number
  error_message: string | null
}

export const savesApi = {
  async upload(file: File, playerId?: string): Promise<SaveRecord> {
    const form = new FormData()
    form.append('file', file)
    if (playerId) form.append('player_id', playerId)
    const response = await apiClient.post('/api/v1/saves/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  async getAll(skip = 0, limit = 100): Promise<SaveRecord[]> {
    const response = await apiClient.get(`/api/v1/saves/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async delete(saveId: string): Promise<void> {
    await apiClient.delete(`/api/v1/saves/${saveId}`)
  },
}

/* ============ Analytics ============ */

export interface GlobalStats {
  total_players: number
  total_choices: number
  total_saves: number
  most_common_choice: { label: string; pct: number }
}

export interface RankedChoice {
  choice_id: string
  choice_text: string
  episode: number
  option_selected: string
  players: number
  pct: number
}

export interface EpisodeDistribution {
  episode: string
  choices: number
}

export interface LeaderboardEntry {
  player_id: string
  country: string
  avg_rarity: number
  rare_count: number
}

export interface CompareRow {
  choice_id: string
  choice_text: string
  episode: number
  option_selected: string
  community_pct: number
}

export interface PlayerRankedChoice {
  label: string
  episode: number
  pct: number
}

export interface PlayerSummary {
  total_choices: number
  completed_episodes: number
  compatibility: number
  ending: string
  rare_choices: PlayerRankedChoice[]
  popular_choices: PlayerRankedChoice[]
}

export interface TimelineRow {
  episode: number
  chapter: number
  choice_id: string
  choice_text: string
  option_selected: string
  community_pct: number
}

export interface NarrativePath {
  label: string
  detail: string
  frequency: number
}

export const analyticsApi = {
  async global(): Promise<GlobalStats> {
    const response = await apiClient.get('/api/v1/analytics/global')
    return response.data
  },
  async popularChoices(limit = 5): Promise<RankedChoice[]> {
    const response = await apiClient.get(`/api/v1/analytics/choices/popular?limit=${limit}`)
    return response.data
  },
  async rareChoices(limit = 5): Promise<RankedChoice[]> {
    const response = await apiClient.get(`/api/v1/analytics/choices/rare?limit=${limit}`)
    return response.data
  },
  async episodeDistribution(): Promise<EpisodeDistribution[]> {
    const response = await apiClient.get('/api/v1/analytics/episodes')
    return response.data
  },
  async timeline(): Promise<TimelineRow[]> {
    const response = await apiClient.get('/api/v1/analytics/timeline')
    return response.data
  },
  async paths(): Promise<NarrativePath[]> {
    const response = await apiClient.get('/api/v1/analytics/paths')
    return response.data
  },
  async leaderboard(limit = 10): Promise<LeaderboardEntry[]> {
    const response = await apiClient.get(`/api/v1/analytics/leaderboard?limit=${limit}`)
    return response.data
  },
  async playerCompare(playerId: string): Promise<CompareRow[]> {
    const response = await apiClient.get(`/api/v1/analytics/players/${playerId}/compare`)
    return response.data
  },
  async playerSummary(playerId: string): Promise<PlayerSummary> {
    const response = await apiClient.get(`/api/v1/analytics/players/${playerId}/summary`)
    return response.data
  },
}

/* ============ Platform (Catalog & Observability) ============ */

export interface CatalogTableRow {
  name: string
  layer: string
  rows: number
  format: string
  partitions: number
  updated: string | null
}

export interface PipelineHealthRow {
  name: string
  status: 'healthy' | 'degraded' | 'down'
  detail: string
  metric: string
}

export interface CatalogResponse {
  metrics: {
    total_records: number
    events_processed_24h: number
    avg_pipeline_latency_ms: number
    data_lake_partitions: number
  }
  tables: CatalogTableRow[]
  pipelines: PipelineHealthRow[]
}

export interface ObservabilityResponse {
  throughput_per_min: number
  events_last_hour: number
  jobs_executed_24h: number
  failures_24h: number
  success_rate: number
}

export const platformApi = {
  async catalog(): Promise<CatalogResponse> {
    const response = await apiClient.get('/api/v1/platform/catalog')
    return response.data
  },
  async observability(): Promise<ObservabilityResponse> {
    const response = await apiClient.get('/api/v1/platform/observability')
    return response.data
  },
}

/* ============ Machine Learning ============ */

export interface EndingPredictionRow {
  ending: string
  probability: number
}

export interface PredictionFactor {
  factor: string
  weight: string
  direction: string
}

export interface PredictionResponse {
  predictions: EndingPredictionRow[]
  factors: PredictionFactor[]
}

export interface ProfileCluster {
  name: string
  description: string
  players: number
  occurrence: number
  typical_choices: string[]
}

export const mlApi = {
  async prediction(playerId: string): Promise<PredictionResponse> {
    const response = await apiClient.get(`/api/v1/ml/prediction/${playerId}`)
    return response.data
  },
  async profiles(): Promise<ProfileCluster[]> {
    const response = await apiClient.get('/api/v1/ml/profiles')
    return response.data
  },
}
