"use client"

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"
import { useEffect, useState } from "react"

type DataPoint = { t: number; value: number }

export default function LiveECGChart() {
  const [data, setData] = useState<DataPoint[]>([])
  const [t, setT] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      const newPoint = {
        t,
        value: Math.sin(t / 5) + Math.random() * 0.2, // Simulated ECG-like data
      }

      setData((prev) => [...prev, newPoint])
      setT((prev) => prev + 1)
    }, 100)

    return () => clearInterval(interval)
  }, [t])

  return (
    <div className="h-40 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="t" tick={{ fontSize: 10 }} />
          <YAxis domain={[-2, 2]} tick={{ fontSize: 10 }} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="currentColor"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
