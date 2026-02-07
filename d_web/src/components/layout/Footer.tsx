import Link from 'next/link'
import { Logo } from '@/components/brand/Logo'

const columns = [
  {
    title: 'Produto',
    items: [
      { label: 'Visão geral', href: '/' },
      { label: 'Enviar Save', href: '/upload' },
      { label: 'Meu Dashboard', href: '/dashboard' },
      { label: 'API Docs', href: 'http://localhost:8000/docs', external: true },
    ],
  },
  {
    title: 'Comunidade',
    items: [
      { label: 'Estatísticas Globais', href: '/stats' },
      { label: 'Análise de Caminhos', href: '/paths' },
      { label: 'Perfis de Jogadores', href: '/profiles' },
      { label: 'Leaderboard', href: '/leaderboard' },
    ],
  },
  {
    title: 'Plataforma',
    items: [
      { label: 'Data Catalog', href: '/catalog' },
      { label: 'Observabilidade', href: '/observability' },
      { label: 'Predição de Final', href: '/prediction' },
    ],
  },
]

export function Footer() {
  return (
    <footer className="border-t border-line">
      <div className="container-page py-14">
        <div className="grid gap-10 md:grid-cols-[1.5fr_1fr_1fr_1fr]">
          <div>
            <div className="flex items-center gap-2.5">
              <Logo className="h-7 w-7" />
              <span className="font-display text-[17px] font-semibold tracking-tight">Arcadia Insights</span>
            </div>
            <p className="mt-4 max-w-xs text-[13px] leading-relaxed text-content-tertiary">
              A plataforma de choice analytics para Life is Strange. Cada decisão
              dos jogadores, transformada em insight em tempo real.
            </p>
            <p className="mt-4 text-[13px] italic text-content-tertiary">
              todas as escolhas importam.
            </p>
          </div>

          {columns.map((col) => (
            <div key={col.title}>
              <h4 className="text-2xs font-semibold uppercase tracking-[0.14em] text-content-faint">
                {col.title}
              </h4>
              <ul className="mt-4 space-y-2.5">
                {col.items.map((item) => (
                  <li key={item.label}>
                    {'external' in item && item.external ? (
                      <a
                        href={item.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[13px] text-content-tertiary transition-colors hover:text-content-secondary"
                      >
                        {item.label}
                      </a>
                    ) : (
                      <Link
                        href={item.href}
                        className="text-[13px] text-content-tertiary transition-colors hover:text-content-secondary"
                      >
                        {item.label}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 flex flex-col items-start justify-between gap-3 border-t border-line pt-6 sm:flex-row sm:items-center">
          <p className="text-2xs text-content-faint">
            © 2026 Arcadia Insights. Fan project sem fins comerciais — não afiliado à Square Enix / Deck Nine.
          </p>
          <p className="text-2xs text-content-faint">Choice Analytics Platform</p>
        </div>
      </div>
    </footer>
  )
}
