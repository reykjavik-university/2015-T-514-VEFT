## Setting up a project in Node.js

*From this point we assume you already have Node.js set up on your computer and that you are located in the folder where you want your application to be set up at.*

####1.

To begin with one way is to set up the project by running ```npm init```.
**npm** or Node package manager is a service which installs, publishes and manages node programs.

After we have run the npm init command we get few steps that we need to go through, such as *name, version, description, entry point (which file starts the application), test command, git repo, keywords and license.* You can fill this out as suits you best and just press enter/return if you don’t want to fill out that specific field.
Once filled out you need to review the fields you put in and need to type in yes if you are happy with the result.

Once this step is done you should have initialised an empty project and created the file ```package.json``` which describes your project.
Add this command to initialize the empty file you want to work on: ```touch index.js``` (index.js being the name of the file).


####2.

**Express:** is a web library which is based on the HTTP module in Node.js.
It implements things like parsing the HTTP protocol, deals with HTTP status codes, adds a way to define routs to certain URLs’ and so on. 
Basically Express makes it a lot easier to build a web application in Node.js.

**Installing Express:** 
```npm install —save express```

This line allows npm to find the latest version of express or in fact any dependancy you declare in this command line and installs it into your project under a folder named ```node_modules``` (creates it for the first dependancy installed in the project automatically).

You can run: ```cat package.json``` to see all the dependancies installed in your project.
The package.json file is important, as it allows us to delete the node_modules folder from our project before, for example uploading it to github for external usage and then if the project is dependant on some dependancies we can simply run the command: npm install and then the package.json file should inform npm which dependancies should be installed in to our project.

We can use the command ```—save-dev``` instead of ```—save``` for dependancies that are not necessary for production such as testing tools like mocha and eslint 


####3.
Now the project should be ready for coding and we can open the file index.js (or what ever you have named it) and start working on the project.

You can take a look at the sample code from class [here](https://github.com/reykjavik-university/2015-T-514-VEFT/blob/master/Week08/code_examples/index.js)

But it’s good to set up in the beginning of index.js ```'use strict';``` to set the project to strict mode and add const ```express = require('express');``` to include the library installed. You need to do this for all dependancies installed.


####4.
Last but not least to run the project we use the command: ```node <name of file>``` or in our case: ```node index.js```
*Here we should already have the port number declared in the project.*


**Few curl commands from sample program:**

Simple GET command:
*curl -XGET http://localhost:<port number>*

Header of the GET command: 
*curl -XGET http://localhost:<port number> -I*

Simple POST command to url /todo:
*curl -XPOST -d “{\”title\”: \”take trash out\”}” -H “Content-Type: Application/json” http://localhost:4000/todo*


if you want to prettify your json result you can add this after your curl command: ```| python -m json.tool```

**eslint modifications:**
~root/ node_modules/eslint/bin/eslint.js —init


You can explore more packages for your Node.js project [here](http://www.npmjs.com)
