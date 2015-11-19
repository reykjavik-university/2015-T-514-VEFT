import requests
import json
import sys

if len(sys.argv) < 4:
	print "Proper usage: " + sys.argv[0] + " 'portno' 'admintoken' 'usertoken'"
	sys.exit()

class Company(object):
	def __init__(self, name, descr, pl):
		self.name = name
		self.description = descr
		self.punchcard_lifetime = pl

	def __str__(self):
		return str(self.__dict__)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def __ne__(self, other):
		return not self.__eq__(other)


haskolabudin = Company(u'Haskolabudin', u'10-11 in disguise', 7)
port = sys.argv[1]
url = 'http://localhost:' + port
ADMIN_TOKEN = sys.argv[2]
USER_TOKEN = sys.argv[3]

def checkEmptyCompanyDocument(url):
	r = requests.get(url)
	try:
		if len(r.json()) is not 0:
			print "ERROR: Does not return an empty list when empty using /api/companies, len is: " + str(len(r.json()))
		else:
			print "Responds correctly when sending GET to /api/companies with empty database"
	except ValueError:
		print "Not a json object, might still be a valid empty list: " + r.text

def insertCompany(url, payload):
	token = {'admin_token' : ADMIN_TOKEN}
	bad_r_auth = requests.post(url, json=payload.__dict__)
	if bad_r_auth.status_code != 401:
		print "ERROR: Does not return 401 when user is not authenticated using /api/companies, returns: "  + str(bad_r_auth.status_code)
	else:
		print "Responds correctly with 401 when posting to /api/companies without proper authentication"

	badCompany = {'name' : 'teogkaffi', 'description' : 'teogkaffi'}
	bad_r_pre = requests.post(url, json=badCompany, headers=token)
	if bad_r_pre.status_code != 412:
		print "ERROR: Does not return 412 when payload is invalid using /api/companies, returns: " + str(bad_r_pre.status_code)
	else:
		print "Responds correctly with 412 when posting to /api/company/ with invalid payload"
	
	ok_r = requests.post(url, json=payload.__dict__, headers=token)
	if ok_r.status_code != 201:
		print "ERROR: Does not return 201 after creating a company using /api/companies, returns: " + str(ok_r.status_code)
	else:
		print "Responds correctly with 201 when posting successfully to /api/companies"

	if 'company_id' not in ok_r.json():
		print "ERROR: Reponse object does not contain a company_id after creating a company using /api/companies, response: " + str(ok_r.json()) + ", stopping tests"
		sys.exit()
	else:
		print "Responds correctly with an object after posting successfully to /api/companies"

	getc_r = requests.get(url + '/' + ok_r.json()['company_id'])
	if getc_r.status_code != 200:
		print "ERROR: Does not return 200 after querying for a valid company from /api/companies/:company_id, returns " + str(getc_r.status_code)
	else:
		print "Responds correctly with 200 after querying for a valid company from /api/companies/" + ok_r.json()['company_id']

	try:
		getc_r.json()
	except ValueError:
		print "ERROR: Does not respond with a json object from /api/companies, response: " + getc_r.text + ", stopping tests"
		sys.exit()

	if 'name' not in getc_r.json()[0]:
		print "ERROR: Response object from /api/companies/ does not include 'name', stopping tests"
		sys.exit()
	if 'description' not in getc_r.json()[0]:
		print "ERROR: Response object from /api/companies/ does not include 'description', stopping tests"
		sys.exit()
	if 'punchcard_lifetime' not in getc_r.json()[0]:
		print "ERROR: Response object from /api/companies/ does not include 'punchcard_lifetime', stopping tests"
		sys.exit()

	cname = getc_r.json()[0]['name']
	cdescr = getc_r.json()[0]['description']
	cpl = getc_r.json()[0]['punchcard_lifetime']
	newComp = Company(cname, cdescr, cpl)

	if newComp != haskolabudin:
		print "ERROR: Does not return a valid company from /api/companies/:company_id"
	else:
		print "Responds with the correct object after posting a valid company to /api/companies/" + ok_r.json()['company_id']
	return ok_r.json()

def checkCompanyDocumentWithOneDocument(url):
	r = requests.get(url)
	try:
		if len(r.json()) is not 1:
			print "ERROR: Does not return the correct amount of documents using /api/documents. Should be: 1, is: " + str(len(r.json()))
		else:
			print "Responds with the correct amount of documents from GET to /api/documents"
	except ValueError:
		print "ERROR: Does not respond with a json object from /api/companies/, returns: " + r.text

def checkPunchcard(url):
	token = {'token' : USER_TOKEN}
	badToken = {'token' : 'badtoken'}
	bad_r_auth = requests.post(url, headers=badToken)
	if bad_r_auth.status_code != 401:
		print "ERROR: Does not return 401 if the user does not have a valid token using /punchcard/:company_id, returns: " + str(bad_r_auth.status_code)
	else:
		print "Responds correctly with 401 when posting to /punchcard/:company_id with an invalid token"

	ok_r = requests.post(url, headers=token)
	if ok_r.status_code != 201:
		print "ERROR: Does not return 201 if the punchcard was posted successfully using /punchcard/" + url.rpartition('/')[2] + ", returns: " + str(ok_r.status_code)
	else: 
		print "Responds correctly with 201 after successfully posting a punchcard to /punchcard/:company_id"
	if len(ok_r.json()) is 0:
		print "ERROR: Does not return an id if the punchcard was posted successfully using /punchcard/" + url.rpartition('/')[2] + "len is: " + str(len(ok_r.json()))
	else:
		print "Responds correctly with a json object after successfully posting to /punchcard/:company_id"
	bad_r_samep = requests.post(url, headers=token)
	if bad_r_samep.status_code != 409:
		print "ERROR: Does not return 409 if the same punchcard is posted twice using /punchcard/" + url.rpartition('/')[2] + ", returns: " + str(bad_r_samep.status_code)
	else:
		print "Responds correctly with 409 if the same punchcard is posted twice using /punchcard/:company_id"

def checkUsers(url):
	r = requests.get(url)
	try:
		if 'token' in r.json()[0]:
			print "ERROR: Response from /user includes a token, which it should not do"
		else:
			print "Responds correctly without a token when requesting users from /user"
	except ValueError:
		print "ERROR: Does not respond with a json object from /users/, returns: " + r.text

checkEmptyCompanyDocument(url + '/api/companies')
companyID = insertCompany(url + '/api/companies', haskolabudin)
checkCompanyDocumentWithOneDocument(url + '/api/companies')
checkUsers(url + '/user')
checkPunchcard(url + '/punchcard/' + companyID['company_id'])
