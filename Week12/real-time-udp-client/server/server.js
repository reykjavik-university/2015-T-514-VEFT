'use strict';

const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const port = 1313;

server.bind(port, () => {
  console.log('Server is ready in port', port);
});

server.on('message', (msg, rinfo) => {
  const data = msg.toString()
  console.log(data);
});
