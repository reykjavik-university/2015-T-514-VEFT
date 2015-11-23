# Setting Visual Code up for Node/Express

To get node/express support in Visual Code (IntelliSense and more): 

Open a terminal/command prompt and enter the following commands: 

npm install -g tsd 

tsd query node --action install

tsd query express --action install 

If, when you installed Visual Code from: https://www.visualstudio.com/en-us/products/code-vs.aspx you selected to add Code to your right-click menu: Right click your node project and select open with code. 

If you didn't, enter the directory and open a terminal there, and enter 'code .'. This will open the whole (folder-based) project. 

To get rid of the "This can only be used with ES6" error in your node file (assuming you're using ES6 syntax): Hover over the name of your opened folder in Visual Code, select new file, and name it jsconfig.json.

Insert the following: 

{
    "compilerOptions": {
        "target": "ES6",
        "module": "commonjs"
    }
}

We save this, and the error should be no more. 

## Debugging JavaScript (or rather, Node) in Visual Code: 

We must specify how to start the app. 

1. Press the debugging bug on the left side of Code. 

Okay so in here.. when we press the cog (settings.symbol), Code will attempt to create launch.json. It looks in package.json for the start script (the one used for npm start) for how to start the app.

So 2. Go to package.json, and to the root object, add the following: 

"scripts": {
    "start": "node app.js"
}

Now we can finally press the cog on the menu we got after we pressed the debugging bug. This will create launch.json.

We should now be able to set a breakpoint, and press F5 to debug the app.

You should now be able to debug the way you'd expect: Step your way through the code, add watches on the left hand panel to watch individual variables or simply hover over the ones you're going over in the code.
You can also see the local variables on the left hand-side. 
