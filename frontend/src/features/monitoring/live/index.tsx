import { useEffect, useRef, useState } from 'react'
import { useParams } from '@tanstack/react-router'
import { toast } from 'sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import { MetricCards } from '../components/MetricsCards'

export default function LiveMonitoring() {
  const { experimentId } = useParams({
    from: '/_authenticated/monitoring/live/$experimentId',
  })

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [metrics, setMetrics] = useState<any[]>([])
  const [isPaused, setIsPaused] = useState(false)
  const [isConnected, setIsConnected] = useState(true)
  const [pollingInterval, setPollingInterval] = useState(1000)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [experimentInfo, setExperimentInfo] = useState<any | null>(null)

  useEffect(() => {
    const fetchExperimentInfo = async () => {
      try {
        const res = await fetch(
          `http://localhost:8089/experiments/${experimentId}`
        )
        const data = await res.json()
        setExperimentInfo(data)
      } catch {
        toast.error('Failed to fetch experiment info')
      }
    }

    fetchExperimentInfo()
  }, [experimentId])

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch(
          `http://localhost:8089/experiments/${experimentId}/metrics`
        )
        const data = await res.json()
        setMetrics(data)
      } catch {
        toast.error('Failed to fetch live metrics')
        setIsConnected(false)
      }
    }

    if (!isPaused) {
      fetchMetrics()
    }

    if (intervalRef.current) clearInterval(intervalRef.current)
    intervalRef.current = setInterval(fetchMetrics, pollingInterval)

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [experimentId, pollingInterval, isPaused])

  const handleStop = async () => {
    try {
      await fetch(`http://localhost:8089/experiments/${experimentId}/stop`, {
        method: 'POST',
      })
      toast.success('Experiment stopped')
      setIsConnected(false)
      setIsPaused(true)
    } catch {
      toast.error('Failed to stop experiment')
    }
  }

  return (
    <>
      <Header>
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
        </div>
      </Header>

      <Main>
        <div className='mb-4 flex items-center justify-between'>
          <h1 className='text-2xl font-bold tracking-tight'>Live Monitoring</h1>
          <Badge variant={isConnected ? 'default' : 'destructive'}>
            {isConnected ? 'Connected' : 'Disconnected'}
          </Badge>
        </div>

        <div className='grid grid-cols-1 gap-6 md:grid-cols-3'>
          <Card className='md:col-span-1'>
            <CardHeader>
              <CardTitle>Session Info</CardTitle>
            </CardHeader>
            <CardContent className='space-y-2 text-sm'>
              <p>
                <strong>Experiment ID:</strong> {experimentId}
              </p>
              <p>
                <strong>Experiment name:</strong> {experimentInfo?.name || 'N/A'}
              </p>
              <p>
                <strong>Experiment Notes:</strong> {experimentInfo?.notes || 'N/A'}
              </p>
              <p>
                <strong>Patient ID:</strong>{' '}
                {experimentInfo?.patientId || 'N/A'}
              </p>
              <p>
                <strong>Device ID:</strong>{' '}
                {experimentInfo?.deviceId || 'N/A'}
              </p>
              <p>
                <strong>Status:</strong> {isPaused ? 'Paused' : 'Running'}
              </p>
            </CardContent>
          </Card>

          <Card className='md:col-span-2'>
            <CardHeader>
              <CardTitle>Data</CardTitle>
            </CardHeader>
            <CardContent>
              <MetricCards data={metrics} />
            </CardContent>
          </Card>
        </div>

        <div className='mt-6 flex flex-col items-end gap-4 md:flex-row md:justify-end'>
          <Select
            defaultValue='3000'
            onValueChange={(value) => setPollingInterval(Number(value))}
          >
            <SelectTrigger className='w-[180px]'>
              <SelectValue placeholder='Polling Interval' />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value='1000'>1 second</SelectItem>
              <SelectItem value='3000'>3 seconds</SelectItem>
              <SelectItem value='5000'>5 seconds</SelectItem>
              <SelectItem value='10000'>10 seconds</SelectItem>
            </SelectContent>
          </Select>

          <Button variant='outline' onClick={() => setIsPaused((p) => !p)}>
            {isPaused ? 'Resume' : 'Pause'}
          </Button>
          <Button variant='destructive' onClick={handleStop}>
            Stop
          </Button>
        </div>
      </Main>
    </>
  )
}
