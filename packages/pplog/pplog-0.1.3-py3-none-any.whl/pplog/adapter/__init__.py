"""Defines adapters/sinks where log checks are sent to."""
from azure.eventgrid import EventGridEvent

from pplog.log_checks.check_model import LogCheckResult
import logging
logger = logging.getLogger(__name__)

def log_check_to_splunk(
    stage: str,
    tenant_id: str,
    splunk_event_endpoint: str,
    log_check_result: LogCheckResult,
):
    """Converts a LogCheckResult into a well structured Splunk Log.

    We avoid using the usual LogHandler because it serializes the data as JSON.
    Instead, we want to add fields using a Structured Logging approach, where we
    know al fields beforehand.

    Trying to log dictionaries through the default handler hasn't worked in the past.
    """
    splunk_payload = {
        "payload_type": log_check_result.payload_type,
        "log_check_name": log_check_result.log_check_name,
        "metric_name": log_check_result.metric.name,
        "metric_value": log_check_result.metric.value,
        "target": log_check_result.target,
        "operator_name": log_check_result.operator.name,
        "operator": log_check_result.operator.function,
        "stage": stage,
        "check": "OK" if log_check_result.check else "Failed",
    }
    logger.info(splunk_payload)

    # event = EventGridEvent(
    #     data_version="1.0",
    #     subject="Log-Message",
    #     event_type="pplog-check",
    #     data=splunk_payload,
    # )
    # print(splunk_payload)
    # event_grid_client = cached_event_grid_client(
    #     tenant_id=tenant_id, event_grid_topic_endpoint=splunk_event_endpoint
    # )
    # event_grid_client.send(event)
