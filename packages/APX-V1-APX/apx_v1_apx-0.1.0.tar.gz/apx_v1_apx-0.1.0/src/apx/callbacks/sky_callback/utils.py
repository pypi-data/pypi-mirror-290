import os
from typing import Optional

DISABLE_CALLBACK = os.environ.get('APXDEPLOY_DISABLE_CALLBACK',
                                  'False').lower() in ('true', '1')


# TODO(woosuk): Find a better way of lazy loading.
class CallbackLoader:

    @staticmethod
    def keras(log_dir: Optional[str] = None, total_steps: Optional[int] = None):
        from apx_callback.integrations.keras import ApxKerasCallback
        return ApxKerasCallback(log_dir=log_dir, total_steps=total_steps)

    @staticmethod
    def pytorch_lightning(log_dir: Optional[str] = None,
                          total_steps: Optional[int] = None):
        from apx_callback.integrations.pytorch_lightning import (
            ApxLightningCallback)
        return ApxLightningCallback(log_dir=log_dir, total_steps=total_steps)

    @staticmethod
    def transformers(log_dir: Optional[str] = None,
                     total_steps: Optional[int] = None):
        from apx_callback.integrations.transformers import (
            ApxTransformersCallback)
        return ApxTransformersCallback(log_dir=log_dir, total_steps=total_steps)
