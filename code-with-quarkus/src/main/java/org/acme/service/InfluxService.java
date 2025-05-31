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

  public List<String> getFieldsForLiveExperiment(Long experimentId) {
    List<String> fieldKeys = new ArrayList<>();
    fieldKeys.addAll(getFieldKeysFromMeasurement("processed_sensor_data", experimentId));
    return fieldKeys.stream().distinct().toList(); 
  }

  public List<String> getFieldsForHistoricalData(Long experimentId) {
    List<String> fieldKeys = new ArrayList<>();
    fieldKeys.addAll(getFieldKeysFromMeasurement("processed_sensor_data", experimentId));
    fieldKeys.addAll(getFieldKeysFromMeasurement("enriched_hr_data", experimentId));
    return fieldKeys.stream().distinct().toList(); 
  }

  private List<String> getFieldKeysFromMeasurement(String measurement, Long experimentId) {
    String flux = String.format("""
        import "influxdata/influxdb/schema"
        
        schema.fieldKeys(
          bucket: "%s",
          predicate: (r) => 
            r._measurement == "%s" and 
            r.experimentId == "%d",
          start: -30d
        )
    """, influxBucket, measurement, experimentId);

    QueryApi queryApi = client.getQueryApi();
    List<FluxTable> tables = queryApi.query(flux);
    List<String> keys = new ArrayList<>();

    for (FluxTable table : tables) {
        for (FluxRecord record : table.getRecords()) {
            Object key = record.getValueByKey("_value");
            if (key != null) {
                keys.add(key.toString());
            }
        }
    }

    return keys;
  }
}
