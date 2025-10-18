#!/bin/bash

# Tree Whisperer Deployment Script for DigitalOcean

set -e

echo "🌲 Deploying Tree Whisperer to DigitalOcean..."

# Check if required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Error: SECRET_KEY environment variable is not set"
    exit 1
fi

# Create .env file
echo "📝 Creating environment configuration..."
cat > .env << EOF
# Database Configuration
DB_HOST=mysql
DB_PORT=3306
DB_NAME=tree_whisperer
DB_USER=tree_user
DB_PASSWORD=secure_password_change_me

# OpenAI Configuration
OPENAI_API_KEY=$OPENAI_API_KEY
OPENAI_MODEL=gpt-3.5-turbo

# Security Configuration
SECRET_KEY=$SECRET_KEY
RATE_LIMIT_PER_MINUTE=1
DAILY_QUERY_LIMIT=100

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Application Configuration
DEBUG=false
HOST=0.0.0.0
PORT=5000
EOF

# Create logs directory
mkdir -p logs

# Set proper permissions
chmod 755 deploy.sh
chmod 644 .env

echo "🐳 Building and starting Docker containers..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."
if curl -f http://localhost/api/health > /dev/null 2>&1; then
    echo "✅ Tree Whisperer is running successfully!"
    echo "🌐 Access the application at: http://your-server-ip"
    echo "📊 Health check: http://your-server-ip/api/health"
else
    echo "❌ Health check failed. Checking logs..."
    docker-compose logs app
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update your domain DNS to point to this server"
echo "2. Configure SSL certificates in ./ssl/ directory"
echo "3. Update nginx.conf to use your domain name"
echo "4. Restart nginx: docker-compose restart nginx"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
