import DataHistoryDashboard from '@/features/datahistory/dashboard'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/_authenticated/data-history/'
)({
  component: DataHistoryDashboard,
})