#!/bin/bash
set -e

# Start FastAPI in the background
uvicorn api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Give the API a moment to boot before the frontend tries to fetch /categories
sleep 5

# Start Gradio (also in background so we can wait on either)
python frontend.py &
UI_PID=$!

# If either process dies, exit with its status so Docker can restart the container
wait -n $API_PID $UI_PID
exit $?