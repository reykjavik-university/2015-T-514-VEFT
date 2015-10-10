'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const uuid = require('node-uuid');
const _ = require('lodash');

const port = 4000;
const app = express();
const todos = [];

app.use(bodyParser.json());

app.get('/todo', (req, res) => {
  res.send(todos);
});

app.get('/todo/:id', (req, res) => {
  const id = req.params.id;
  console.log(req.headers);

  const todoEntry = _.find(todos, (todo) => {
    return todo.id === id;
  });

  if (todoEntry) {
    res.send(todoEntry);
  } else {
    // Example how we can set response headers.
    res.set('Some', 'Header');
    res.status(404).send('No todo entry found');
  }
});

app.post('/todo', (req, res) => {
  const data = req.body;
  if (!data.hasOwnProperty('title')) {
    res.status(412).send('missing title');
    return;
  }

  if (!data.hasOwnProperty('category')) {
    res.status(412).send('missing category');
    return;
  }
  data.timestamp = new Date();
  data.id = uuid.v4();
  todos.push(data);
  res.status(201).send(data);
});


app.listen(port, () => {
  console.log('Server is on port', port);
});
