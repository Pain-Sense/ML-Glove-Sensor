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

export default function Dashboard() {
  const navigate = useNavigate()

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
                Begin a real-time monitoring experiment by selecting a patient and
                device.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                onClick={() => navigate({ to: '/monitoring/new-experiment' })}
              >
                Start Monitoring
              </Button>
            </CardFooter>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Create New Patient</CardTitle>
            </CardHeader>
            <CardContent>
              <p className='text-muted-foreground'>
                Add a new patient to the system by entering basic details.
              </p>
            </CardContent>
            <CardFooter className='mt-auto'>
              <Button onClick={() => {}}>Create Patient</Button>
            </CardFooter>
          </Card>
        </div>
      </Main>
    </>
  )
}
