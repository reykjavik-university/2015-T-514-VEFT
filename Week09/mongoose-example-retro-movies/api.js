'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const models = require('./models');
const api = express();

api.get('/movies', (req, res) => {
  models.Movie.find({}, function(err, docs) {
    if (err) {
      res.status(500).send(err);
      return;
    }
    else {
      res.send(docs);
    }
  });
});

api.post('/movies', bodyParser.json(), (req, res) => {
  const m = new models.Movie(req.body);
  m.save(function(err, doc) {
    if (err) {
      res.status(500).send(err);
      return;
    }
    else {
      res.send(doc);
      return;
    }
  })
});

module.exports = api;
