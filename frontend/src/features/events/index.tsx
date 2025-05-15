import { useEffect, useState } from "react"

export default function EventReader() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetch('http://localhost:8089/events')
                const res = await response.json()
                if (res.event === 'sensor-off')
                setMessage(`Device with id ${res.deviceId} is offline`)
            } catch (error) {
                console.error('Error fetching events:',error)
            }
        }
        fetchEvents()
    },[])

    return (
        <div>{message}</div>
    )
}