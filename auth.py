import requests
from requests.auth import HTTPBasicAuth
import getpass

def get_token():
    user_name = input("Username: ")
    password = getpass.getpass(prompt='Password: ')
    auth = {'username':user_name,'password':password}
    r = requests.post('https://api.robinhood.com/api-token-auth/',
        data=auth,verify=True, timeout=5)
    if r.json()['mfa_required']:
        auth['mfa_code'] = input("mfa_code: ")
        r = requests.post('https://api.robinhood.com/api-token-auth/',
            data=auth,verify=True, timeout=5)
        if 'non_field_errors' in r.json().keys():
            print('inccorect code')
            return
    if 'token' in r.json().keys():
        token = r.json()['token']
        return token
    else:
        print('nothing happened')
        return

def logout(token):
    r = requests.post('https://api.robinhood.com/api-token-logout/',
        data={'Token':token},verify=True, timeout=5)

    return r.json()

def get_accounts(token):
    r = requests.get('https://api.robinhood.com/api-token-auth/',
        auth=(token),verify=True, timeout=5)
    return r.json()
