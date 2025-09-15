#!/bin/bash

# LineBotWithGPT Keycloak Setup Script
echo "🚀 LineBotWithGPT Keycloak Setup"
echo "==============================="

# Function to check if file exists and create it if not
setup_env_file() {
    local example_file=$1
    local target_file=$2
    
    if [ ! -f "$target_file" ]; then
        echo "📄 Creating $target_file from $example_file..."
        cp "$example_file" "$target_file"
        echo "✅ $target_file created"
        echo "⚠️  Please edit $target_file and configure the required variables"
        return 1
    else
        echo "✅ $target_file already exists"
        return 0
    fi
}

# Setup environment files
env_configured=true
setup_env_file ".env.example" ".env" || env_configured=false
setup_env_file "frontend/.env.example" "frontend/.env" || env_configured=false

if [ "$env_configured" = false ]; then
    echo ""
    echo "🔧 Please configure the following variables in .env:"
    echo "   - KEYCLOAK_ADMIN (admin username for Keycloak)"
    echo "   - KEYCLOAK_ADMIN_PASSWORD (admin password for Keycloak)"
    echo "   - Other database and API settings as needed"
    echo ""
    echo "🔧 Frontend environment (.env) is already configured with:"
    echo "   - REACT_APP_KEYCLOAK_URL=http://localhost:9999"
    echo ""
    read -p "Press Enter after configuring .env files to continue..."
fi

echo ""
echo "🐳 Starting Keycloak server..."
docker-compose up -d linebot-gpt-keycloak

echo "⏳ Waiting for Keycloak to start..."
sleep 10

# Wait for Keycloak to be ready
echo "🔍 Checking Keycloak availability..."
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s --connect-timeout 5 "http://localhost:9999/health/ready" > /dev/null 2>&1; then
        echo "✅ Keycloak is ready!"
        break
    else
        echo "⏳ Waiting for Keycloak... (attempt $attempt/$max_attempts)"
        sleep 5
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Keycloak failed to start within expected time"
    echo "🔍 Check logs with: docker logs linebot-gpt-keycloak"
    exit 1
fi

echo ""
echo "🎉 Keycloak Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. 🌐 Access Keycloak Admin Console: http://localhost:9999"
echo "2. 🔑 Login with admin credentials from your .env file"
echo "3. 🏠 Create a new realm called 'linebot'"
echo "4. 👤 Create a new client with these settings:"
echo "   - Client ID: linebot-frontend"
echo "   - Access Type: public"
echo "   - Valid Redirect URIs:"
echo "     * http://localhost:3000/*"
echo "     * http://localhost:13000/*"
echo "   - Web Origins:"
echo "     * http://localhost:3000"
echo "     * http://localhost:13000"
echo ""
echo "5. 🚀 Start the full application:"
echo "   docker-compose up -d"
echo ""
echo "6. 🌍 Access the frontend:"
echo "   - Development: http://localhost:3000"
echo "   - Production: http://localhost:13000"
echo ""
echo "🔧 Troubleshooting:"
echo "   Run ./validate-keycloak.sh to diagnose issues"