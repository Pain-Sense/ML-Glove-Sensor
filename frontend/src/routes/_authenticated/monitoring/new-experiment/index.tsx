import MonitoringNewExperiment from '@/features/monitoring/new-experiment'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/_authenticated/monitoring/new-experiment/'
)({
  component: MonitoringNewExperiment,
})
