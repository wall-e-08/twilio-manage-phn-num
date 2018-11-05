#!/usr/bin/python3

import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def find_all_numbers_sid_by_service(service_sid):
    try:
        all_numbers = client.messaging.services.get(service_sid).phone_numbers.list()
    except TwilioException as err:
        print("Messaging service SID not matched. error: {}".format(err))
        return
    print("FOUND MESSAGING SERVICE: {}".format(client.messaging.services.get(service_sid).fetch().friendly_name))
    return [pn.sid for pn in all_numbers]


def release_all_numbers_by_service():
    all_sids = find_all_numbers_sid_by_service(settings.MESSAGING_SERVICE_SID)
    if not all_sids:
        print("Please Try again")
        return
    for psid in all_sids:
        tw_number = client.incoming_phone_numbers(psid)
        phn = tw_number.fetch().phone_number
        print("Deleting number: {}".format(phn))
        try:
            tw_number.delete()
            print("Successfully deleted number: {}".format(phn))
        except TwilioException as err:
            print("CANNOT DELETE NUMBER: {}. Error: {}".format(phn, err))
    print("Task finished. Check previous log for details.")


def release_every_numbers():
    all_numbers = client.incoming_phone_numbers.list()

    if not all_numbers:
        print("Please Try again")
        return

    for phn in all_numbers:
        tw_number = client.incoming_phone_numbers(phn.sid)
        nmb = phn.phone_number
        print("Deleting number: {}".format(nmb))
        try:
            tw_number.delete()
            print("Successfully deleted number: {}".format(nmb))
        except TwilioException as err:
            print("CANNOT DELETE NUMBER: {}. Error: {}".format(nmb, err))


if __name__ == '__main__':
    release_every_numbers()
