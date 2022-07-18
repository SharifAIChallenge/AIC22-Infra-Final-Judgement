import enum


class EventStatus(enum.Enum):
    # compile status codes
    COMPILE_SUCCESS = 100
    COMPILE_FAILED  = 102

    # file transfer status codes
    UPLOAD_FAILED   = 402
    FILE_NOT_FOUND  = 404

    # match status codes
    MATCH_STARTED       = 500
    MATCH_FAILED        = 502
    MATCH_SUCCESS       = 504
    MATCH_TIMEOUT       = 506
    MATCH_NOT_PROVIDED  = 508
    


class Event:
    def __init__(self, title, token, status_code, message_body=""):
        self.title = title
        self.status_code = status_code
        self.message_body = message_body
        self.token = token
