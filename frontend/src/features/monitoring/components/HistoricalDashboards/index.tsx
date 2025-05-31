export default function HistoricalDashboards({deviceId, patientId, experimentId, fields, processingFields}: {deviceId: string, patientId: string, experimentId: string, fields: string[], processingFields: string[]}) {

  return (
    <div className="p-4 space-y-6">
      <div className="flex flex-col gap-4">
        {fields.map((field) => (
          <div key={field}>
            <div className="flex flex-col gap-2">
                <iframe
                  src={`http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&var-field=${field}&panelId=4&__feature.dashboardSceneSolo`}
                  height={400}
                  className="w-full border-none"
                  loading="lazy"
                />
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-col gap-4">
        {processingFields.map((field) => (
          <div key={field}>
            <div className="flex flex-col gap-2">
                <iframe
                  src={`http://localhost:3000/d-solo/dae0e31d-8150-44f7-a661-e02885189d0b/historical-data?orgId=1&timezone=browser&var-subjectId=${patientId}&var-deviceId=${deviceId}&var-experimentId=${experimentId}&var-field=bvp&var-processing_field=${field}&panelId=7&__feature.dashboardSceneSolo`}
                  height={400}
                  className="w-full border-none"
                  loading="lazy"
                />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
