import { useEffect, useState } from 'react'
import { useParams } from '@tanstack/react-router'
import { toast } from 'sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import { GrafanaDashboards } from '../components/GrafanaDashboards'

export default function LiveMonitoring() {
  const { experimentId } = useParams({
    from: '/_authenticated/monitoring/live/$experimentId',
  })

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [isPaused, setIsPaused] = useState(false)
  const [isConnected, setIsConnected] = useState(true)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [experimentInfo, setExperimentInfo] = useState<any | null>(null)
  const [sensorStatus, setSensorStatus] = useState<any | null>(null)

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
    const fetchSensorData = async () => {
      if (experimentInfo){
        const res = await fetch(`http://localhost:8089/events/${experimentInfo.deviceId}`)
        if (res.ok){
          const data = await res.json()
          setSensorStatus(data)
        }
      }
    }
    const intervalId = setInterval(fetchSensorData, 1500)
    return () => clearInterval(intervalId)
  })

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
            </CardContent>
            {sensorStatus && !isPaused &&
              <CardFooter>
                <p>
                  ECG sensor: {sensorStatus.ecg ? 'on' : 'off'}
                </p>
                <p>
                  BVP sensor: {sensorStatus.bvp ? 'on' : 'off'}
                </p>
                <p>
                  GSR sensor: {sensorStatus.gsr ? 'on' : 'off'}
                </p>
              </CardFooter>
            }
          </Card>

          <Card className='md:col-span-2'>
            <CardHeader>
              <CardTitle>Data</CardTitle>
            </CardHeader>
            <CardContent>
              {!isPaused && experimentInfo &&
                <GrafanaDashboards deviceId={experimentInfo.deviceId}></GrafanaDashboards>
              }
            </CardContent>
          </Card>
        </div>

        <div className='mt-6 flex flex-col items-end gap-4 md:flex-row md:justify-end'>
          <Button variant='destructive' onClick={handleStop}>
            Stop
          </Button>
        </div>
      </Main>
    </>
  )
}
