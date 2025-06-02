export default function Dashboard({deviceId, fields}: {deviceId: string, fields: string[]}) {
  return (
    <div className="p-4 space-y-6">
      {fields.map((field) => (
        <div key={field}>
          <div className="flex flex-col gap-2">
            <iframe
              src={`http://localhost:3000/d-solo/d4ebeaef-38b9-48e3-9d38-7d80cfeb9260/iot?orgId=1&timezone=browser&var-deviceId=${deviceId}&var-field=${field}&panelId=1&__feature.dashboardSceneSolo`}
              height={400}
              className="w-full border-none"
              loading="lazy"
            />
          </div>
        </div>
      ))}
    </div>
  );
}
