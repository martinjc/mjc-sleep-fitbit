from urllib.parse import urlencode, quote


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


if __name__ == '__main__':
    print(get_auth_url())
