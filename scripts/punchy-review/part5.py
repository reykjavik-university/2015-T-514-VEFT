import time
from base import BasePart


class Test(BasePart):
    """POST /companies/:id - 20 %"""
    tests = [
        ('verify_company_not_found_404', 5),
        ('verify_company_is_deleted', 5),
        ('verify_company_is_deleted_in_es', 10)
    ]

    def __init__(self, base_url, admin_token):
        super(self.__class__, self).__init__(base_url, admin_token)
        self.url = self.base_url + '/companies'
        self.company = None

        try:
            # Create five test_companies
            headers = {
                'admin_token': self.admin_token,
                'content-type': 'application/json'
            }

            self.company = self.make_request('post', self.url, data={
                'title': self.random_string(10),
                'description': 'url',
                'url': 'http://www.foo.is',
            }, headers=headers).json()
        except Exception as ex:
            print 'Unable to create test companies', ex.message

        if not self.company.get('id'):
            raise Exception('Unable to fetch company id for created company')

    def verify_company_not_found_404(self):
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json'
        }
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }
        resp = self.make_request('delete', self.url + '/dummy-id', headers=headers, data=data)
        return resp.status_code == 404

    def verify_company_is_deleted(self):
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json'
        }
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }

        resp = self.make_request('post', self.url, headers=headers, data=data)
        company_id = resp.json().get('id')

        # Next we update the company
        self.make_request('delete', self.url + '/' + company_id, headers=headers)

        r = self.make_request('get', self.url + '/' + company_id, headers=headers)
        return r.status_code == 404

    def verify_company_is_deleted_in_es(self):
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json'
        }
        data = {
            'title': self.random_string(10),
            'description': 'url',
            'url': 'http://www.foo.is',
        }

        resp = self.make_request('post', self.url, headers=headers, data=data)
        company_id = resp.json().get('id')
        self.make_request('delete', self.url + '/' + company_id, headers=headers)

        time.sleep(5)

        companies = self.make_request('get', self.url + '?max=500', headers=headers).json()
        c = filter(lambda x: x.get('title') == data.get('title'), companies)
        return len(c) == 0
