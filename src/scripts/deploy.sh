#!/bin/bash

# Hospital Chatbot Deployment Script
# This script helps deploy the hospital chatbot to production

set -e

echo "🏥 Hospital Chatbot Deployment Script"
echo "======================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed!"
    echo "Please install Docker and try again"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed!"
    echo "Please install Docker Compose and try again"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Build and deploy
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if the service is healthy
echo "🔍 Checking service health..."
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Hospital Chatbot is running successfully!"
    echo "🌐 Access the application at: http://localhost:8501"
else
    echo "❌ Service health check failed"
    echo "📋 Checking logs..."
    docker-compose logs --tail=20
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart:          docker-compose restart"
echo "  Update:           git pull && docker-compose up --build -d" 