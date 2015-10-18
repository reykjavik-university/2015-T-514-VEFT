'use strict';

const express = require('express');
const api = require('./api');

const mongoose = require('mongoose');
const port = 4000;
const app = express();

app.use('/api', api);

// Connect to MongoDB
mongoose.connect('localhost/retro');
mongoose.connection.once('open', function() {
  console.log('mongoose is connected');
  app.listen(port, function() {
    console.log('server starting on port', port);
  });
});

