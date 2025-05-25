package org.acme.service;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.InfluxDBClientFactory;
import com.influxdb.client.QueryApi;
import com.influxdb.client.domain.Query;
import com.influxdb.query.FluxTable;
import com.influxdb.query.FluxRecord;
import jakarta.annotation.PostConstruct;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import java.util.*;

@ApplicationScoped
public class InfluxService {

    @ConfigProperty(name = "influx.url")
    String influxUrl;

    @ConfigProperty(name = "influx.token")
    String influxToken;

    @ConfigProperty(name = "influx.org")
    String influxOrg;

    @ConfigProperty(name = "influx.bucket")
    String influxBucket;

    private String measurement = "processed_sensor_data";

    private InfluxDBClient client;

    @PostConstruct
    void init() {
        client = InfluxDBClientFactory.create(influxUrl, influxToken.toCharArray(), influxOrg, influxBucket);
    }

    public List<Map<String, Object>> queryMetricsInRange(Long experimentId, String start, String stop) {
      String flux = String.format("""
          from(bucket: "%s")
            |> range(start: %s, stop: %s)
            |> filter(fn: (r) => r._measurement == "%s" and r.experimentId == "%d")
      """, influxBucket, start, stop, measurement, experimentId);

        QueryApi queryApi = client.getQueryApi();
        List<FluxTable> tables = queryApi.query(flux);
        List<Map<String, Object>> results = new ArrayList<>();

        for (FluxTable table : tables) {
            for (FluxRecord record : table.getRecords()) {
                Map<String, Object> entry = new HashMap<>();
                entry.put("field", record.getField());
                entry.put("value", record.getValue());
                entry.put("time", record.getTime());
                entry.put("deviceId", record.getValueByKey("deviceId"));
                entry.put("experimentId", record.getValueByKey("experimentId"));
                results.add(entry);
            }
        }

        return results;
    }

    public List<Map<String, Object>> queryHistory(Long experimentId, String start) {
      String flux = String.format("""
          from(bucket: "%s")
            |> range(start: %s)
            |> filter(fn: (r) => r._measurement == "%s" and r.experimentId == "%d")
      """, influxBucket, start, measurement, experimentId);

        QueryApi queryApi = client.getQueryApi();
        List<FluxTable> tables = queryApi.query(flux);
        List<Map<String, Object>> results = new ArrayList<>();

        for (FluxTable table : tables) {
            for (FluxRecord record : table.getRecords()) {
                Map<String, Object> entry = new HashMap<>();
                entry.put("field", record.getField());
                entry.put("value", record.getValue());
                entry.put("time", record.getTime());
                entry.put("deviceId", record.getValueByKey("deviceId"));
                entry.put("experimentId", record.getValueByKey("experimentId"));
                results.add(entry);
            }
        }

        return results;
    }

    public List<Map<String, Object>> queryAggregatedMetrics(
      Long experimentId,
      String field,
      String start,
      String stop,
      String window,
      String aggregateFn
    ) {
    String flux = String.format("""
        from(bucket: "%s")
          |> range(start: %s, stop: %s)
          |> filter(fn: (r) => r._measurement == "%s" and r._field == "%s" and r.experimentId == "%d")
          |> aggregateWindow(every: %s, fn: %s, createEmpty: false)
          |> yield(name: "agg")
        """, influxBucket, start, stop, measurement, field, experimentId, window, aggregateFn);

    QueryApi queryApi = client.getQueryApi();
    List<FluxTable> tables = queryApi.query(flux);
    List<Map<String, Object>> results = new ArrayList<>();

    for (FluxTable table : tables) {
        for (FluxRecord record : table.getRecords()) {
            Map<String, Object> entry = new HashMap<>();
            entry.put("time", record.getTime());
            entry.put("value", record.getValue());
            entry.put("field", record.getField());
            entry.put("experimentId", record.getValueByKey("experimentId"));
            results.add(entry);
        }
    }

    return results;
  }
}
