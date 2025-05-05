'use client'

import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export interface Patient {
  id: number
  name: string
  age: string
  gender: 'male' | 'female'
  health_condition?: string
}

interface PatientSelectorProps {
  onChange: (patient: Patient) => void
}

export const PatientSelector: React.FC<PatientSelectorProps> = ({
  onChange,
}) => {
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectMode, setSelectMode] = useState<'select' | 'create'>('select')
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(
    null
  )

  const [patient, setPatient] = useState<Patient>({
    id: 0,
    name: '',
    age: '',
    gender: 'male',
    health_condition: '',
  })

  const fetchPatients = async () => {
    fetch('http://localhost:8089/patients')
      .then((res) => res.json())
      .then((data) => setPatients(data))
      // eslint-disable-next-line no-console
      .catch((err) => console.error('Failed to fetch patients', err))
  }

  useEffect(() => {
    fetchPatients()
  }, [])

  useEffect(() => {
    if (selectedPatientId) {
      const selected = patients.find((p) => String(p.id) === selectedPatientId)
      if (selected) {
        setPatient(selected)
        onChange(selected)
      }
    }
  }, [selectedPatientId, patients, onChange])

  useEffect(() => {
    if (selectMode === 'create') {
      onChange(patient)
    }
  }, [patient, selectMode, onChange])

  return (
    <Card>
      <CardHeader>
        <CardTitle>Patient Info</CardTitle>
      </CardHeader>
      <CardContent className='space-y-4'>
        {selectMode === 'select' && (
          <Select
            onValueChange={(value) => {
              if (value === 'new') {
                setSelectMode('create')
                setSelectedPatientId(null)
                setPatient({
                  id: 0,
                  name: '',
                  age: '',
                  gender: 'male',
                  health_condition: '',
                })
              } else {
                setSelectedPatientId(value)
              }
            }}
          >
            <SelectTrigger>
              <SelectValue placeholder='Select existing patient or add new' />
            </SelectTrigger>
            <SelectContent>
              {patients.map((p) => (
                <SelectItem key={p.id} value={String(p.id)}>
                  {p.name} ({p.id})
                </SelectItem>
              ))}
              <SelectItem value='new'>➕ Add New Patient</SelectItem>
            </SelectContent>
          </Select>
        )}

        {selectMode === 'create' && (
          <div className='space-y-4'>
            <Input
              placeholder='Patient Name'
              value={patient.name}
              onChange={(e) => setPatient({ ...patient, name: e.target.value })}
            />
            <Input
              placeholder='Age'
              type='number'
              value={patient.age}
              onChange={(e) => setPatient({ ...patient, age: e.target.value })}
            />
            <Input
              placeholder='Health Condition'
              value={patient.health_condition}
              onChange={(e) =>
                setPatient({ ...patient, health_condition: e.target.value })
              }
            />
            <div>
              <Label className='mb-1 block'>Gender</Label>
              <RadioGroup
                defaultValue={patient.gender}
                onValueChange={(value) =>
                  setPatient({ ...patient, gender: value as 'male' | 'female' })
                }
                className='flex gap-4'
              >
                <div className='flex items-center space-x-2'>
                  <RadioGroupItem value='male' id='male' />
                  <Label htmlFor='male'>Male</Label>
                </div>
                <div className='flex items-center space-x-2'>
                  <RadioGroupItem value='female' id='female' />
                  <Label htmlFor='female'>Female</Label>
                </div>
              </RadioGroup>
            </div>

            <div className='flex gap-4'>
              <Button
                onClick={async () => {
                  try {
                    const res = await fetch('http://localhost:8089/patients', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                        name: patient.name,
                        age: patient.age,
                        gender: patient.gender,
                        health_condition: 'N/A',
                      }),
                    })

                    if (!res.ok) throw new Error('Failed to create patient')

                    const saved = await res.json()
                    onChange(saved)
                    toast('Patient created successfully!')
                    setSelectMode('select')
                    fetchPatients()
                  } catch {
                    toast('Failed to create patient')
                  }
                }}
              >
                ✅ Create Patient
              </Button>
              <Button
                variant='ghost'
                onClick={() => {
                  setSelectMode('select')
                  setPatient({ id: 0, name: '', age: '', gender: 'male' })
                }}
              >
                ← Back to Patient List
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
