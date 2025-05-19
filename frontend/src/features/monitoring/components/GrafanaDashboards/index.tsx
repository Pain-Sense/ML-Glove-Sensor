import React from "react";

interface DashboardProps {
    deviceId: number
}

export const GrafanaDashboards: React.FC<DashboardProps> = ({
    deviceId,
}) => {
    const ecg = `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&from=1747666147577&to=1747666447577&timezone=browser&var-deviceId=${deviceId}&panelId=2&__feature.dashboardSceneSolo`
    const bvp = `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&from=1747666147577&to=1747666447577&timezone=browser&var-deviceId=${deviceId}&panelId=5&__feature.dashboardSceneSolo`
    const gsr = `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&from=1747666147577&to=1747666447577&timezone=browser&var-deviceId=${deviceId}&panelId=3&__feature.dashboardSceneSolo`
    return (
        <>
            <iframe src={ecg} width='450' height='200' frameBorder='0'></iframe>
            <iframe src={bvp} width='450' height='200' frameBorder='0'></iframe>
            <iframe src={gsr} width='450' height='200' frameBorder='0'></iframe>
        </>
    )
}