import { useEffect, useRef, useState } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

interface MetricEntry {
  field: string
  experimentId: string
  time: string
  value: number
  deviceId: string
}

interface MetricCardsProps {
  data: MetricEntry[]
  maxPoints?: number
}

export const MetricCards: React.FC<MetricCardsProps> = ({
  data,
  maxPoints = 100,
}) => {
  const [groupedData, setGroupedData] = useState<Record<string, MetricEntry[]>>(
    {}
  )
  const historyRef = useRef<Record<string, MetricEntry[]>>({})

  useEffect(() => {
    const updated: Record<string, MetricEntry[]> = { ...historyRef.current }

    for (const point of data) {
      const field = point.field
      if (!updated[field]) updated[field] = []

      const exists = updated[field].some((e) => e.time === point.time)
      if (!exists) {
        updated[field].push(point)
      }

      if (updated[field].length > maxPoints) {
        updated[field] = updated[field].slice(-maxPoints)
      }
    }

    historyRef.current = updated
    setGroupedData({ ...updated })
  }, [data, maxPoints])

  return (
    <div className='grid grid-cols-1 gap-4 md:grid-cols-3'>
      {Object.entries(groupedData).map(([field, entries]) => {
        const latest = entries[entries.length - 1]

        return (
          <Card key={field}>
            <CardHeader>
              <CardTitle className='capitalize'>
                {field.toUpperCase()}: {latest.value.toFixed(2)}
              </CardTitle>
            </CardHeader>
            <CardContent className='h-48'>
              <ResponsiveContainer width='100%' height='100%'>
                <LineChart data={entries}>
                  <XAxis dataKey='time' hide />
                  <YAxis domain={['auto', 'auto']} />
                  <Tooltip />
                  <Line
                    type='monotone'
                    dataKey='value'
                    stroke='#8884d8'
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
