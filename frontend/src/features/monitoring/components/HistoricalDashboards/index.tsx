export default function HistoricalDashboards({deviceId, patientId, experimentId}: {deviceId: string, patientId: string, experimentId: string}) {
  const panelData = [
    {
      label: "ECG",
      panels: [
        {
          src: `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=3&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
    {
      label: "BVP",
      panels: [
        {
          src: `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=2&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
    {
      label: "GSR",
      panels: [
        {
          src: `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=4&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
    {
      label: "Correlation Analysis (BVP, ECG, GSR)",
      panels: [
        {
          src: `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&panelId=6&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
 {
      label: "GSR Features",
      panels: [
        {
          src: `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=1&var-deviceId=${deviceId}&var-experimentId=1&panelId=7&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
 {
      label: "ECG Features",
      panels: [
        {
          src: `http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&var-subjectId=1&var-deviceId=${deviceId}&var-experimentId=1&panelId=8&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },

    
  ];

  return (
    <div className="p-4 space-y-6">
      {panelData.map(({ label, panels }) => (
        <div key={label}>
          <div className="flex flex-col gap-2">
            {panels.map(({ src, height }, idx) => (
              <iframe
                key={`${label}-panel-${idx}`}
                src={src}
                height={height}
                className="w-full border-none"
                loading="lazy"
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
