import logging
import re
import uuid
import simplejson as json
from django.conf import settings
from request_logging.middleware.RequestResponseLogging import ctx_request_id

MASKING_FIELDS = [field.upper()
                  for field in getattr(
        settings, 'REQUEST_RESPONSE_LOGGING_MASKING_FIELDS', list())]


class RequestIdFilter(logging.Filter):
    """
        Adds request id field in log record with uuid for each request
    """

    def filter(self, record):
        record.request_id = ctx_request_id.get(uuid.uuid4().hex)
        return True


class MaskingFilter(logging.Filter):
    """
    Masks data in log based on list of fields provided in
    settings.REQUEST_ID_MASKING_FIELDS
    """

    def filter(self, record):
        try:
            if MASKING_FIELDS:
                msg = json.loads(record.msg)
                if isinstance(msg.get('request_response_contents'), dict):
                    for key, value in msg['request_response_contents'].items():
                        if key.upper() in MASKING_FIELDS:
                            msg['request_response_contents'][key] = re.sub(
                                r'.', 'X', value)
                record.msg = json.dumps(msg)
        except Exception as _:
            pass
        return True
