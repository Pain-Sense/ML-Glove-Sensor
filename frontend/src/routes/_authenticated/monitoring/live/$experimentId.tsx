import LiveMonitoring from "@/features/monitoring/live"
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_authenticated/monitoring/live/$experimentId")({
  component: LiveMonitoring,
})
