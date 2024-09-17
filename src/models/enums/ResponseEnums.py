from enum import Enum

class ResponseSignal(Enum):


    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported_yet"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_VALIDATED_SUCCESS = "file_validated_success"
    FILE_VALIDATED_ERROR = "file_validated_error"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_ERROR = "file_upload_error"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESS = "processing_success"
