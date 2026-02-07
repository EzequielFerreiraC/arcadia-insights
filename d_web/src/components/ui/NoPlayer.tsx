import Link from 'next/link'
import { Upload, UserRound } from 'lucide-react'
import { Card, CardBody } from '@/components/ui/Card'

/** Shown on personal pages when no save has been uploaded from this browser yet. */
export function NoPlayer({
  message = 'Envie um save de Life is Strange para desbloquear a sua análise pessoal.',
}: {
  message?: string
}) {
  return (
    <Card>
      <CardBody className="flex flex-col items-center gap-4 py-14 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-amber/25 bg-amber/10 text-amber">
          <UserRound className="h-7 w-7" />
        </div>
        <div>
          <h3 className="font-display text-lg font-medium tracking-tight">Nenhum jogador ainda</h3>
          <p className="mx-auto mt-1.5 max-w-sm text-sm text-content-tertiary">{message}</p>
        </div>
        <Link href="/upload" className="btn-primary h-10 px-5 text-[14px]">
          <Upload className="h-4 w-4" />
          Enviar Save
        </Link>
        <p className="text-2xs text-content-faint">
          Sem login: você é identificado pelo save que enviar deste navegador.
        </p>
      </CardBody>
    </Card>
  )
}
