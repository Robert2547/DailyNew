# Stock Market Analytics Platform
A modern web application for tracking stocks and analyzing company news using NLP. Get daily summarized news with sentiment analysis for your favorite stocks.
Quick Start
Prerequisites

Docker & Docker Compose
Node.js v18+
npm or yarn

Setup & Run

Clone the repository

bashCopygit clone [repository-url]
cd stock-market-analytics

Environment Setup

Create .env file in root directory:
envCopy# Database
DB_USER=dbuser
DB_PASSWORD=dbpassword
AUTH_DB_NAME=auth_db
USER_DB_NAME=user_db
WATCHLIST_DB_NAME=watchlist_db

# Ports

AUTH_SERVICE_PORT=8001
USER_SERVICE_PORT=8002
WATCHLIST_SERVICE_PORT=8003

# Auth

SECRET_KEY=your-secret-key

# External APIs

ALPHA_VANTAGE_API_KEY=your-api-key

Start Backend Services

bashCopydocker-compose up -d

Start Frontend Development Server

bashCopycd frontend
npm install
npm run dev
The application will be available at:

Frontend: http://localhost:5173
Backend Services:

Auth: http://localhost:8001
User: http://localhost:8002
Watchlist: http://localhost:8003

Project Structure
Copy├── AuthService/ # Auth microservice (FastAPI)
├── UserService/ # User microservice (FastAPI)
├── WatchlistService/ # Watchlist microservice (FastAPI)
├── frontend/ # React frontend
└── docker-compose.yml # Docker configuration
Tech Stack

Frontend: React, TypeScript, TailwindCSS, Shadcn UI
Backend: FastAPI, PostgreSQL
Infrastructure: Docker, Docker Compose

API Documentation

Auth Service: http://localhost:8001/docs
User Service: http://localhost:8002/docs
Watchlist Service: http://localhost:8003/docs

Development
Backend Services
Each service runs in its own container and has its own PostgreSQL database:

AuthService: User authentication & authorization
UserService: User profiles & preferences
WatchlistService: Stock watchlist management

Frontend Development
The frontend is a React application with:

TypeScript for type safety
TailwindCSS for styling
Shadcn UI for components
React Query for data fetching
Zustand for state management

Troubleshooting
Common Issues

Database Connection Issues

bashCopy# Check container status
docker ps

# View container logs

docker logs [container-name]

Port Conflicts

bashCopy# Check ports in use
lsof -i :[port-number]

# Stop conflicting service or change port in .env

Service Health Check
bashCopy# Check all services
docker-compose ps
License
MIT

For more detailed documentation, refer to individual service READMEs.
