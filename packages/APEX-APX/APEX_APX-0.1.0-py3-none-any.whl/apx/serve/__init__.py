"""Modules for APXServe services."""
import os

from apx.serve.constants import ENDPOINT_PROBE_INTERVAL_SECONDS
from apx.serve.constants import INITIAL_VERSION
from apx.serve.constants import LB_CONTROLLER_SYNC_INTERVAL_SECONDS
from apx.serve.constants import APXSERVE_METADATA_DIR
from apx.serve.core import down
from apx.serve.core import status
from apx.serve.core import tail_logs
from apx.serve.core import up
from apx.serve.core import update
from apx.serve.serve_state import ReplicaStatus
from apx.serve.serve_state import ServiceStatus
from apx.serve.serve_utils import DEFAULT_UPDATE_MODE
from apx.serve.serve_utils import format_service_table
from apx.serve.serve_utils import generate_replica_cluster_name
from apx.serve.serve_utils import generate_service_name
from apx.serve.serve_utils import get_endpoint
from apx.serve.serve_utils import ServeCodeGen
from apx.serve.serve_utils import ServiceComponent
from apx.serve.serve_utils import APX_SERVE_CONTROLLER_NAME
from apx.serve.serve_utils import UpdateMode
from apx.serve.service_spec import ApxServiceSpec

os.makedirs(os.path.expanduser(APXSERVE_METADATA_DIR), exist_ok=True)

__all__ = [
    'down',
    'ENDPOINT_PROBE_INTERVAL_SECONDS',
    'format_service_table',
    'generate_replica_cluster_name',
    'generate_service_name',
    'get_endpoint',
    'INITIAL_VERSION',
    'LB_CONTROLLER_SYNC_INTERVAL_SECONDS',
    'ReplicaStatus',
    'ServiceComponent',
    'ServiceStatus',
    'ServeCodeGen',
    'ApxServiceSpec',
    'APX_SERVE_CONTROLLER_NAME',
    'APXSERVE_METADATA_DIR',
    'status',
    'tail_logs',
    'up',
    'update',
    'UpdateMode',
    'DEFAULT_UPDATE_MODE',
]
