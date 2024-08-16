"""Managed jobs."""
import pathlib

from apx.jobs.constants import JOBS_CLUSTER_NAME_PREFIX_LENGTH
from apx.jobs.constants import JOBS_CONTROLLER_TEMPLATE
from apx.jobs.constants import JOBS_CONTROLLER_YAML_PREFIX
from apx.jobs.constants import JOBS_TASK_YAML_PREFIX
from apx.jobs.core import cancel
from apx.jobs.core import launch
from apx.jobs.core import queue
from apx.jobs.core import tail_logs
from apx.jobs.recovery_strategy import DEFAULT_RECOVERY_STRATEGY
from apx.jobs.recovery_strategy import RECOVERY_STRATEGIES
from apx.jobs.state import ManagedJobStatus
from apx.jobs.utils import dump_managed_job_queue
from apx.jobs.utils import format_job_table
from apx.jobs.utils import JOB_CONTROLLER_NAME
from apx.jobs.utils import load_managed_job_queue
from apx.jobs.utils import ManagedJobCodeGen

pathlib.Path(JOBS_TASK_YAML_PREFIX).expanduser().parent.mkdir(parents=True,
                                                              exist_ok=True)
__all__ = [
    'RECOVERY_STRATEGIES',
    'DEFAULT_RECOVERY_STRATEGY',
    'JOB_CONTROLLER_NAME',
    # Constants
    'JOBS_CONTROLLER_TEMPLATE',
    'JOBS_CONTROLLER_YAML_PREFIX',
    'JOBS_TASK_YAML_PREFIX',
    # Enums
    'ManagedJobStatus',
    # Core
    'cancel',
    'launch',
    'queue',
    'tail_logs',
    # utils
    'ManagedJobCodeGen',
    'format_job_table',
    'dump_managed_job_queue',
    'load_managed_job_queue',
]
