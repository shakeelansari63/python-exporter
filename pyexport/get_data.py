import requests
import base64

def get_data():
    api_key = 'CXSvg9Rjz8CVvy7oi5963768qQwWHJ3l'

    auth = requests.auth.HTTPBasicAuth(api_key, '')

    url = 'https://api.sandbox.invoiced.com/invoices/10030138'

    req = requests.get(url, auth=auth)
    data = req.json()

    return data

if __name__ == '__main__':
    get_data()