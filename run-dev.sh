#!/bin/bash
set -e
cd qrscanner
poetry run uvicorn qrscanner.web:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

cd qrscanner-web
npm run dev &
FRONTEND_PID=$!
cd ..

trap "echo ' Stopping...'; kill $BACKEND_PID $FRONTEND_PID" EXIT

wait
