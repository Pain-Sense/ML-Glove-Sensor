/* eslint-disable @typescript-eslint/ban-ts-comment */
import { useEffect, useState } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { Button } from '@/components/ui/button'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import { Experiment } from './components/ExperimentSelector'
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
} from '@/components/ui/table'

export default function Dashboard() {
  const navigate = useNavigate()
  const [experiments, setExperiments] = useState<Experiment[]>([])

  const fetchExperiments = () => {
    fetch('http://localhost:8089/experiments')
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setExperiments(data)
        }
      })
  }

  useEffect(() => fetchExperiments(), [])

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

        <div className='flex w-full justify-end mt-2'>
          <Button onClick={() => navigate({ to: '/monitoring/new-experiment' })}>
            Start new experiment
          </Button>
        </div>

        {/* ===== Experiment Table ===== */}
        <section className='mt-10'>
          <h2 className='text-xl font-semibold mb-4'>Your Experiments</h2>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Patient ID</TableHead>
                <TableHead>Device ID</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {experiments.map((exp) => (
                <TableRow key={exp.id}>
                  <TableCell>{exp.id}</TableCell>
                  <TableCell>{exp.name}</TableCell>
                  {/* @ts-ignore */}
                  <TableCell>{exp.patientId}</TableCell>
                  {/* @ts-ignore */}
                  <TableCell>{exp.deviceId}</TableCell>
                  {/* @ts-ignore */}
                  <TableCell>{exp.stopped ? 'Stopped' : 'Running'}</TableCell>
                  <TableCell>
                    <Button
                      variant='outline'
                      onClick={() => navigate({ to: `/monitoring/live/${exp.id}` })}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {experiments.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} className='text-center'>
                    No experiments found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </section>
      </Main>
    </>
  )
}
