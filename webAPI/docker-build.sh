#!/bin/bash
# Script to build the Docker image

echo "Building GPS Service Docker image..."
docker build -t gps-service:latest .

if [ $? -eq 0 ]; then
    echo "✓ Docker image built successfully!"
    echo "Run 'docker-compose up' to start the service"
else
    echo "✗ Docker build failed"
    exit 1
fi
