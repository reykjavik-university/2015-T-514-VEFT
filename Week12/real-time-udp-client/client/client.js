'use strict';

const dgram = require('dgram');

const createClient = (host, port) => {
  return {
    'send': (key, metric) => {
      const message = new Buffer(key + ';' + metric);
      const client = dgram.createSocket("udp4");
      client.send(message, 0, message.length, port, host, function(err) {
        client.close();
      });
    }
  };
};

module.exports = createClient;

