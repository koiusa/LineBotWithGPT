import Keycloak from 'keycloak-js';

// Environment variable validation and Keycloak URL determination
const getKeycloakUrl = () => {
  console.log('🌐 Window location:', window.location);
  console.log('🔒 Protocol:', window.location.protocol);
  
  const keycloakUrl = process.env.REACT_APP_KEYCLOAK_URL;
  
  // Validate environment variable
  if (!keycloakUrl) {
    console.error('❌ REACT_APP_KEYCLOAK_URL environment variable is not set!');
    console.error('💡 Please check your .env file and ensure REACT_APP_KEYCLOAK_URL is configured');
    return 'http://localhost:9999'; // Fallback URL
  }
  
  console.log('🔗 Using Keycloak URL:', keycloakUrl);
  
  // Validate URL format
  try {
    new URL(keycloakUrl);
    console.log('✅ Keycloak URL format is valid');
  } catch (error) {
    console.error('❌ Invalid Keycloak URL format:', keycloakUrl);
    console.error('💡 URL should be in format: http://localhost:9999 or https://your-domain.com');
  }
  
  return keycloakUrl;
};

// Keycloak configuration
const keycloakConfig = {
  url: getKeycloakUrl(),
  realm: 'linebot',
  clientId: 'linebot-frontend'
};

console.log('🔧 Keycloak configuration:', keycloakConfig);

const keycloak = new Keycloak(keycloakConfig);

// Enhanced debugging with detailed event listeners
keycloak.onReady = function(authenticated) {
  console.log('🚀 Keycloak Ready - Authenticated:', authenticated);
  console.log('🔑 Token present:', !!keycloak.token);
  console.log('🆔 User ID:', keycloak.subject);
};

keycloak.onAuthSuccess = function() {
  console.log('✅ Auth Success');
  console.log('🔑 Access Token:', keycloak.token ? 'Present' : 'Missing');
  console.log('🔄 Refresh Token:', keycloak.refreshToken ? 'Present' : 'Missing');
};

keycloak.onAuthError = function(errorData) {
  console.error('❌ Auth Error:', errorData);
  console.error('🔗 Keycloak URL being used:', keycloakConfig.url);
  console.error('🏠 Current origin:', window.location.origin);
  console.error('💡 Possible causes:');
  console.error('   - Keycloak server is not running');
  console.error('   - Wrong Keycloak URL in environment variables');
  console.error('   - Client "linebot-frontend" not configured in Keycloak');
  console.error('   - CORS issues between frontend and Keycloak');
};

keycloak.onAuthRefreshSuccess = function() {
  console.log('🔄 Auth Refresh Success');
};

keycloak.onAuthRefreshError = function() {
  console.error('❌ Auth Refresh Error');
  console.error('💡 Token may have expired, redirecting to login...');
};

keycloak.onTokenExpired = function() {
  console.log('⏰ Token Expired');
  console.log('🔄 Attempting to refresh token...');
  keycloak.updateToken(30)
    .then((refreshed) => {
      if (refreshed) {
        console.log('✅ Token refreshed successfully');
      } else {
        console.log('ℹ️ Token is still valid');
      }
    })
    .catch(() => {
      console.error('❌ Failed to refresh token');
    });
};

keycloak.onAuthLogout = function() {
  console.log('👋 User logged out');
};

export default keycloak;
