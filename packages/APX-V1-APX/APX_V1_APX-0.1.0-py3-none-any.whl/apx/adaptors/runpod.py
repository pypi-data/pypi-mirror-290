"""RunPod cloud adaptor."""

from apx.adaptors import common

runpod = common.LazyImport(
    'runpod',
    import_error_message='Failed to import dependencies for RunPod. '
    'Try running: pip install "apxdeploy[runpod]"')
