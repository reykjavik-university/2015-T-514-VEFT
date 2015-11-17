import json
import sys
import random
import requests
import string


class BasePart(object):
    def __init__(self, base_url, admin_token):
        self.base_url = base_url
        self.admin_token = admin_token

    @staticmethod
    def random_string(length):
        return ''.join(random.choice(string.lowercase) for x in range(length))

    @staticmethod
    def make_request(method, url, data=None, headers=None):
        if not data:
            data = {}
        if not headers:
            headers = {}
        try:
            m = getattr(requests, method)
            return m(url, data=json.dumps(data), headers=headers)
        except Exception as ex:
            print(ex)
            sys.exit(2)

    def execute(self):
        res = 0

        for t, v in self.tests:
            func = getattr(self, t)

            if func():
                res += v
            else:
                print t, 'failed'
        return res
