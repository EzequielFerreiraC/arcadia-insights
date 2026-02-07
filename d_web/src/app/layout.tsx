import type { Metadata } from 'next'
import './globals.css'
import { Providers } from './providers'

export const metadata: Metadata = {
  title: 'Arcadia Insights - Life is Strange Choice Analytics',
  description:
    'Plataforma de engenharia de dados que analisa comportamento e padroes de escolha dos jogadores de Life is Strange.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className="noise antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}