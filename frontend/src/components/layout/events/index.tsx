import { useEffect, useState } from "react"
import { toast, ToastContainer } from "react-toastify";

export default function EventReader() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetch('http://localhost:8089/events')
                const res = await response.json()
                if (res.event === 'sensor-off')
                    setMessage(`Device with id ${res.deviceId} is offline`)
                else if (res.event === 'sensor-on')
                    setMessage(`Device with id ${res.deviceId} is online`)
            } catch (error) {
                console.error('Error fetching events:',error)
            }
        }
        fetchEvents()
        if (message) {
            toast(message)
        }
        setMessage(null)
    },[])

    return <ToastContainer/>
}