# DWSurvey - Online Voting System

A Slido-like real-time voting system that allows audiences to participate in multiple-choice polls with instant results visualization.

## Features

- **Real-time Voting**: Audiences can vote on multiple-choice questions
- **QR Code Integration**: Generate QR codes for each question/poll for easy mobile access
- **Mobile-Optimized Voting**: Dedicated mobile interface for smartphone users
- **Live Results**: See voting results update in real-time with voting status indicators
- **Poll Control**: Close voting and display final results
- **Multiple Question Support**: Create and manage multiple polls with different question types
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Anonymous Voting**: No login required for participants
- **Printable QR Codes**: Generate printer-friendly QR code sheets for events

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript with real-time updates
- **Backend**: Node.js with Express.js
- **Database**: SQLite for simplicity (can be upgraded to PostgreSQL for production)
- **Real-time Communication**: WebSockets for live updates
- **QR Code Generation**: QRCode.js library for dynamic QR code creation
- **Mobile Detection**: Express-useragent for device-specific routing
- **Deployment**: Optimized for Zeabur deployment

## Project Structure

```
DWSurvey/
├── public/              # Frontend static files
│   ├── index.html      # Main voting interface
│   ├── admin.html      # Admin panel for creating polls
│   ├── mobile.html     # Mobile-optimized voting interface
│   ├── css/            # Stylesheets
│   │   ├── style.css   # Main desktop styles
│   │   ├── admin.css   # Admin panel styles
│   │   └── mobile.css  # Mobile-specific styles
│   └── js/             # Client-side JavaScript
│       ├── main.js     # Main application logic
│       ├── admin.js    # Admin panel functionality
│       └── mobile.js   # Mobile voting interface
├── src/                # Backend source code
│   ├── app.js          # Express server setup
│   ├── routes/         # API routes
│   │   ├── polls.js    # Poll management
│   │   ├── votes.js    # Voting endpoints
│   │   ├── admin.js    # Admin functionality
│   │   └── qr.js       # QR code generation
│   ├── models/         # Database models
│   ├── db/             # Database initialization
│   └── websocket/      # WebSocket handlers
├── database/           # SQLite database files
├── package.json        # Node.js dependencies
├── .env.example        # Environment variables template
├── CLAUDE.md          # Technical documentation
└── README.md          # Deployment instructions

```

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```

4. **Access the Application**
   - Voting Interface: http://localhost:3000
   - Admin Panel: http://localhost:3000/admin.html
   - Mobile Voting: http://localhost:3000/mobile/:pollId (via QR code)

## QR Code Workflow

### 1. Create Poll with QR Codes
1. Admin creates a poll through the admin panel
2. Click "QR Codes" button to generate QR codes for each question
3. Download or print QR codes for distribution

### 2. Audience Participation
1. Participants scan QR code with their smartphones
2. Automatic redirect to mobile-optimized voting interface
3. Single-tap voting with instant feedback
4. Real-time results viewing

### 3. Poll Management
1. Admin can close voting at any time
2. Real-time status updates (Live/Closed) shown to all participants
3. Final results preserved after voting closes

## API Endpoints

### Public Endpoints
- `GET /api/polls` - Get all active polls
- `GET /api/polls/:id` - Get specific poll details
- `POST /api/votes` - Submit a vote
- `GET /api/polls/:id/results` - Get real-time results
- `GET /api/votes/check/:pollId/:sessionId` - Check if user has voted

### QR Code Endpoints
- `GET /api/qr/poll/:pollId` - Generate QR code for entire poll
- `GET /api/qr/poll/:pollId/questions` - Generate QR codes for all questions
- `GET /api/qr/poll/:pollId/print` - Printable QR code page

### Admin Endpoints (Password Required)
- `POST /api/admin/polls` - Create new poll
- `PUT /api/admin/polls/:id/status` - Update poll status
- `PUT /api/admin/polls/:id/close` - Close poll voting
- `DELETE /api/admin/polls/:id` - Delete poll
- `POST /api/admin/polls/list` - Get all polls with stats

## Deployment to Zeabur

1. Push code to GitHub repository
2. Connect repository to Zeabur
3. Set environment variables in Zeabur dashboard
4. Deploy with one click

## Environment Variables

- `PORT` - Server port (default: 3000)
- `DATABASE_URL` - Database connection string
- `ADMIN_PASSWORD` - Password for admin panel access

## Development Notes

- WebSocket connections handle real-time updates for voting and poll status
- Votes are stored with timestamps and session IDs to prevent duplicates
- QR codes are generated dynamically with customizable styling
- Mobile interface auto-detects device type and optimizes UI accordingly
- Poll closing triggers real-time notifications to all connected clients
- Admin panel requires password authentication
- Results are calculated on-the-fly for accuracy
- Database supports both active/inactive and open/closed poll states

## Mobile Features

### Responsive Design
- Touch-optimized voting interface
- Large tap targets for easy selection
- Automatic scaling for different screen sizes
- Prevents accidental zoom on input focus

### Smart Navigation
- Direct question access via QR code scanning
- Progress indicators showing question number
- Automatic detection of already-voted questions
- Seamless transition to results view

### Real-time Feedback
- Instant vote confirmation
- Live status updates (voting open/closed)
- Connection status indicators
- Error handling with retry options

## Event Management

### Pre-Event Setup
1. Create polls in admin panel
2. Generate and print QR code sheets
3. Test mobile access and voting flow
4. Distribute QR codes to audience

### During Event
1. Display QR codes on screen or handouts
2. Monitor real-time participation
3. Close voting when appropriate
4. Display final results

### Post-Event
1. Export results (future feature)
2. Archive or delete polls
3. Analyze participation metrics