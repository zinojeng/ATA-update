const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

const pollRoutes = require('./routes/polls');
const voteRoutes = require('./routes/votes');
const adminRoutes = require('./routes/admin');
const qrRoutes = require('./routes/qr');
const setupWebSocket = require('./websocket/socketHandler');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Static files
app.use(express.static(path.join(__dirname, '../public')));

// Mobile routes
app.get('/mobile/:pollId/:questionId?', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/mobile.html'));
});

// API Routes
app.use('/api/polls', pollRoutes);
app.use('/api/votes', voteRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/qr', qrRoutes);

// WebSocket setup
setupWebSocket(io);

// Make io available to routes
app.set('io', io);

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something went wrong!');
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Access the app at:`);
  console.log(`  - http://192.168.1.118:${PORT}`);
  console.log(`  - http://localhost:${PORT}`);
  console.log(`  - http://127.0.0.1:${PORT}`);
});