import { useParams } from "@tanstack/react-router"
import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/layout/header"
import { Main } from "@/components/layout/main"
import { ThemeSwitch } from "@/components/theme-switch"
import LiveECGChart from "../components/LiveECGChart"

export default function LiveMonitoring() {
  const { experimentId } = useParams({
    from: "/_authenticated/monitoring/live/$experimentId",
  })

  const [isPaused, setIsPaused] = useState(false)
  const [isConnected, setIsConnected] = useState(true)

  return (
    <>
      <Header>
        <div className="ml-auto flex items-center space-x-4">
          <ThemeSwitch />
        </div>
      </Header>

      <Main>
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-tight">Live Monitoring</h1>
          <Badge variant={isConnected ? "default" : "destructive"}>
            {isConnected ? "Connected" : "Disconnected"}
          </Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="md:col-span-1">
            <CardHeader>
              <CardTitle>Session Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p><strong>Experiment ID:</strong> {experimentId}</p>
              <p><strong>Patient:</strong> John Doe</p>
              <p><strong>Device:</strong> ECG Sensor #001</p>
              <p><strong>Status:</strong> {isPaused ? "Paused" : "Running"}</p>
            </CardContent>
          </Card>

          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>ECG Stream</CardTitle>
            </CardHeader>
            <CardContent>
              <LiveECGChart/>
            </CardContent>
          </Card>
        </div>

        <div className="mt-6 flex justify-end gap-4">
          <Button
            variant="outline"
            onClick={() => setIsPaused((p) => !p)}
          >
            {isPaused ? "Resume" : "Pause"}
          </Button>
          <Button
            variant="destructive"
            onClick={() => {
              setIsConnected(false)
              setIsPaused(true)
              // Maybe redirect or mark complete
            }}
          >
            Stop
          </Button>
        </div>
      </Main>
    </>
  )
}
