import requests
from requests.auth import HTTPBasicAuth
import getpass
import email_alerts

def get_token():
    user_name = input("Username: ")
    password = getpass.getpass(prompt='Password: ')
    auth = {'username':user_name,'password':password}
    r = requests.post('https://api.robinhood.com/api-token-auth/',
        data=auth,verify=True, timeout=5)
    if 'mfa_required' in r.json().keys():
        auth['mfa_code'] = input("mfa_code: ")
        r = requests.post('https://api.robinhood.com/api-token-auth/',
            data=auth,verify=True, timeout=5)
        if 'non_field_errors' in r.json().keys():
            print('inccorect code')
            return
    if 'token' in r.json().keys():
        token = r.json()['token']
        print('always remember to logout')
        return token
    else:
        print('unable to log in')
        return

def logout(token):
    token = 'Token ' + token
    r = requests.post('https://api.robinhood.com/api-token-logout/',
        headers={'Authorization':token},verify=True, timeout=5)
    print('successfully logged out')

def accounts(token):
    token = 'Token ' + token
    r = requests.get('https://api.robinhood.com/accounts/',
        headers={'Authorization':token},verify=True, timeout=5)
    return r.json()['results'][0]

def recent_orders(token):
    token = 'Token ' + token
    r = requests.get('https://api.robinhood.com/orders/',
        headers={'Authorization':token},verify=True, timeout=5)
    return r.json()

def security_data(ticker):
    url = 'https://api.robinhood.com/instruments/?symbol={}'.format(ticker)
    r = requests.get(url,verify=True, timeout=5)

    return r.json()['results'][0]

def place_order(token, ticker, side, quantity, price=None):
    SAFETY_MARGIN = 1.02
    sufficient_funds = False
    security_data = security_data(ticker)
    url = security_data['url']
    tradeable = security_data['tradeable']
    if side == 'buy':
        est_cost = quantity * (price * SAFETY_MARGIN)
    account_data = accounts(token)
    if side == 'buy':
        #is buying power the correct number here?
        if float(account_data['buying_power']) > est_cost:
            sufficient_funds = True
    if tradeable and sufficient_funds:


    return
