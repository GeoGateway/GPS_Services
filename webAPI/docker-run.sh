#!/bin/bash
# Script to run the GPS Service container

echo "Starting GPS Service with Docker Compose..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✓ GPS Service is running!"
    echo "Access the service at: http://localhost:5000/gpsservice/test"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
else
    echo "✗ Failed to start GPS Service"
    exit 1
fi
