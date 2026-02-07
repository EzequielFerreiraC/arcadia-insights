'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { ArrowLeft, Menu, X } from 'lucide-react'
import { Butterfly } from '@/components/brand/Logo'
import { navGroups } from '@/config/nav'
import { cn } from '@/lib/utils'

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)

  // Close the drawer whenever the route changes.
  useEffect(() => {
    setMobileOpen(false)
  }, [pathname])

  return (
    <div className="min-h-screen">
      {/* ===== Sidebar (desktop) ===== */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r border-line bg-bg-subtle/60 backdrop-blur-xl lg:flex">
        <SidebarContent pathname={pathname} />
      </aside>

      {/* ===== Mobile top bar ===== */}
      <div className="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-line bg-bg/80 px-4 backdrop-blur-xl lg:hidden">
        <Link href="/" className="flex items-center gap-2.5">
          <Butterfly className="h-6 w-6" />
          <span className="font-display text-[15px] font-semibold tracking-tight">Arcadia Insights</span>
        </Link>
        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="btn-ghost h-9 w-9 px-0"
          aria-label="Abrir menu"
        >
          <Menu className="h-5 w-5" />
        </button>
      </div>

      {/* ===== Mobile drawer ===== */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm lg:hidden"
            />
            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', bounce: 0, duration: 0.35 }}
              className="fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-line bg-bg-elevated lg:hidden"
            >
              <button
                type="button"
                onClick={() => setMobileOpen(false)}
                className="btn-ghost absolute right-3 top-3 h-9 w-9 px-0"
                aria-label="Fechar menu"
              >
                <X className="h-5 w-5" />
              </button>
              <SidebarContent pathname={pathname} />
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* ===== Main ===== */}
      <div className="lg:pl-64">
        <main className="container-page py-8 lg:py-10">{children}</main>
      </div>
    </div>
  )
}

function SidebarContent({ pathname }: { pathname: string }) {
  return (
    <div className="flex h-full flex-col">
      <Link href="/" className="flex h-14 items-center gap-2.5 border-b border-line px-5">
        <Butterfly className="h-7 w-7" />
        <span className="font-display text-[16px] font-semibold tracking-tight">Arcadia Insights</span>
      </Link>

      <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-5">
        <Link
          href="/"
          className="group flex items-center gap-3 rounded-md px-3 py-2 text-[13px] font-medium text-content-tertiary transition-colors hover:bg-white/[0.03] hover:text-content-secondary"
        >
          <ArrowLeft className="h-4 w-4 shrink-0 text-content-faint group-hover:text-content-tertiary" />
          Voltar para a home
        </Link>

        {navGroups.map((group) => (
          <div key={group.title}>
            <p className="px-3 text-2xs font-semibold uppercase tracking-[0.14em] text-content-faint">
              {group.title}
            </p>
            <ul className="mt-2 space-y-0.5">
              {group.items.map((item) => {
                const active = pathname === item.href
                const Icon = item.icon
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={cn(
                        'group flex items-center gap-3 rounded-md px-3 py-2 text-[13px] font-medium transition-colors',
                        active
                          ? 'bg-white/[0.06] text-content-primary'
                          : 'text-content-tertiary hover:bg-white/[0.03] hover:text-content-secondary',
                      )}
                    >
                      <Icon className={cn('h-4 w-4 shrink-0', active ? 'text-amber' : 'text-content-faint group-hover:text-content-tertiary')} />
                      {item.label}
                    </Link>
                  </li>
                )
              })}
            </ul>
          </div>
        ))}
      </nav>

      <div className="border-t border-line p-3">
        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-secondary h-9 w-full text-[13px]"
        >
          Documentação da API
        </a>
      </div>
    </div>
  )
}
