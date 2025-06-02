import { useEffect, useState } from 'react'
import { useParams, useRouter } from '@tanstack/react-router'
import { toast } from 'sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CardTitle } from '@/components/ui/card'

import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import Dashboards from '../components/Dashboards'
import HistoricalDashboards from '../components/HistoricalDashboards'

export default function LiveMonitoring() {
  const { experimentId } = useParams({
    from: '/_authenticated/monitoring/live/$experimentId',
  })

  const router = useRouter()

  const [isConnected, setIsConnected] = useState(true)
  const [isStopped, setIsStopped] = useState(false)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [experimentInfo, setExperimentInfo] = useState<any | null>(null)
  const [experimentFields, setExperimentFields] = useState<string[]>([])
  const [processingFields, setProcessingFields] = useState<string[]>([])
  const [deviceStatus, setDeviceStatus] = useState<'online' | 'offline'>('online')

  useEffect(() => {
    const fetchExperimentInfo = async () => {
      try {
        const res = await fetch(
          `http://localhost:8089/experiments/${experimentId}`
        )
        const data = await res.json()
        setExperimentInfo(data)

        if (data.stopped) {
          await fetch(`http://localhost:8089/experiments/${experimentId}/metrics/fields/grouped`).then((res) => res.json()).then(data => setProcessingFields(data))
          setIsConnected(false)
          setIsStopped(true)
        }
      } catch {
        toast.error('Failed to fetch experiment info', {
          duration: 2000,
          dismissible: true,
        })
        router.navigate({ to: '/404' })
      }
    }

    fetchExperimentInfo()
  }, [])

  useEffect(() => {
    if (!experimentId) return;

    const timeoutId = setTimeout(() => {
      const fetchFields = async () => {

        try {
          const response = await fetch(`http://localhost:8089/experiments/${experimentId}/metrics/fields`);
          if (!response.ok) {
            throw new Error(`Failed to fetch fields: ${response.statusText}`);
          }

          const data = await response.json();
          setExperimentFields(data);
        } catch {
          //
        } 
      };

      fetchFields();
    }, 2000);

    return () => clearTimeout(timeoutId);
  }, []);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (!experimentInfo?.deviceId) return;

      try {
        const response = await fetch('http://localhost:8089/devices/events');
        const data = await response.json()

        const device = data.find((id: string) => id === String(experimentInfo?.deviceId))

        if (device) {
          setDeviceStatus('offline')
          setIsConnected(false)
          toast.error('Device is OFFLINE', {
            duration: 4000,
            position: 'top-right',
            richColors: true,
            dismissible: true,
          })
        } else if (deviceStatus === 'offline' && !device) {
          setDeviceStatus('online')
          setIsConnected(true)
          toast.success('Device is ONLINE', {
            duration: 4000,
            position: 'top-right',
            richColors: true,
            dismissible: true,
          })
        }
      } catch {
        //
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [deviceStatus, experimentInfo?.deviceId])

  const handleStop = async () => {
    try {
      await fetch(`http://localhost:8089/experiments/${experimentId}/stop`, {
        method: 'POST',
      })
      await fetch(`http://localhost:8089/experiments/${experimentId}/metrics/fields/grouped`).then((res) => res.json()).then(data => setProcessingFields(data))
      toast.success('Experiment stopped', {
        dismissible: true,
        duration: 1000,
      })
      setIsConnected(false)
      setIsStopped(true)
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
          <h1 className='text-2xl font-bold tracking-tight'> {isStopped ? 'Historical Data' : 'Live Monitoring'}</h1>

          <div className='flex items-center space-x-2'>
            <Badge variant={isConnected ? 'default' : 'destructive'} className={isConnected ?'bg-green-400' : ''}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </Badge>


            {!isStopped && (
              <Button variant='destructive' onClick={handleStop}>
                Stop Experiment
              </Button>
            )} 
          </div>
        </div>

        <CardTitle>Session Info</CardTitle>
        <div className='space-y-2 flex gap-2 text-sm mt-2'>
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
        </div>


        {isStopped ? (
          <>
          <p className='mt-4 text-sm text-muted-foreground'>
            The experiment has been stopped. You can view historical data below.
          </p>
            <HistoricalDashboards deviceId={experimentInfo?.deviceId} experimentId={experimentId} patientId={experimentInfo?.patientId} fields={experimentFields} processingFields={processingFields} />
          </>
        ) : (
          <Dashboards deviceId={experimentInfo?.deviceId} fields={experimentFields} />
        )}

      </Main>
    </>
  )
}
