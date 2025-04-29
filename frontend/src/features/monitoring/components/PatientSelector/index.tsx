"use client"

import { useEffect, useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export interface Patient {
  id: string
  name: string
  age: string
  sex: "male" | "female"
}

interface PatientSelectorProps {
  onChange: (patient: Patient) => void
}

export const PatientSelector: React.FC<PatientSelectorProps> = ({ onChange }) => {
  const [patients] = useState<Patient[]>([
    { id: "p1", name: "John Doe", age: "42", sex: "male" },
    { id: "p2", name: "Jane Smith", age: "35", sex: "female" },
  ])

  const [selectMode, setSelectMode] = useState<"select" | "create">("select")
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(null)

  const [patient, setPatient] = useState<Patient>({
    id: "",
    name: "",
    age: "",
    sex: "male",
  })

  useEffect(() => {
    if (selectedPatientId) {
      const selected = patients.find((p) => p.id === selectedPatientId)
      if (selected) {
        setPatient(selected)
        onChange(selected)
      }
    }
  }, [selectedPatientId, patients, onChange])

  useEffect(() => {
    if (selectMode === "create") {
      onChange(patient)
    }
  }, [patient, selectMode, onChange])

  return (
    <Card>
      <CardHeader>
        <CardTitle>Patient Info</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Patient Selector */}
        {selectMode === "select" && (
          <Select onValueChange={(value) => {
            if (value === "new") {
              setSelectMode("create")
              setSelectedPatientId(null)
              setPatient({ id: "", name: "", age: "", sex: "male" })
            } else {
              setSelectedPatientId(value)
            }
          }}>
            <SelectTrigger>
              <SelectValue placeholder="Select existing patient or add new" />
            </SelectTrigger>
            <SelectContent>
              {patients.map((p) => (
                <SelectItem key={p.id} value={p.id}>
                  {p.name} ({p.id})
                </SelectItem>
              ))}
              <SelectItem value="new">➕ Add New Patient</SelectItem>
            </SelectContent>
          </Select>
        )}

        {/* New Patient Form */}
        {selectMode === "create" && (
          <div className="space-y-4">
            <Input
              placeholder="Patient Name"
              value={patient.name}
              onChange={(e) => setPatient({ ...patient, name: e.target.value })}
            />
            <Input
              placeholder="Patient ID"
              value={patient.id}
              onChange={(e) => setPatient({ ...patient, id: e.target.value })}
            />
            <Input
              placeholder="Age"
              type="number"
              value={patient.age}
              onChange={(e) => setPatient({ ...patient, age: e.target.value })}
            />
            <div>
              <Label className="mb-1 block">Sex</Label>
              <RadioGroup
                defaultValue={patient.sex}
                onValueChange={(value) => setPatient({ ...patient, sex: value as "male" | "female" })}
                className="flex gap-4"
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="male" id="male" />
                  <Label htmlFor="male">Male</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="female" id="female" />
                  <Label htmlFor="female">Female</Label>
                </div>
              </RadioGroup>
            </div>
            <Button variant="ghost" onClick={() => {
              setSelectMode("select")
              setPatient({ id: "", name: "", age: "", sex: "male" })
            }}>
              ← Back to Patient List
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
