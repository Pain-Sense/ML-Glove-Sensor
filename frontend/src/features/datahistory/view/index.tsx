import { useEffect, useState } from 'react'
import { useParams } from '@tanstack/react-router'
import { toast } from 'sonner'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import Dashboards from './components/Dashboards'

export default function DataHistoryView() {
  const { experimentId } = useParams({
    from: '/_authenticated/data-history/$experimentId',
  })

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

  return (
    <>
      <Header>
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
        </div>
      </Header>

      <Main>
        <div className='mb-4 flex items-center justify-between'>
          <h1 className='text-2xl font-bold tracking-tight'>Data history</h1>
        </div>

        <div className='flex flex-col gap-4'>
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
          </Card>

          <Card className='md:col-span-2'>
            <CardHeader>
              <CardTitle>Data</CardTitle>
            </CardHeader>
            <CardContent>
              <Dashboards patientId={experimentInfo?.patientId} deviceId={experimentInfo?.deviceId} experimentId={experimentId} />
            </CardContent>
          </Card>
        </div>
      </Main>
    </>
  )
}
