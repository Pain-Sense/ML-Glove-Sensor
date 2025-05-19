import { useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";


export function EventNotifications() {
    useEffect(() => {
        const processEvents = async () => {
            const response = await fetch('http://localhost:8089/events')
            const res = await response.json()
            if (res.event === 'off'){
                toast(`${res.sensor} offline for device ${res.deviceId}`)
            } else if (res.event === 'on'){
                toast(`${res.sensor} online for device ${res.deviceId}`)
            }
        }
        processEvents()
    },[])

    return <ToastContainer/>
}