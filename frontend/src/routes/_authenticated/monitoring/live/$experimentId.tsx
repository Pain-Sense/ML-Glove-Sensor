import { createFileRoute } from '@tanstack/react-router'
import LiveMonitoring from '@/features/monitoring/live'

export const Route = createFileRoute(
  '/_authenticated/monitoring/live/$experimentId'
)({
  component: LiveMonitoring,
})
