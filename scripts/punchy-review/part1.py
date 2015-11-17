from base import BasePart
import random


class Test(BasePart):
    """POST /companies - 10%"""
    tests = [
        ('verify_401_when_missing_admin_token', 2),
        ('verify_401_invalid_admin_token', 2),
        ('verify_415_missing_content_type', 1),
        ('verify_415_incorrect_content_type', 1),
        ('verify_201_if_created', 1),
        ('verify_409_if_same_name_created', 2),
        ('verify_that_newly_created_company_id_in_response', 1)
    ]

    def __init__(self, base_url, admin_token):
        super(self.__class__, self).__init__(base_url, admin_token)
        self.url = self.base_url + '/companies'

    def verify_401_when_missing_admin_token(self):
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        resp = self.make_request('post', self.url + '', data)
        return resp.status_code == 401

    def verify_401_invalid_admin_token(self):
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        headers = {
            'admin_token': ''.join(sorted(list(self.admin_token), key=lambda k: random.random()))
        }
        resp = self.make_request('post', self.url, data=data, headers=headers)
        return resp.status_code == 401

    def verify_415_missing_content_type(self):
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        headers = {
            'admin_token': self.admin_token
        }
        resp = self.make_request('post', self.url, data=data, headers=headers)
        return resp.status_code == 415

    def verify_415_incorrect_content_type(self):
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'text/plain',
        }
        resp = self.make_request('post', self.url, data=data, headers=headers)
        return resp.status_code == 415

    def verify_201_if_created(self):
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json',
        }
        resp = self.make_request('post', self.url, data=data, headers=headers)
        return resp.status_code == 201

    def verify_409_if_same_name_created(self):
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json',
        }
        self.make_request('post', self.url, data=data, headers=headers)
        resp = self.make_request('post', self.url, data=data, headers=headers)
        return resp.status_code == 409

    def verify_that_newly_created_company_id_in_response(self):
        data = {
            'title': self.random_string(10),
            'description': 'some description',
            'url': 'some url',
        }
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json',
        }
        resp = self.make_request('post', self.url, data=data, headers=headers)
        try:
            response_body = resp.json()
            response_keys = map(lambda x: x.lower(), response_body.keys())
            return 'id' in response_keys or '__id' in response_keys, resp
        except:
            return False
