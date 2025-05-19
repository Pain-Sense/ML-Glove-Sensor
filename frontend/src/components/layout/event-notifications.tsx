import { useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";


export function EventNotifications() {
    useEffect(() => {
        const processEvents = async () => {
            const response = await fetch('http://localhost:8089/events')
            const res = await response.json();

            if ('timestamp' in res){
                // console.log(res);
                var online = ""
                if (res.sensorOn) {
                    online = "online"
                } else {
                    online = "offline"
                }

                var msg = "" + res.sensorType + " sensor " + online + " for device " + res.deviceId;
                toast(msg);
            }
        }
        const intervalId = setInterval(processEvents, 3000)
        return () => clearInterval(intervalId)
    },[])

    return <ToastContainer/>
}