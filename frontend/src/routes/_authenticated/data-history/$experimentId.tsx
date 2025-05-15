import { createFileRoute } from '@tanstack/react-router'
import DataHistoryView from '@/features/datahistory/view'

export const Route = createFileRoute(
  '/_authenticated/data-history/$experimentId'
)({
  component: DataHistoryView,
})
