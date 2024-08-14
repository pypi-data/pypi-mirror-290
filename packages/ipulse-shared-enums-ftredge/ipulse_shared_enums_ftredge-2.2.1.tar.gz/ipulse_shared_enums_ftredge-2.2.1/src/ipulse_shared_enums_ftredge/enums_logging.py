# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import Enum


class LoggingHandler(Enum):

    """
    Standardized remote logging handlers for data engineering pipelines,
    designed for easy analysis and identification of remote logging
    requirements
    """
    
    NONE = "none"  # No remote handler
    LOCAL_STREAM = "local_stream"  # Local stream handler
    GCP_CLOUD_LOGGING = "gcp_cloud_logging"
    GCP_ERROR_REPORTING = "gcp_error_reporting"
    GCP_FIREBASE = "gcp_firebase"
    AWS_CLOUD_WATCH = "aws_cloud_watch"
    AZURE_MONITOR = "azure_monitor"
    AZURE_APPLICATION_INSIGHTS = "azure_application_insights"
    IBM_LOG_ANALYTICS = "ibm_log_analytics"
    ALIBABA_LOG_SERVICE = "alibaba_log_service"
    LOGGLY = "loggly"
    DATADOG = "datadog"
    NEW_RELIC = "new_relic"
    SENTRY = "sentry"
    SUMOLOGIC = "sumologic"
    # --- Other ---
    SYSLOG = "syslog" # For system logs
    CUSTOM = "custom" # For a user-defined remote handler
    OTHER = "other"

    def __str__(self):
        return self.value


class LogLevel(Enum):
    """
    Standardized notice levels for data engineering pipelines,
    designed for easy analysis and identification of manual 
    intervention needs.
    """
    DEBUG = 10  # Detailed debug information (for development/troubleshooting)

    INFO = 100
    INFO_REMOTE_PERSISTNACE_COMPLETE= 101
    INFO_REMOTE_UPDATE_COMPLETE = 102
    INFO_REMOTE_DELETE_COMPLETE = 103

    INFO_REMOTE_BULK_PERSISTNACE_COMPLETE= 111
    INFO_REMOTE_BULK_UPDATE_COMPLETE = 112
    INFO_REMOTE_BULK_DELETE_COMPLETE = 113

    INFO_LOCAL_PERSISTNACE_COMPLETE = 121

    SUCCESS = 201
    SUCCESS_WITH_NOTICES = 211
    SUCCESS_WITH_WARNINGS = 212

    NOTICE = 300  # Maybe same file or data already fully or partially exists
    NOTICE_ALREADY_EXISTS = 301 # Data already exists, no action required
    NOTICE_PARTIAL_EXISTS = 302 # Partial data exists, no action required
    NOTICE_ACTION_CANCELLED = 303 # Data processing cancelled, no action required

     # Warnings indicate potential issues that might require attention:
    WARNING = 400 # General warning, no immediate action required
    # WARNING_NO_ACTION = 401 # Minor issue or Unexpected Behavior, no immediate action required (can be logged frequently)
    WARNING_REVIEW_RECOMMENDED = 402 # Action recommended to prevent potential future issues
    WARNING_FIX_RECOMMENDED = 403 # Action recommended to prevent potential future issues
    WARNING_FIX_REQUIRED = 404  # Action required, pipeline can likely continue

    ERROR = 500 # General error, no immediate action required

    ERROR_EXCEPTION = 501
    ERROR_CUSTOM = 502 # Temporary error, automatic retry likely to succeed

    ERROR_OPERATION_PARTIALLY_FAILED = 511 # Partial or full failure, manual intervention required
    ERROR_OPERATION_FAILED = 512 # Operation failed, manual intervention required
    ERORR_OPERATION_WITH_WARNINGS = 513 # Partial or full failure, manual intervention required
    ERORR_OPERATION_WITH_ERRORS = 514 # Partial or full failure, manual intervention required
    ERORR_OPERATION_WITH_WARNINGS_OR_ERRORS = 515 # Partial or full failure, manual intervention required

    ERROR_PERSISTANCE_FAILED = 522 # Data persistance failed, manual intervention required
    ERROR_UPDATE_FAILED = 523 # Data update failed, manual intervention required
    ERROR_DELETE_FAILED = 524 # Data deletion failed, manual intervention required
    ERROR_PERSISTANCE_WITH_ERRORS = 525 # Data persistance failed, manual intervention required
    ERROR_UPDATE_WITH_ERRORS = 526 # Data update failed, manual intervention required
    ERROR_DELETE_WITH_ERRORS = 527 # Data deletion failed, manual intervention required

    ERROR_THRESHOLD_REACHED = 551
    ERROR_PIPELINE_THRESHOLD_REACHED = 552 # Error due to threshold reached, no immediate action required
    ERROR_SUBTHRESHOLD_REACHED = 553 # Error due to threshold reached, no immediate action required
    ERROR_DATA_QUALITY_THRESHOLD_REACHED = 554 # Error due to threshold reached, no immediate action required
    ERROR_METADATA_QUALITY_THRESHOLD_REACHED = 555 # Error due to threshold reached, no immediate action required
    # Critical errors indicate severe failures requiring immediate attention:
    CRITICAL=600 # General critical error, requires immediate action
    CRITICAL_SYSTEM_FAILURE = 601 # System-level failure (e.g., infrastructure, stackoverflow ), requires immediate action

    UNKNOWN=1001 # Unknown error, should not be used in normal operation

    def __str__(self):
        return self.value