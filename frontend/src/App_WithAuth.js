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
    
    // HTTPS環境対応のKeycloak初期化
    keycloak.init({
      onLoad: 'login-required',
      checkLoginIframe: false,
    })
    .then(authenticated => {
      console.log('✅ Keycloak初期化完了:', authenticated);
      setAuthenticated(authenticated);
      setLoading(false);
    })
    .catch((error) => {
      console.error('❌ Keycloak初期化失敗:', error);
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
        <button onClick={() => window.location.reload()} style={{ marginTop: '10px' }}>
          🔄 再試行
        </button>
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
