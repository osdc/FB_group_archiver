import requests
import json
import urllib2

class Kippt:
    def __init__(self, username, api_token):
        self.username = username
        self.api_token = api_token
        self.api_endpoints = {
            'account': 'https://kippt.com/api/account/',
            'lists': 'https://kippt.com/api/lists/',
            'list': 'https://kippt.com/api/lists/%s/',
            'clips': 'https://kippt.com/api/clips/',
            'clip': 'https://kippt.com/api/clips/%s/',
            'search': 'https://kippt.com/api/search/clips/',
        }
        self.headers = {
            'X-Kippt-API-Token': self.api_token,
            'X-Kippt-Username': self.username,
        }

    def get_lists(self):
        r = requests.get(self.api_endpoints['lists'], headers=self.headers)
        return json.loads(r.content)

    def get_list(self, list_id):
        r = requests.get(self.api_endpoints['list'] % list_id, headers=self.headers)
        return json.loads(r.content)

    def get_clips(self):
        r = requests.get(self.api_endpoints['clips'], headers=self.headers)
        return json.loads(r.content)

    def get_clip(self, clip_id):
        r = requests.get(self.api_endpoints['clip'] % clip_id, headers=self.headers)
        return json.loads(r.content)

    def search(self, keyword):
        r = requests.get(self.api_endpoints['search'], headers=self.headers)
        return json.loads(r.content)

    def create(self, title, **args):
        """ Create a new Kippt List.

        Parameters:
        - title (Required)
        - args Dictionary of other fields"""

        data = json.dumps(dict({'title': title}, **args))
        r = requests.post(
            "https://kippt.com/api/lists",
            headers=self.headers,
            data=data
        )
        return (r.json())


    
