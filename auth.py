import requests
from requests.auth import HTTPBasicAuth
import getpass
from email_alerts import send_mail

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
    if 'results' in r.json().keys():
        return r.json()['results'][0]
    else:
        return {}

def recent_orders(token):
    token = 'Token ' + token
    r = requests.get('https://api.robinhood.com/orders/',
        headers={'Authorization':token},verify=True, timeout=5)
    return r.json()

def security_data(ticker):
    url = 'https://api.robinhood.com/instruments/?symbol={}'.format(ticker)
    r = requests.get(url,verify=True, timeout=5)

    return r.json()['results'][0]

def get_quote(ticker):

    r = requests.get('https://api.robinhood.com/quotes/{}/'.format(ticker))
    return r.json()
    try:
        return float(r.json()['ask_price'])
    except:
        return None

def notify(order_dat):
    return


def place_order(token, ticker=None, side=None, quantity=None, price=None):

    est_cost = None
    est_proceeds = None
    formatted_token = 'Token ' + token
    email_address = input('Email address: ')
    SAFETY_MARGIN = 1.02
    sufficient_funds = False
    sec_data = security_data(ticker)
    quote = get_quote(ticker)
    sec_url = sec_data['url']
    tradeable = sec_data['tradeable']
    account_data = accounts(token)
    if side == 'buy':
        last_trade = float(quote['last_trade_price'])
        est_cost = quantity * (last_trade * SAFETY_MARGIN)
        #is buying power the correct number here?
        if float(account_data['buying_power']) > est_cost:
            sufficient_funds = True
    if tradeable and sufficient_funds:
        print('Estimated cost/proceeds from this transaction: {}'.format(est_cost))
        account = 'https://api.robinhood.com/accounts/{}/'.format(input('Account number: '))
        pattern_url = 'https://api.robinhood.com/orders/'
        #had to specify price
        data = {
        'account' : account,
        'instrument' : sec_url,
        'quantity' : str(quantity),
        'side' : side,
        'symbol' : ticker,
        'time_in_force' : 'gfd',
        'trigger': 'immediate',
        'type' : 'market',
        'price' : last_trade + 0.05
        }
        r = requests.post(pattern_url,data=data,headers={'Authorization':formatted_token},verify=True, timeout=5)
        
        order_dat = r.json()

        subject = 'succesful {} trade on robinhood'.format(side)

        notify(order_dat)

    return order_dat
