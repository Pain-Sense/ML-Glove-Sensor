const Dashboards = ({experimentId, deviceId, patientId}: {
  experimentId: string
  patientId: number
  deviceId: number
}) => {
  const ecg = `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&from=1747693375313&to=1747694275313&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=3&__feature.dashboardSceneSolo`

  const bvp = `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&from=1747693375313&to=1747694275313&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=2&__feature.dashboardSceneSolo`

  const gsr = `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&from=1747693375313&to=1747694275313&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=4&__feature.dashboardSceneSolo`

  return (
    <div className="flex flex-col gap-4">
      <iframe src={ecg} width='900' height='450' frameBorder='0'></iframe>
      <iframe src={bvp} width='900' height='450' frameBorder='0'></iframe>
      <iframe src={gsr} width='900' height='450' frameBorder='0'></iframe>
    </div>
  )
}

export default Dashboards