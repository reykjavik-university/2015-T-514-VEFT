'use strict';

const express = require('express');
const elasticsearch = require('elasticsearch');
const bodyParser = require('body-parser');
const uuid = require('node-uuid');

const port = 4000;
const app = express();

const client = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'error'
});

app.get('/', (req, res) => {
  res.send('Hello world');
});

app.post('/api/feed/:wall_id', bodyParser.json(), (req, res) => {
  const postId = uuid.v4();
  const data = req.body;
  data['wall_id'] = req.params.wall_id
  data['post_id'] = postId,
  data['like_counter'] = 0
  data['created'] = new Date();

  const promise = client.index({
    'index': 'feeds',
    'type': 'feed',
    'id': postId,
    'body': data,
  });

  promise.then((doc) => {
    res.send(doc)
  }, (err) => {
    res.status(500).send(err)
  });
});

app.get('/api/feed/search', bodyParser.json(), (req, res) => {
  const search = req.query.q || '';
  const promise = client.search({
    'index': 'feeds',
    'type': 'feed',
    'body': {
      'query': {
        'query_string': {
          'query': search,
        }
      }
    }
  });

  promise.then((docs) => {
    res.send(docs.hits.hits.map((x) => x._source));
  }, (err) => {
    res.status(500).send(err);
  });

});

app.get('/api/feed/:wall_id', (req, res) => {
  const wall_id = req.params.wall_id;

  const promise = client.search({
    'index': 'feeds',
    'type': 'feed',
    'body': {
      "query": {
        "match": {
          "wall_id": wall_id
        }
      }
    }
  });

  promise.then((docs) => {
    res.send(docs.hits.hits.map((x) => x._source));
  }, (err) => {
    res.status(500).send(err);
  });

});

app.listen(port, () => {
  console.log('Server starting on port', port);
});
