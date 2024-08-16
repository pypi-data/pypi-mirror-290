"""Vsphere configuration bootstrapping."""

from apx import apx_logging
from apx.provision import common

logger = apx_logging.init_logger(__name__)


def bootstrap_instances(
        region: str, cluster_name: str,
        config: common.ProvisionConfig) -> common.ProvisionConfig:
    """See apx/provision/__init__.py"""
    logger.info(f'New provision of Vsphere: bootstrap_instances().Region: '
                f'{region} Cluster Name:{cluster_name}')

    # TODO: process config.

    return config
