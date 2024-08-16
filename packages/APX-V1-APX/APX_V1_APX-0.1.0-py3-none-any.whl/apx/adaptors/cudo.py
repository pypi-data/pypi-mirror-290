"""Cudo Compute cloud adaptor."""

from apx.adaptors import common

cudo = common.LazyImport(
    'cudo_compute',
    import_error_message='Failed to import dependencies for Cudo Compute. '
    'Try running: pip install "apxdeploy[cudo]"')
