import type { LucideIcon } from 'lucide-react'
import {
  Activity, BarChart3, Database, GitCompareArrows, LayoutDashboard,
  ListTree, Route, Sparkles, Trophy, Upload, Users,
} from 'lucide-react'

export interface NavItem {
  href: string
  label: string
  icon: LucideIcon
  description?: string
}

export interface NavGroup {
  title: string
  items: NavItem[]
}

/** Grouped navigation for the analytics app area (rendered in the sidebar). */
export const navGroups: NavGroup[] = [
  {
    title: 'Meu jogo',
    items: [
      { href: '/dashboard', label: 'Meu Dashboard', icon: LayoutDashboard, description: 'Análise do jogador' },
      { href: '/timeline', label: 'Timeline', icon: ListTree, description: 'Jornada de decisões' },
      { href: '/compare', label: 'Comparação', icon: GitCompareArrows, description: 'Você vs. comunidade' },
      { href: '/prediction', label: 'Predição de Final', icon: Sparkles, description: 'Resultado do modelo' },
    ],
  },
  {
    title: 'Comunidade',
    items: [
      { href: '/stats', label: 'Estatísticas Globais', icon: BarChart3, description: 'Analytics gerais' },
      { href: '/paths', label: 'Análise de Caminhos', icon: Route, description: 'Rotas narrativas' },
      { href: '/profiles', label: 'Perfis de Jogadores', icon: Users, description: 'Segmentação por ML' },
      { href: '/leaderboard', label: 'Leaderboard', icon: Trophy, description: 'Escolhas raras' },
    ],
  },
  {
    title: 'Dados & plataforma',
    items: [
      { href: '/upload', label: 'Enviar Save', icon: Upload, description: 'Entrada de dados' },
      { href: '/catalog', label: 'Data Catalog', icon: Database, description: 'Engenharia de dados' },
      { href: '/observability', label: 'Observabilidade', icon: Activity, description: 'Monitoramento' },
    ],
  },
]

export const allNavItems: NavItem[] = navGroups.flatMap((g) => g.items)

/** Marketing top-nav (home). */
export const marketingLinks = [
  { href: '/', label: 'Visão geral' },
  { href: '/stats', label: 'Estatísticas' },
  { href: '/dashboard', label: 'Dashboard' },
]
