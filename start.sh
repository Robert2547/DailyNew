#!/bin/bash

# Start backend services
docker-compose up -d

# Start proxy server
cd server && node index.js &

# Start frontend
npm run dev
