#!/bin/bash

# Keycloak validation script
echo "🔍 Keycloak Configuration Validation"
echo "===================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
else
    echo "✅ .env file found"
fi

# Load environment variables
set -a
source .env
set +a

# Check if frontend .env exists
if [ ! -f frontend/.env ]; then
    echo "⚠️  frontend/.env file not found. Please copy frontend/.env.example to frontend/.env"
else
    echo "✅ frontend/.env file found"
    set -a
    source frontend/.env
    set +a
fi

echo ""
echo "🔧 Environment Variables:"
echo "KEYCLOAK_ADMIN: ${KEYCLOAK_ADMIN:-'NOT SET'}"
echo "KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD:+SET}"
echo "REACT_APP_KEYCLOAK_URL: ${REACT_APP_KEYCLOAK_URL:-'NOT SET'}"

echo ""
echo "🌐 Network Connectivity Tests:"

# Check if Keycloak URL is accessible
if [ ! -z "$REACT_APP_KEYCLOAK_URL" ]; then
    echo "Testing connectivity to $REACT_APP_KEYCLOAK_URL..."
    if curl -s --connect-timeout 5 "$REACT_APP_KEYCLOAK_URL/health/ready" > /dev/null 2>&1; then
        echo "✅ Keycloak server is accessible"
    else
        echo "❌ Cannot connect to Keycloak server"
        echo "💡 Make sure Keycloak is running: docker-compose up linebot-gpt-keycloak"
    fi
else
    echo "❌ REACT_APP_KEYCLOAK_URL not set"
fi

echo ""
echo "🐳 Docker Container Status:"
if command -v docker &> /dev/null; then
    if docker ps | grep -q linebot-gpt-keycloak; then
        echo "✅ Keycloak container is running"
        echo "   Container: $(docker ps --format 'table {{.Names}}\t{{.Status}}' | grep linebot-gpt-keycloak)"
    else
        echo "❌ Keycloak container is not running"
        echo "💡 Start it with: docker-compose up -d linebot-gpt-keycloak"
    fi
else
    echo "⚠️  Docker command not available"
fi

echo ""
echo "📋 Configuration Checklist:"
echo "1. ✅ Copy .env.example to .env and configure variables"
echo "2. ✅ Copy frontend/.env.example to frontend/.env" 
echo "3. 🔧 Start Keycloak: docker-compose up -d linebot-gpt-keycloak"
echo "4. 🌐 Access Keycloak admin: http://localhost:9999"
echo "5. 🔑 Create realm 'linebot' if it doesn't exist"
echo "6. 👤 Create client 'linebot-frontend' with these settings:"
echo "   - Client ID: linebot-frontend"
echo "   - Access Type: public"
echo "   - Valid Redirect URIs: http://localhost:3000/*, http://localhost:13000/*"
echo "   - Web Origins: http://localhost:3000, http://localhost:13000"
echo ""
echo "🔗 Useful URLs:"
echo "   Keycloak Admin: ${REACT_APP_KEYCLOAK_URL:-http://localhost:9999}"
echo "   Frontend: http://localhost:3000 (dev) or http://localhost:13000 (docker)"