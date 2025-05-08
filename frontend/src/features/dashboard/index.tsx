import { useState } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import { Experiment, ExperimentSelector } from './components/ExperimentSelector'

export default function Dashboard() {
  const navigate = useNavigate()
  const [experiment, setExperiment] = useState<Experiment | null>(null)

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
        <div className='mb-2 flex items-center justify-between space-y-2'>
          <h1 className='text-2xl font-bold tracking-tight'>Dashboard</h1>
        </div>

        <div className='mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
          <Card>
            <CardHeader>
              <CardTitle>Start New Monitoring Experiment</CardTitle>
            </CardHeader>
            <CardContent>
              <p className='text-muted-foreground'>
                Begin a real-time monitoring experiment by selecting a patient
                and device.
              </p>
            </CardContent>
            <CardFooter>
              <ExperimentSelector onChange={(e) => setExperiment(e)}></ExperimentSelector>
            </CardFooter>
            <CardFooter>
              {experiment && (
                <Button
                  onClick={() => navigate({ to: `/monitoring/live/${experiment.id}` })}
                >
                  Start monitoring
                </Button>
              )}
            </CardFooter>
            <CardFooter>
              <Button
                onClick={() => navigate({ to: '/monitoring/new-experiment' })}
              >
                New experiment
              </Button>
            </CardFooter>
          </Card>
        </div>
      </Main>
    </>
  )
}
