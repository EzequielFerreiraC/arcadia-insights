'use client'

import {
  Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis,
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

export function ColumnChart<T extends object>({
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
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fill: 'rgba(247,244,238,0.42)', fontSize: 12 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: 'rgba(247,244,238,0.42)', fontSize: 12 }} axisLine={false} tickLine={false} />
        <Tooltip contentStyle={tooltipStyle} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
        <Bar dataKey={yKey} radius={[6, 6, 0, 0]} fill={accentHex[accent]} maxBarSize={48} />
      </BarChart>
    </ResponsiveContainer>
  )
}

export function ColumnChartMulti<T extends object>({
  data,
  xKey,
  yKey,
  colors,
  height = 260,
}: {
  data: T[]
  xKey: Extract<keyof T, string>
  yKey: Extract<keyof T, string>
  colors: string[]
  height?: number
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fill: 'rgba(247,244,238,0.42)', fontSize: 12 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: 'rgba(247,244,238,0.42)', fontSize: 12 }} axisLine={false} tickLine={false} />
        <Tooltip contentStyle={tooltipStyle} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
        <Bar dataKey={yKey} radius={[6, 6, 0, 0]} maxBarSize={48}>
          {data.map((_, i) => (
            <Cell key={i} fill={colors[i % colors.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
