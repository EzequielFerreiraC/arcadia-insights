'use client'

/** Tracks the "current player" id (set after a successful save upload). */
const KEY = 'arcadia.currentPlayerId'

export function getCurrentPlayerId(): string | null {
  if (typeof window === 'undefined') return null
  return window.localStorage.getItem(KEY)
}

export function setCurrentPlayerId(id: string): void {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(KEY, id)
}
