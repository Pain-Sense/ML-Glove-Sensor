import { useState } from "react"
import { useNavigate } from "@tanstack/react-router"
import { Header } from "@/components/layout/header"
import { Main } from "@/components/layout/main"
import { ThemeSwitch } from "@/components/theme-switch"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Patient, PatientSelector } from "../components/PatientSelector"

export default function MonitoringNewExperiment() {
  const navigate = useNavigate()

  const [patient, setPatient] = useState<Patient | null>(null)


  const [experiment, setExperiment] = useState({
    name: "",
    notes: "",
  })

  const [device, setDevice] = useState<string | null>(null)
  const [deviceConnected, setDeviceConnected] = useState(false)

  const handleTestConnection = () => {
    setTimeout(() => setDeviceConnected(true), 500)
  }

  const handleStart = () => {
    const newExperimentId = crypto.randomUUID()
    navigate({ to: `/monitoring/live/${newExperimentId}` })
  }

  const formComplete =
    patient?.name && patient?.id && experiment.name && device && deviceConnected

  return (
    <>
      {/* ===== Top Heading ===== */}
      <Header>
        <div className="ml-auto flex items-center space-x-4">
          <ThemeSwitch />
        </div>
      </Header>

      {/* ===== Main ===== */}
      <Main>
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-tight">New Experiment</h1>
        </div>

        <div className="space-y-6">
          <PatientSelector onChange={(p) => setPatient(p)}/>

          <Card>
            <CardHeader>
              <CardTitle>Experiment Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input
                placeholder="Experiment Name"
                value={experiment.name}
                onChange={(e) => setExperiment({ ...experiment, name: e.target.value })}
              />
              <Textarea
                placeholder="Notes"
                value={experiment.notes}
                onChange={(e) => setExperiment({ ...experiment, notes: e.target.value })}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Select Device</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Select onValueChange={(value) => setDevice(value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a device" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ecg-001">ECG Sensor #001</SelectItem>
                  <SelectItem value="ecg-002">ECG Sensor #002</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline" onClick={handleTestConnection}>
                {deviceConnected ? "Device Connected ✅" : "Test Connection"}
              </Button>
            </CardContent>
          </Card>

          {/* Start Monitoring */}
          <div className="text-right">
            <Button onClick={handleStart} disabled={!formComplete}>
              Start Monitoring
            </Button>
          </div>
        </div>
      </Main>
    </>
  )
}
