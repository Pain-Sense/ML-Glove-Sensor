'use client'

import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export interface Device {
  id: number
  name: string
  type: string
  status: string
}

interface Props {
  onSelect: (device: Device) => void
}

export const DeviceSelector: React.FC<Props> = ({ onSelect }) => {
  const [devices, setDevices] = useState<Device[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [connected, setConnected] = useState(false)
  const [showDeviceNotAvailable, setShowDeviceNotAvailable] = useState(false)

  useEffect(() => {
    fetch('http://localhost:8089/devices')
      .then((res) => res.json())
      .then(setDevices)
      .catch(() => toast('Failed to load devices'))
  }, [])

  const handleTestConnection = async () => {
    if (!selectedId) return
    try {
      const res = await fetch(
        `http://localhost:8089/devices/${selectedId}/status`
      )
      const data = await res.json()
      setConnected(data.available)
      if (data.available) {
        const device = devices.find((d) => d.id.toString() === selectedId)
        if (device) onSelect(device)

          toast.success('Device is ONLINE', {
            duration: 4000,
            position: 'top-right',
            richColors: true,
            dismissible: true
          })
      } else {
        setShowDeviceNotAvailable(true)

        toast.error('Device is OFFLINE', {
          duration: 4000,
          position: 'top-right',
          richColors: true
        })

        setTimeout(() => {
          setShowDeviceNotAvailable(false)
        }, 4000)
      }
    } catch {
      toast('Failed to check device status')
      setConnected(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Select Device</CardTitle>
      </CardHeader>
      <CardContent className='space-y-4'>
        <Select
          onValueChange={(val) => {
            setSelectedId(val)
            setConnected(false)
            setShowDeviceNotAvailable(false)
          }}
        >
          <SelectTrigger>
            <SelectValue placeholder='Select a device' />
          </SelectTrigger>
          <SelectContent>
            {devices.map((d) => (
              <SelectItem key={d.id} value={d.id.toString()}>
                {d.name} (#{d.id})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Button variant='outline' onClick={handleTestConnection}>
          {connected ? 'Device Connected ✅' : 'Test Connection'}
        </Button>
        {showDeviceNotAvailable && (
          <p className='text-red-500'>
            Device is not available. Please select another device.
          </p>
        )}
      </CardContent>
    </Card>
  )
}
