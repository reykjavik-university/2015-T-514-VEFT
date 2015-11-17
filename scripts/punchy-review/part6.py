from base import BasePart
import time


class Test(BasePart):
    """POST /companies/search - 10%"""
    tests = [
        ('verify_search_found', 10),
    ]

    def __init__(self, base_url, admin_token):
        super(self.__class__, self).__init__(base_url, admin_token)
        self.url = self.base_url + '/companies'

    def verify_search_found(self):
        data = {
            'title': 'hlysig ' + self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json',
        }

        # Create entry
        self.make_request('post', self.url, data=data, headers=headers)

        # Give ES minor time to reindex
        time.sleep(2)

        search_resp = self.make_request('post', self.url + '/search',
                                        data={'search': 'hlysig'},
                                        headers=headers)

        return len(search_resp.json()) > 0
