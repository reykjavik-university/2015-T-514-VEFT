#Tester for Assignment08

##Setup
Assuming you have the pip package manager for python, run '**pip install -r requirements.txt**', this installs the 'requests' dependency for python needed to send the requests to the api.

The tester assumes that the database is empty(Use db.dropDatabase() in the mongo shell to empty a database), that there is at least one entry in the users document with a token, and that the api is running on localhost.

##Run
Example(assuming admin_token is 'admintoken', portnumber is 4000):

In the mongo shell, drop the database and insert a document in to the users collection with a {token : test}:
```
db.dropDatabase()
db.users.insert({'token' : 'test'})
```

In the terminal, run testapi with the corresponding parameters:
```
python testapi.py 4000 admintoken test
```

First parameter(4000) is the port the server is listening on

Second parameter(admintoken) is the ADMIN_TOKEN hardcoded into the api

Third parameter(test) is the token of a user in the databse

###Easy mode Run
Use '**sh testscript.sh portno admintoken**', where portno is the port the api is listening on and admintoken is the hardcoded ADMIN_TOKEN. (You might need to '**chmod -x testscript.sh**' to make it executable).

This handles dropping the database, inserting a user with token 'test' and then starting the tester with the correct parameters.
