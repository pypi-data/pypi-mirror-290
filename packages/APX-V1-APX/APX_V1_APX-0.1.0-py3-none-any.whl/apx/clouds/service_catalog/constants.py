"""Constants used for service catalog."""
HOSTED_CATALOG_DIR_URL = 'https://raw.githubusercontent.com/apxdeploy-org/apxdeploy-catalog/master/catalogs'  # pylint: disable=line-too-long
CATALOG_SCHEMA_VERSION = 'v5'
CATALOG_DIR = '~/.apx/catalogs'
ALL_CLOUDS = ('aws', 'azure', 'gcp', 'ibm', 'lambda', 'scp', 'oci',
              'kubernetes', 'runpod', 'vsphere', 'cudo', 'fluidstack',
              'paperspace')
