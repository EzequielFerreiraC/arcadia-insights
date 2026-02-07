'use client'

import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { accentHex } from '@/lib/accents'
import type { Accent } from '@/types'

const tooltipStyle = {
  background: '#141b23',
  border: '1px solid rgba(255,255,255,0.12)',
  borderRadius: 10,
  fontSize: 12,
  color: 'rgba(247,244,238,0.95)',
}

export function TrendChart<T extends object>({
  data,
  xKey,
  yKey,
  accent = 'teal',
  height = 260,
}: {
  data: T[]
  xKey: Extract<keyof T, string>
  yKey: Extract<keyof T, string>
  accent?: Accent
  height?: number
}) {
  const color = accentHex[accent]
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
        <defs>
          <linearGradient id={`trend-${accent}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.35} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fill: 'rgba(247,244,238,0.42)', fontSize: 12 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: 'rgba(247,244,238,0.42)', fontSize: 12 }} axisLine={false} tickLine={false} />
        <Tooltip contentStyle={tooltipStyle} cursor={{ stroke: 'rgba(255,255,255,0.12)' }} />
        <Area type="monotone" dataKey={yKey} stroke={color} strokeWidth={2} fill={`url(#trend-${accent})`} />
      </AreaChart>
    </ResponsiveContainer>
  )
}
