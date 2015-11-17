from base import BasePart
import random
import time
import inspect


class Test(BasePart):
    """GET /companies[?page=N&max=N] - 20%"""
    tests = [
        ('verify_page_and_max_parameters', 10),
        ('verify_company_fields', 10),
    ]

    def __init__(self, base_url, admin_token):
        super(self.__class__, self).__init__(base_url, admin_token)
        self.url = self.base_url + '/companies'

        try:
            # Create five test_companies
            headers = {
                'admin_token': self.admin_token,
                'content-type': 'application/json'
            }

            for n in range(5):
                self.make_request('post', self.url, data={
                    'title': self.random_string(10),
                    'description': 'url',
                    'url': 'http://www.foo.is',
                }, headers=headers)
        except Exception as ex:
            print 'Unable to create test companies', ex.message

        time.sleep(2)

    def verify_page_and_max_parameters(self):
        headers = {
            'admin_token': self.admin_token,
            'content_type': 'application/json'
        }

        try:
            for page, _max, est in [(0, 1, 1), (1, 2, 2), (100, 100, 0)]:
                resp = self.make_request('get', self.url + '?page={}&max={}'.format(page, _max), headers=headers)
                data = resp.json()
                assert len(data) == est

        except:
            return False

        return True

    def verify_company_fields(self):
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json'
        }
        resp = self.make_request('get', self.url + '?page=0&max=1', headers=headers)

        try:
            company = resp.json()[0]
            k = ['url', 'title', 'description', 'id']
            return set(company.keys()) == set(k)
        except:
            return False
