import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/_authenticated/monitoring/new-experiment/'
)({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/_authenticated/monitoring/new-experiment/"!</div>
}
