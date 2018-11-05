#!/usr/bin/python3

import settings, sys
from twilio.rest import Client


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def get_number(toll_free=True, region=None):
    """
    get available numbers to buy from twilio
    https://www.twilio.com/docs/api/rest/available-phone-numbers
    :param bool toll_free: is toll free or local.
    :param str region: Phone number search in specific region (won't work if toll_free)
    :return: available phone numbers to buy (limit 30 if not specified)
    """
    country_iso = 'US'
    sms_enabled = True
    print("SMS service: {}".format("Enabled" if sms_enabled else "Not enabled"))
    if toll_free:
        numbers = client.available_phone_numbers(country_iso). \
            toll_free. \
            list(sms_enabled=sms_enabled)
    else:
        numbers = client.available_phone_numbers(country_iso). \
            local. \
            list(in_region=region, sms_enabled=sms_enabled)
    return numbers


def buy_number():
    """
    buy number from twilio
    https://www.twilio.com/docs/api/rest/incoming-phone-numbers
    :param int try_limit: How many numbers you want to buy?
    :param sms_url: URL Twilio will request when receiving an incoming SMS message to this number
    :param sms_method: when making requests to the SmsUrl. Either GET or POST
    :param str friendly_name: Friendly Name
    :param bool toll_free: is toll free or local.
    :param str state_code: region/state. eg: 'CA'
    :return: the number object which has been bought or None

    # not using now
    # :param str voice_url: The URL Twilio will request when this phone number receives a call
    # :param str voice_method: The HTTP method Twilio will use when requesting voice_url. Either GET or POST
    """
    all_args = sys.argv[1:]
    if not all_args or len(all_args) < 2:
        # '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
        print("Please enter " + "\x1b[6;30;42m" + "Phone Number limit" + "\x1b[0m" + " as 1st argument and  " + "\x1b[6;30;42m" + "friendly name" + "\x1b[0m" + " as 2nd argument..!")
        print("For Example: " + "\x1b[6;30;32m" + "$ python3 twilio_buy_number.py 20 phone_number_by_debashis" + "\x1b[0m")
        print("Hint: Use quote if you want space inside friendly name")
        return
    try_limit = int(all_args[0])
    friendly_name = all_args[1]

    toll_free = True
    sms_url = "https://demo.twilio.com/welcome/sms/"

    numbers = get_number(toll_free)
    if not numbers or try_limit < 1:
        print("Unfortunately no numbers found right now...\nOr might be you tried to buy 0 phone numbers?? wtf!?")
        return None
    print("Total phone numbers found: {}".format(len(numbers)))
    for number in numbers:
        number_region = number.region.split(" ")[0].strip(",").strip().lower() if not toll_free else None  # state name lowercase
        if number_region not in settings.TWILIO_BUY_NUMBER_BAN_STATES:  # don't take number from banned region
            print("Need '{}' more phone numbers to be bought".format(try_limit))
            # buying phone number
            print("Trying to buy phone number: \x1b[0;32;31m{}\x1b[0m".format(number.phone_number))
            new_number = client.incoming_phone_numbers.create(
                friendly_name=friendly_name,
                phone_number=number.phone_number,
                sms_url=sms_url,
                sms_method="POST",
                # voice_url=voice_url,
                # voice_method=voice_method,
            )
            if new_number:  # if res[0] == 201:
                print("Successfully bought number: \x1b[6;30;32m{0}\x1b[0m".format(str(new_number.phone_number)))
                phone_number_sid = new_number.sid
                msg_service_list = client.messaging.services.list()
                if len(msg_service_list) != 0:
                    msg_sid = msg_service_list[0].sid
                    frndly_name = msg_service_list[0].friendly_name
                    print("Picking 'first' messaging service. Friendly Name: {}".format(frndly_name))
                    client.messaging.services(msg_sid).phone_numbers.create(phone_number_sid=phone_number_sid)
                    print("Successfully added \x1b[6;30;42m{}\x1b[0m to message service: \x1b[6;30;42m{}\x1b[0m".format(new_number.phone_number, frndly_name))

            try_limit -= 1
            if try_limit == 0:
                print("All phone numbers bought.. Existing..")
                return None
    return None


if __name__ == '__main__':
    buy_number()