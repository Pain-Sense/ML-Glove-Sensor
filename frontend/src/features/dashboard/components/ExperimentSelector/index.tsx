'use client'

import { useEffect, useState } from 'react'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export interface Experiment {
  id: number
  name: string
  notes: string
}

interface ExperimentSelectorProps {
  onChange: (experiment: Experiment) => void
}

export const ExperimentSelector: React.FC<ExperimentSelectorProps> = ({
  onChange,
}) => {
  const [experiments, setExperiments] = useState<Experiment[]>([])
  const [selectedExperimentId, setSelectedExperimentId] = useState<string | null>(
    null
  )

  const fetchExperiments = async () => {
    fetch('http://localhost:8089/experiments/notstopped')
      .then((res) => res.json())
      .then((data) => setExperiments(data))
      // eslint-disable-next-line no-console
      .catch((err) => console.error('Failed to fetch experiments', err))
  }

  useEffect(() => {
    fetchExperiments()
  }, [])

  useEffect(() => {
    if (selectedExperimentId) {
      const selected = experiments.find((p) => String(p.id) === selectedExperimentId)
      if (selected) {
        onChange(selected)
      }
    }
  }, [selectedExperimentId, experiments, onChange])

  return (
        <Select
          onValueChange={(value) => {
            setSelectedExperimentId(value)
          }}
        >
          <SelectTrigger>
            <SelectValue placeholder='Select experiment' />
          </SelectTrigger>
          <SelectContent>
            {experiments.map((e) => (
              <SelectItem key={e.id} value={String(e.id)}>
                {e.name} ({e.id})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
  )
}