'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Butterfly } from '@/components/brand/Logo'

const links = [
  { href: '/', label: 'Visão geral' },
  { href: '/stats', label: 'Estatísticas' },
  { href: '/dashboard', label: 'Dashboard' },
]

export function Navbar() {
  const pathname = usePathname()
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <div
        className={`transition-colors duration-300 ${
          scrolled ? 'border-b border-line bg-bg/70 backdrop-blur-xl' : 'border-b border-transparent'
        }`}
      >
        <div className="container-page">
          <nav className="flex h-14 items-center justify-between">
            {/* Brand */}
            <Link href="/" className="flex items-center gap-2.5">
              <Butterfly className="h-7 w-7" />
              <span className="font-display text-[17px] font-semibold tracking-tight text-content-primary">
                Arcadia Insights
              </span>
            </Link>

            {/* Center links */}
            <div className="absolute left-1/2 hidden -translate-x-1/2 items-center gap-1 md:flex">
              {links.map(({ href, label }) => {
                const active = pathname === href
                return (
                  <Link
                    key={href}
                    href={href}
                    className={`relative rounded-md px-3 py-1.5 text-[13px] font-medium transition-colors ${
                      active ? 'text-content-primary' : 'text-content-tertiary hover:text-content-secondary'
                    }`}
                  >
                    {active && (
                      <motion.span
                        layoutId="nav-active"
                        className="absolute inset-0 rounded-md bg-white/[0.06]"
                        transition={{ type: 'spring', bounce: 0.15, duration: 0.5 }}
                      />
                    )}
                    <span className="relative">{label}</span>
                  </Link>
                )
              })}
            </div>

            {/* Right actions */}
            <div className="flex items-center gap-2">
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-ghost hidden sm:inline-flex text-[13px]"
              >
                API
              </a>
              <Link href="/dashboard" className="btn-primary text-[13px]">
                Abrir dashboard
              </Link>
            </div>
          </nav>
        </div>
      </div>
    </header>
  )
}