#!/bin/bash

# Start the backend (Uvicorn)
cd /app/backend
poetry lock
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Start the frontend (Vite)
cd /app/frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

# Function to gracefully shut down processes
function cleanup {
  echo "Stopping processes..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  wait $BACKEND_PID
  wait $FRONTEND_PID
  echo "Processes stopped."
}

# Trap SIGTERM and SIGINT to call the cleanup function
trap cleanup SIGTERM SIGINT

# Wait for both background processes to complete (which they won't in dev mode)
# This keeps the script running indefinitely, allowing the trap to catch signals
wait $BACKEND_PID
wait $FRONTEND_PID
