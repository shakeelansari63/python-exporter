import requests

def get_data(url, auth = None):
    req = requests.get(url, auth=auth)
    data = req.json()

    return data

def create_basic_auth(username, password):
    return requests.auth.HTTPBasicAuth(username, password)

if __name__ == '__main__':
    get_data()