import Keycloak from 'keycloak-js';

// HTTPS環境対応のKeycloak設定
const getKeycloakUrl = () => {
  console.log('🌐 Window location:', window.location);
  console.log('🔒 Protocol:', window.location.protocol);
  
  // 開発環境のHTTPS設定
  const keycloakUrl = process.env.REACT_APP_KEYCLOAK_URL;
  console.log('🔗 Using Keycloak URL:', keycloakUrl);
  return keycloakUrl;
};

const keycloak = new Keycloak({
  url: getKeycloakUrl(),
  realm: 'linebot',
  clientId: 'linebot-frontend'
});

// デバッグ用のイベントリスナー
keycloak.onReady = function(authenticated) {
  console.log('🚀 Keycloak Ready - Authenticated:', authenticated);
};

keycloak.onAuthSuccess = function() {
  console.log('✅ Auth Success');
};

keycloak.onAuthError = function(errorData) {
  console.error('❌ Auth Error:', errorData);
};

keycloak.onAuthRefreshSuccess = function() {
  console.log('🔄 Auth Refresh Success');
};

keycloak.onAuthRefreshError = function() {
  console.error('❌ Auth Refresh Error');
};

keycloak.onTokenExpired = function() {
  console.log('⏰ Token Expired');
};

export default keycloak;
