'use strict';
const request = require('supertest');
const app = require('../app');
const a = require('assert');


describe('api', function() {

  it('get / should return status code 200', function(done) {
    request(app).get('/').expect(200).end(function(err, res) {
      done();
    });
  });
  
  it('get /convert parameter rate is negative, we should return 412', function(done) {
    request(app).get('/convert?rate=-2').expect(412).end(function(err, res) {
      done(err);
    });
  });

});
