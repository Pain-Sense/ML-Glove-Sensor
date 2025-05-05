import { useState } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import { Device, DeviceSelector } from '../components/DeviceSelector'
import { Patient, PatientSelector } from '../components/PatientSelector'

export default function MonitoringNewExperiment() {
  const navigate = useNavigate()

  const [patient, setPatient] = useState<Patient | null>(null)

  const [experiment, setExperiment] = useState({
    name: '',
    notes: '',
  })

  const [device, setDevice] = useState<string | null>(null)

  const handleStart = async () => {
    try {
      const res = await fetch('http://localhost:8089/experiments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: experiment.name,
          notes: experiment.notes,
          patientId: patient?.id,
          deviceId: Number(device),
        }),
      })

      if (!res.ok) {
        const errorText = await res.text()
        throw new Error(errorText || 'Failed to create experiment')
      }

      const data = await res.json()

      navigate({ to: `/monitoring/live/${data.id}` })
    } catch {
      toast('Experiment creation failed')
    }
  }

  const formComplete = patient?.name && patient?.id && experiment.name && device

  return (
    <>
      {/* ===== Top Heading ===== */}
      <Header>
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
        </div>
      </Header>

      {/* ===== Main ===== */}
      <Main>
        <div className='mb-4 flex items-center justify-between'>
          <h1 className='text-2xl font-bold tracking-tight'>New Experiment</h1>
        </div>

        <div className='space-y-6'>
          <PatientSelector onChange={(p) => setPatient(p)} />

          <Card>
            <CardHeader>
              <CardTitle>Experiment Details</CardTitle>
            </CardHeader>
            <CardContent className='space-y-4'>
              <Input
                placeholder='Experiment Name'
                value={experiment.name}
                onChange={(e) =>
                  setExperiment({ ...experiment, name: e.target.value })
                }
              />
              <Textarea
                placeholder='Notes'
                value={experiment.notes}
                onChange={(e) =>
                  setExperiment({ ...experiment, notes: e.target.value })
                }
              />
            </CardContent>
          </Card>

          <DeviceSelector
            onSelect={(d: Device) => {
              setDevice(d.id.toString())
            }}
          />

          {/* Start Monitoring */}
          <div className='text-right'>
            <Button onClick={handleStart} disabled={!formComplete}>
              Start Monitoring
            </Button>
          </div>
        </div>
      </Main>
    </>
  )
}
