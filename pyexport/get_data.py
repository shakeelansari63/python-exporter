import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, req):
        req.headers["authorization"] = "Bearer " + self.token
        return req

def get_data(url, auth = None):
    req = requests.get(url, auth=auth)
    data = req.json()

    return data

def create_basic_auth(username, password):
    return requests.auth.HTTPBasicAuth(username, password)

def create_bearer_auth(token):
    return BearerAuth(token)
