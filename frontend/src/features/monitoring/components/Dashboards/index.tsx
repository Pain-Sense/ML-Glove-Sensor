export default function Dashboard({deviceId}: {deviceId: string}) {
  const panelData = [
    {
      label: "ECG",
      panels: [
        {
          src: `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&panelId=2&__feature.dashboardSceneSolo`,
        },
        {
          src: `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&panelId=1&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
    {
      label: "BVP",
      panels: [
        {
          src: `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&panelId=5&__feature.dashboardSceneSolo",
        },
        {
          src: "http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&panelId=4&__feature.dashboardSceneSolo`,
          height: 400,
        },
      ],
    },
    {
      label: "GSR",
      panels: [
        {
          src: `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&panelId=3&__feature.dashboardSceneSolo`,
        },
        {
          src: `http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&panelId=6&__feature.dashboardSceneSolo`,
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
