import sys
import json
import requests

from datetime import datetime
from urllib.parse import urlencode, quote

from _credentials import access_token, user_id

def get_auth_url():
# create an authorisation url to copy paste into a browser window
# so we can get an access token to store in _credentials.py

    base_url = "https://www.fitbit.com/"
    endpoint = "oauth2/authorize"
    params = {
        'response_type': 'token',
        'client_id': '228Z47', # not privileged information, can be public
        'redirect_uri': 'http://www.martinjc.com',
        'expires_in': 31536000,
        'scope': 'activity heartrate location nutrition profile settings sleep social weight', # oh my god we don't need all this, but why not, eh?
    }

    auth_url = base_url + endpoint + "?" + urlencode(params, quote_via=quote)
    return auth_url


def collate_sleeps(sleeps, response):
    # extract sleep data from response and add to existing sleep records
    # check to see if there's a next page and get that too
    response_json = response.json()
    if response_json.get('sleep'):
        sleeps += response_json['sleep']
    next = response_json.get('pagination').get('next')
    return sleeps, next

def get_sleeps_list():

    sleeps = []

    today = datetime.today()

    today_string = today.date().isoformat()
    print(today_string)

    base_url = 'https://api.fitbit.com/1.2/user/-/sleep/list.json'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    params = {
        'beforeDate': today_string,
        'sort': 'desc',
        'offset': 0,
        'limit': 100
    }

    # get the first set of sleep records
    r = requests.get(base_url, params=params, headers=headers)
    sleeps, next = collate_sleeps(sleeps, r)
    print(len(sleeps))

    with open('sleeps.json', 'w') as output_file:
        json.dump(sleeps, output_file)

    # while there's more records to get, get them
    # note fitbit apparently can't tell when there are no more
    # this will crap out at some point and start returning
    # errors, so we'll only carry on while the status code is good
    while r.status_code == 200:
        try:
            print(next)
            r = requests.get(next, headers=headers)
            sleeps, next = collate_sleeps(sleeps, r)
            print(len(sleeps))
        except Exception:
            with open('sleeps.json', 'w') as output_file:
                json.dump(sleeps, output_file)
            sys.exit(0)

    with open('sleeps.json', 'w') as output_file:
        json.dump(sleeps, output_file)

if __name__ == '__main__':
    print(get_auth_url())
    get_sleeps_list()
