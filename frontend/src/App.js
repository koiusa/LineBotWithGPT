import React, { useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ChannelManager from './components/ChannelManager';
import HistoryViewer from './components/HistoryViewer';
import Settings from './components/Settings';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

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

  return (
    <Router>
      <div className="App">
        <header className="header">
          <div className="container">
            <h1>LINE Bot GPT 管理画面</h1>
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
