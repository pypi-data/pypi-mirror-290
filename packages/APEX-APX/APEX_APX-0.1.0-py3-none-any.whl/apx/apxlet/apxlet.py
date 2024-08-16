"""apxlet: a daemon running on the head node of a cluster."""

import time

import apx
from apx import apx_logging
from apx.apxlet import constants
from apx.apxlet import events

# Use the explicit logger name so that the logger is under the
# `apx.apxlet.apxlet` namespace when executed directly, so as
# to inherit the setup from the `apx` logger.
logger = apx_logging.init_logger('apx.apxlet.apxlet')
logger.info(f'Apxlet started with version {constants.APXLET_VERSION}; '
            f'APX v{apx.__version__} (commit: {apx.__commit__})')

EVENTS = [
    events.AutostopEvent(),
    events.JobSchedulerEvent(),
    # The managed job update event should be after the job update event.
    # Otherwise, the abnormal managed job status update will be delayed
    # until the next job update event.
    events.ManagedJobUpdateEvent(),
    # This is for monitoring controller job status. If it becomes
    # unhealthy, this event will correctly update the controller
    # status to CONTROLLER_FAILED.
    events.ServiceUpdateEvent(),
]

while True:
    time.sleep(events.EVENT_CHECKING_INTERVAL_SECONDS)
    for event in EVENTS:
        event.run()
