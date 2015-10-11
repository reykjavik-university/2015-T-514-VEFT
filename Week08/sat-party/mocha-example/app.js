'use strict';

const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('hello world');
});

app.get('/convert', (req, res) => {
  console.log(req.query);
  const convert = req.query.rate || 0;

  if (convert > 0) {
    res.status(412).send('Invalid data');
    return;
  }
  

  res.send('hello world');
});


module.exports = app;
