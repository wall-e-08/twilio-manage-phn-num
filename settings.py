TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""

MESSAGING_SERVICE_SID = ""

TWILIO_BUY_NUMBER_BAN_STATES = ['AK', 'HI']

try:
    from local_settings import *
except ImportError:
    pass
