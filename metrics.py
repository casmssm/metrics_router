import os,sys
sys.dont_write_bytecode = True
os.environ["PROMETHEUS_DISABLE_CREATED_SERIES"] = 'True'
# Metrics
# Importing default requirements for exporter
import prometheus_client
from prometheus_client import start_http_server, Counter, Gauge, Info, multiprocess
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY

# Removing unused metrics for clean
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

# Defining the counter metric layouts
METRIC_INGESTION_SUCCESS_COUNT = Counter(
    'system_metric_ingestion_success', 'Counter for success in ingestion of metrics',
    ['worker']
)
##
METRIC_LAST_RECEIVED_MESSAGE = Gauge(
    'system_metric_last_received_message', 'Last received message in timestamp format',
    ['worker']
)