'use client'

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { chartPalette } from '@/lib/accents'

const tooltipStyle = {
  background: '#141b23',
  border: '1px solid rgba(255,255,255,0.12)',
  borderRadius: 10,
  fontSize: 12,
  color: 'rgba(247,244,238,0.95)',
}

export function DonutChart<T extends object>({
  data,
  nameKey,
  valueKey,
  height = 260,
  colors = chartPalette,
}: {
  data: T[]
  nameKey: Extract<keyof T, string>
  valueKey: Extract<keyof T, string>
  height?: number
  colors?: string[]
}) {
  return (
    <div className="flex flex-col items-center gap-6 sm:flex-row">
      <ResponsiveContainer width="100%" height={height} className="max-w-[240px]">
        <PieChart>
          <Pie
            data={data}
            dataKey={valueKey}
            nameKey={nameKey}
            innerRadius="58%"
            outerRadius="88%"
            paddingAngle={2}
            stroke="none"
          >
            {data.map((_, i) => (
              <Cell key={i} fill={colors[i % colors.length]} />
            ))}
          </Pie>
          <Tooltip contentStyle={tooltipStyle} />
        </PieChart>
      </ResponsiveContainer>

      <ul className="w-full space-y-2.5">
        {data.map((d, i) => (
          <li key={i} className="flex items-center justify-between text-sm">
            <span className="flex items-center gap-2.5 text-content-secondary">
              <span className="h-2.5 w-2.5 rounded-sm" style={{ background: colors[i % colors.length] }} />
              {String(d[nameKey])}
            </span>
            <span className="tabular-nums text-content-tertiary">{Number(d[valueKey]).toLocaleString('pt-BR')}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
