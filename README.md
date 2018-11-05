# Twilio Number manager

#### settings:
- `TWILIO_ACCOUNT_SID` -> Twilio account sid
- `TWILIO_AUTH_TOKEN` -> Twilio auth token
- `MESSAGING_SERVICE_SID` -> messaging service sid (used to release number)
- `TWILIO_BUY_NUMBER_BAN_STATES` -> when buying number, don't buy number from those states. input type: `list`

#### Scripts:
- `twilio_buy_number.py` => buy bulk amount of numbers and add this to a messaging service from twilio
- `twilio_release_number.py` => release bulk amount of numbers from messaging service

** more scripts coming soon..
