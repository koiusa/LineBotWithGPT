import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ChannelManager from './components/ChannelManager';
import HistoryViewer from './components/HistoryViewer';
import Settings from './components/Settings';
import keycloak from './keycloak';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const redirectUri = window.location.origin + '/';
    console.log('🔄 Keycloak初期化開始: redirectUri =', redirectUri);
    console.log('🌍 Environment details:');
    console.log('   - Origin:', window.location.origin);
    console.log('   - Protocol:', window.location.protocol);
    console.log('   - Hostname:', window.location.hostname);
    console.log('   - Port:', window.location.port);
    
    // Enhanced Keycloak initialization with robust error handling
    const initOptions = {
      onLoad: 'login-required',
      checkLoginIframe: false,
      redirectUri: redirectUri,
      // Enhanced configuration for better reliability
      enableLogging: true,
      // Disable login iframe for development to avoid CORS issues
      checkLoginIframeInterval: 0,
      // Set response mode for better compatibility
      responseMode: 'fragment'
    };
    
    console.log('🔧 Keycloak init options:', initOptions);
    
    keycloak.init(initOptions)
    .then(authenticated => {
      console.log('✅ Keycloak初期化完了:', authenticated);
      if (authenticated) {
        console.log('🎉 User is authenticated!');
        console.log('🔑 Token info:');
        console.log('   - Has token:', !!keycloak.token);
        console.log('   - Has refresh token:', !!keycloak.refreshToken);
        console.log('   - Token expires in:', keycloak.tokenParsed?.exp ? new Date(keycloak.tokenParsed.exp * 1000) : 'Unknown');
      } else {
        console.log('🔒 User not authenticated, should redirect to login');
      }
      setAuthenticated(authenticated);
      setLoading(false);
    })
    .catch((error) => {
      console.error('❌ Keycloak初期化失敗:', error);
      console.error('🔍 Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });
      console.error('💡 Troubleshooting tips:');
      console.error('   1. Check if Keycloak server is running at the configured URL');
      console.error('   2. Verify REACT_APP_KEYCLOAK_URL environment variable');
      console.error('   3. Ensure "linebot-frontend" client exists in Keycloak realm "linebot"');
      console.error('   4. Check Keycloak client configuration for valid redirect URIs');
      console.error('   5. Verify CORS settings in Keycloak');
      setLoading(false);
    });
  }, []);

  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'channels':
        return <ChannelManager />;
      case 'history':
        return <HistoryViewer />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div>🔄 認証中...</div>
        <div style={{ fontSize: '12px', color: '#666', marginTop: '10px' }}>
          URL: {window.location.origin}
        </div>
        <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
          Keycloak URL: {process.env.REACT_APP_KEYCLOAK_URL}
        </div>
        <div style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
          Keycloakサーバーに接続しています...
        </div>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div>🔐 ログイン中...</div>
        <div style={{ fontSize: '12px', color: '#666', marginTop: '10px' }}>
          Keycloakにリダイレクトしています...
        </div>
        <div style={{ fontSize: '11px', color: '#999', marginTop: '10px' }}>
          <div>Keycloak URL: {process.env.REACT_APP_KEYCLOAK_URL}</div>
          <div>Frontend URL: {window.location.origin}</div>
        </div>
        <div style={{ marginTop: '15px' }}>
          <button onClick={() => window.location.reload()} style={{ marginRight: '10px' }}>
            🔄 再試行
          </button>
          <button onClick={() => {
            console.log('🔍 Manual login attempt');
            keycloak.login();
          }}>
            🔑 手動ログイン
          </button>
        </div>
        <div style={{ fontSize: '11px', color: '#999', marginTop: '15px' }}>
          認証に問題がある場合は、ブラウザの開発者ツールのコンソールを確認してください
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <header className="header">
          <div className="container">
            <h1>LINE Bot GPT 管理画面</h1>
            <button onClick={() => keycloak.logout()} style={{ float: 'right' }}>
              ログアウト
            </button>
          </div>
        </header>
        
        <div className="container">
          <nav className="nav">
            <button 
              className={activeTab === 'dashboard' ? 'active' : ''}
              onClick={() => setActiveTab('dashboard')}
            >
              ダッシュボード
            </button>
            <button 
              className={activeTab === 'channels' ? 'active' : ''}
              onClick={() => setActiveTab('channels')}
            >
              チャンネル管理
            </button>
            <button 
              className={activeTab === 'history' ? 'active' : ''}
              onClick={() => setActiveTab('history')}
            >
              会話履歴
            </button>
            <button 
              className={activeTab === 'settings' ? 'active' : ''}
              onClick={() => setActiveTab('settings')}
            >
              設定
            </button>
          </nav>

          {renderActiveComponent()}
        </div>
      </div>
    </Router>
  );
}

export default App;
