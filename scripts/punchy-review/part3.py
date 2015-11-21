from base import BasePart


class Test(BasePart):
    """GET /companies/:id - 20%"""
    tests = [
        ('verify_fetch_company_by_id', 10),
        ('verify_company_fields', 10),
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
            }, headers=headers)

            self.company = self.company.json()
        except Exception as ex:
            print 'Unable to create test companies', ex.message

        if not self.company.get('id'):
            raise Exception('Unable to fetch company id for created company')

    def verify_fetch_company_by_id(self):
        headers = {
            'admin_token': self.admin_token,
            'content_type': 'application/json'
        }

        try:
            fetched_company = self.make_request('get',
                                                self.url + '/' + self.company.get('id'),
                                                headers=headers).json()

            if 'id' in fetched_company:
                fetched_company_id = fetched_company.get('id')
            elif '_id' in fetched_company:
                fetched_company_id = fetched_company.get('_id')
            elif '__id' in fetched_company:
                fetched_company_id = fetched_company.get('__id')
            else:
                return False
            return fetched_company_id == self.company.get('id')

        except Exception as ex:
            print ex
            return False

    def verify_company_fields(self):
        headers = {
            'admin_token': self.admin_token,
            'content-type': 'application/json'
        }
        resp = self.make_request('get', self.url + '/' + self.company.get('id'), headers=headers)

        try:
            company = resp.json()
            company_keys = company.keys()

            if 'id' in company_keys:
                company_keys.remove('id')
            if '_id' in company_keys:
                company_keys.remove('_id')
            if '__id' in company_keys:
                company_keys.remove('__id')

            k = ['url', 'title', 'description']
            return set(company_keys) == set(k)
        except Exception as ex:
            print ex
            return False
