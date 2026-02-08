'use client'

import { useCallback, useRef, useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import {
  CheckCircle2, Database, FileUp, Loader2, Radio, Trash2, UploadCloud, Workflow, XCircle,
} from 'lucide-react'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardBody, CardHeader } from '@/components/ui/Card'
import { StatusPill } from '@/components/ui/StatusPill'
import { supportedFormats } from '@/lib/mock'
import { savesApi, type SaveRecord } from '@/lib/api'
import { setCurrentPlayerId } from '@/lib/currentPlayer'
import { formatRelativeTime } from '@/lib/format'
import { cn } from '@/lib/utils'
import type { UploadRecord } from '@/types'

const pipeline = [
  { icon: FileUp, label: 'Upload', tech: 'FastAPI' },
  { icon: Radio, label: 'Evento', tech: 'Kafka' },
  { icon: Database, label: 'Data Lake', tech: 'MinIO · Bronze' },
  { icon: Workflow, label: 'Processamento', tech: 'Spark' },
]

const STAGE: Record<SaveRecord['status'], string> = {
  uploaded: 'Bronze',
  processing: 'Silver',
  processed: 'Gold',
  failed: 'Bronze',
}

const STATUS: Record<SaveRecord['status'], UploadRecord['status']> = {
  uploaded: 'queued',
  processing: 'processing',
  processed: 'done',
  failed: 'failed',
}

function toRecord(s: SaveRecord): UploadRecord {
  return {
    id: s.id,
    filename: s.filename,
    size: `${(s.file_size_bytes / 1_048_576).toFixed(1)} MB`,
    status: STATUS[s.status],
    stage: STAGE[s.status],
    uploadedAt: s.uploaded_at,
  }
}

export default function UploadPage() {
  const queryClient = useQueryClient()
  const [dragging, setDragging] = useState(false)
  const [pending, setPending] = useState<UploadRecord[]>([])
  const [deleting, setDeleting] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // History from the API — polled so worker-processed saves flip to "done".
  const { data: serverSaves } = useQuery({
    queryKey: ['saves'],
    queryFn: () => savesApi.getAll(0, 20),
    retry: 2,
    refetchOnWindowFocus: false,
    refetchInterval: 4000,
  })

  const items: UploadRecord[] = [...pending, ...(serverSaves ?? []).map(toRecord)]

  const ingest = useCallback(
    (files: FileList | null) => {
      if (!files || files.length === 0) return

      Array.from(files).forEach(async (file) => {
        const tempId = `tmp_${Math.random().toString(36).slice(2, 8)}`
        setPending((prev) => [
          {
            id: tempId,
            filename: file.name,
            size: `${(file.size / 1_048_576).toFixed(1)} MB`,
            status: 'processing',
            stage: 'Bronze',
            uploadedAt: new Date().toISOString(),
          },
          ...prev,
        ])

        try {
          const saved = await savesApi.upload(file)
          setCurrentPlayerId(saved.player_id)
          setPending((prev) => prev.filter((it) => it.id !== tempId))
          queryClient.invalidateQueries({ queryKey: ['saves'] })
        } catch {
          setPending((prev) =>
            prev.map((it) => (it.id === tempId ? { ...it, status: 'failed', stage: 'Bronze' } : it)),
          )
        }
      })
    },
    [queryClient],
  )

  const remove = useCallback(
    async (id: string) => {
      setDeleting(id)
      try {
        await savesApi.delete(id)
        await queryClient.invalidateQueries({ queryKey: ['saves'] })
      } catch {
        // ignore — the row stays; the poll will reconcile
      } finally {
        setDeleting(null)
      }
    },
    [queryClient],
  )

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Dados & plataforma"
        title="Enviar Save"
        description="Envie o save de Life is Strange. Ele entra no pipeline event-driven e vira analytics."
      />

      <div className="grid gap-4 lg:grid-cols-3">
        {/* Dropzone */}
        <Card className="lg:col-span-2">
          <CardBody>
            <div
              role="button"
              tabIndex={0}
              onClick={() => inputRef.current?.click()}
              onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && inputRef.current?.click()}
              onDragOver={(e) => {
                e.preventDefault()
                setDragging(true)
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={(e) => {
                e.preventDefault()
                setDragging(false)
                ingest(e.dataTransfer.files)
              }}
              className={cn(
                'flex cursor-pointer flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed px-6 py-16 text-center transition-colors',
                dragging
                  ? 'border-amber/60 bg-amber/[0.06]'
                  : 'border-line-strong bg-bg hover:border-white/25 hover:bg-white/[0.02]',
              )}
            >
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-amber/25 bg-amber/10 text-amber">
                <UploadCloud className="h-7 w-7" />
              </div>
              <div>
                <p className="text-base font-medium">Arraste o arquivo aqui</p>
                <p className="mt-1 text-sm text-content-tertiary">
                  ou <span className="text-amber">clique para selecionar</span> · máx. 25 MB
                </p>
              </div>
              <input
                ref={inputRef}
                type="file"
                multiple
                accept=".sav,.json,.zip"
                className="hidden"
                onChange={(e) => ingest(e.target.files)}
              />
            </div>

            {/* Pipeline */}
            <div className="mt-6">
              <p className="text-2xs font-semibold uppercase tracking-[0.14em] text-content-faint">
                O que acontece depois
              </p>
              <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
                {pipeline.map((s, i) => (
                  <div key={s.label} className="relative rounded-lg border border-line bg-bg-subtle p-3">
                    <div className="flex h-7 w-7 items-center justify-center rounded-md border border-line bg-white/[0.02] text-content-secondary">
                      <s.icon className="h-3.5 w-3.5" />
                    </div>
                    <p className="mt-3 text-[13px] font-medium">{s.label}</p>
                    <p className="mt-0.5 text-2xs text-content-tertiary">{s.tech}</p>
                    {i < pipeline.length - 1 && (
                      <div className="absolute right-[-9px] top-1/2 hidden h-px w-3 -translate-y-1/2 bg-line-strong sm:block" />
                    )}
                  </div>
                ))}
              </div>
            </div>
          </CardBody>
        </Card>

        {/* Formats */}
        <Card>
          <CardHeader title="Formatos suportados" />
          <CardBody className="space-y-3">
            {supportedFormats.map((f) => (
              <div key={f.ext} className="flex items-center gap-3 rounded-lg border border-line bg-bg px-4 py-3">
                <span className="rounded-md border border-teal/25 bg-teal/10 px-2 py-0.5 font-mono text-2xs font-medium text-teal">
                  {f.ext}
                </span>
                <span className="text-sm text-content-secondary">{f.label}</span>
              </div>
            ))}
            <p className="pt-1 text-2xs leading-relaxed text-content-faint">
              O arquivo é enviado à API, gera um evento no Kafka e é armazenado na camada Bronze do
              Data Lake antes de ser transformado.
            </p>
          </CardBody>
        </Card>
      </div>

      {/* History */}
      <Card className="overflow-hidden">
        <CardHeader
          title="Histórico de uploads"
          action={<span className="text-2xs text-content-faint">{items.length} arquivos</span>}
        />
        <div className="divide-y divide-line">
          <AnimatePresence initial={false}>
            {items.map((it) => (
              <motion.div
                key={it.id}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0 }}
                className="flex items-center justify-between gap-4 px-6 py-4"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <StatusIcon status={it.status} />
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{it.filename}</p>
                    <p className="text-2xs text-content-faint">
                      {it.size} · camada {it.stage} · {formatRelativeTime(it.uploadedAt)}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <StatusPill status={it.status} pulse={it.status === 'processing'} />
                  {!it.id.startsWith('tmp_') && (
                    <button
                      type="button"
                      onClick={() => remove(it.id)}
                      disabled={deleting === it.id}
                      aria-label="Excluir save"
                      className="flex h-8 w-8 items-center justify-center rounded-md text-content-faint transition-colors hover:bg-sunset/10 hover:text-sunset disabled:opacity-40"
                    >
                      {deleting === it.id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Trash2 className="h-4 w-4" />
                      )}
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </Card>
    </div>
  )
}

function StatusIcon({ status }: { status: UploadRecord['status'] }) {
  if (status === 'done') return <CheckCircle2 className="h-5 w-5 shrink-0 text-teal" />
  if (status === 'failed') return <XCircle className="h-5 w-5 shrink-0 text-sunset" />
  return <Loader2 className="h-5 w-5 shrink-0 animate-spin text-amber" />
}
