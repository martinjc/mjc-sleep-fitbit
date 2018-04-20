import json
import requests

from datetime import datetime
from urllib.parse import urlencode, quote

from _credentials import access_token, user_id

def get_auth_url():
# authorisation url

    base_url = "https://www.fitbit.com/"
    endpoint = "oauth2/authorize"
    params = {
        'response_type': 'token',
        'client_id': '228Z47',
        'redirect_uri': 'http://www.martinjc.com',
        'expires_in': 31536000,
        'scope': 'activity heartrate location nutrition profile settings sleep social weight',
    }

    auth_url = base_url + endpoint + "?" + urlencode(params, quote_via=quote)
    return auth_url

def collate_sleeps(sleeps, response):
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

    r = requests.get(base_url, params=params, headers=headers)
    sleeps, next = collate_sleeps(sleeps, r)
    print(len(sleeps))

    with open('sleeps.json', 'w') as output_file:
        json.dump(sleeps, output_file)

    while next:
        try:
            r = requests.get(next, headers=headers)
            sleeps, next = collate_sleeps(sleeps, r)
            print(len(sleeps))
        except Exception:
            print(r.headers)
            print(r.json())
            with open('sleeps.json', 'w') as output_file:
                json.dump(sleeps, output_file)

    with open('sleeps.json', 'w') as output_file:
        json.dump(sleeps, output_file)

if __name__ == '__main__':
    #print(get_auth_url())
    get_sleeps_list()
