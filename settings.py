TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""

TWILIO_BUY_NUMBER_BAN_STATES = ['AK', 'HI']

try:
    from local_settings import *
except ImportError:
    pass
