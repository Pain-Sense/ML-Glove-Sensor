import { useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";


export function EventNotifications() {
    useEffect(() => {
        const processEvents = async () => {
            const response = await fetch('http://localhost:8089/events')
            const res = await response.text()
            if (res !== 'no event'){
                toast(res)
            }
        }
        processEvents()
    },[])

    return <ToastContainer/>
}