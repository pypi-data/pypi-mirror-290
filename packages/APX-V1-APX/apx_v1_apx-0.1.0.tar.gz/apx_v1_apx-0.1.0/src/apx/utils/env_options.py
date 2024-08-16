"""Global environment options for apx."""
import enum
import os


class Options(enum.Enum):
    """Environment variables for APX."""
    IS_DEVELOPER = 'APXDEPLOY_DEV'
    SHOW_DEBUG_INFO = 'APXDEPLOY_DEBUG'
    DISABLE_LOGGING = 'APXDEPLOY_DISABLE_USAGE_COLLECTION'
    MINIMIZE_LOGGING = 'APXDEPLOY_MINIMIZE_LOGGING'
    # Internal: this is used to skip the cloud user identity check, which is
    # used to protect cluster operations in a multi-identity scenario.
    # Currently, this is only used in the job and serve controller, as there
    # will not be multiple identities, and skipping the check can increase
    # robustness.
    SKIP_CLOUD_IDENTITY_CHECK = 'APXDEPLOY_SKIP_CLOUD_IDENTITY_CHECK'

    def get(self):
        """Check if an environment variable is set to True."""
        return os.getenv(self.value, 'False').lower() in ('true', '1')
