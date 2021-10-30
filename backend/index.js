const redis = require('redis');
const http = require('http');
const client = redis.createClient();
const express = require('express');
const compression = require('compression');
const app = express();
const httpServer = http.createServer(app);
const sio = require('socket.io');

let piSocket = '';

const io = sio(httpServer, {
  cors: {
    origin        : '*',
    methods       : '*',
    allowedHeaders: '*',
    credentials   : false,
  },
});

app.use(compression()); //use compression
app.use(express.json());

app.get('/hello', function (req, res) {
  res.json({message: 'hello'});
});

//Whenever someone connects this gets executed
io.on('connection', function (socket) {
  console.log('A user connected');

  socket.on('raspberrypi', function () {
    piSocket = socket.id;
    socket.join(piSocket);
  });

  //Whenever someone disconnects this piece of code executed
  socket.on('disconnect', function () {
    console.log('A user disconnected');
  });

  socket.on('TOGGLE_MOTOR', function (data, socketId) {
    console.log(data);
    io.to(piSocket)
      .emit('TOGGLE_MOTOR_PI', data);
  });

  socket.on('TRIGGER_SNAPSHOT', function (data) {
    console.log(data);
    io.to(piSocket)
      .emit('TRIGGER_SNAPSHOT_PI', data);
  });
});


httpServer.listen(4001, function () {
  console.log('listening on *:4001');
});
