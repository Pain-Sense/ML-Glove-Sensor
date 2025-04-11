#!/bin/bash
# Replace env vars in provisioning files
envsubst < /etc/grafana/provisioning/datasources/datasources.yml.template > /etc/grafana/provisioning/datasources/datasources.yml

# Then start Grafana
/run.sh
