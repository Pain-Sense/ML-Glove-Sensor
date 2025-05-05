import { createFileRoute } from '@tanstack/react-router'
import MonitoringNewExperiment from '@/features/monitoring/new-experiment'

export const Route = createFileRoute(
  '/_authenticated/monitoring/new-experiment/'
)({
  component: MonitoringNewExperiment,
})
