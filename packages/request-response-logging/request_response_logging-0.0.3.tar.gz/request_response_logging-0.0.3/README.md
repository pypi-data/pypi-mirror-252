# request-response-logging

This logs request and response and also helps in generating request_id for each execution

## Installation

You can install it using pip:

```bash
pip install request-response-logging
```

## Usage
**In Djangos settings file use following attributes for controlling logger**






```python
# request header containing request id defaults X-REQUEST-ID if not provided
REQUEST_RESPONSE_ID_HEADER_KEY='X-REQUEST-ID'
# list of endpoints to ignore logging
REQUEST_RESPONSE_LOGGING_IGNORE_LIST= ['/get/user-details/', '/get/aadhar']
# list of request/response field to mask in logging in case of JSONResponse at base level
REQUEST_RESPONSE_LOGGING_MASKING_FIELDS=['pan', 'mobile']
# list of response fields to be popped in case of JSONResponse at base level
REQUEST_RESPONSE_LOGGING_POP_RESPONSE_KEYS=['error','traceback']
```
