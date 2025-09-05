import React, { useState, useEffect } from 'react';

const HistoryViewer = () => {
  const [channels, setChannels] = useState([]);
  const [selectedChannel, setSelectedChannel] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      // API実装後に有効化
      // const response = await axios.get('/api/channels');
      // setChannels(response.data);
      
      // ダミーデータ（開発用）
      setChannels([
        { channelId: 'C1234567890', type: 'group' },
        { channelId: 'U0987654321', type: 'user' }
      ]);
    } catch (err) {
      setError('チャンネル一覧の取得に失敗しました');
    }
  };

  const fetchHistory = async (channelId) => {
    if (!channelId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // API実装後に有効化
      // const response = await axios.get(`/api/history/${channelId}`);
      // setHistory(response.data);
      
      // ダミーデータ（開発用）
      setTimeout(() => {
        setHistory([
          {
            id: '1',
            userId: 'U123',
            message: 'こんにちは！',
            timestamp: '2024-01-15 10:30:15'
          },
          {
            id: '2',
            userId: 'bot',
            message: 'こんにちは！何かお手伝いできることはありますか？',
            timestamp: '2024-01-15 10:30:18'
          },
          {
            id: '3',
            userId: 'U123',
            message: 'Pythonについて教えてください',
            timestamp: '2024-01-15 10:31:00'
          },
          {
            id: '4',
            userId: 'bot',
            message: 'Pythonは、シンプルで読みやすい構文が特徴のプログラミング言語です。データサイエンス、ウェブ開発、自動化など様々な分野で使われています。',
            timestamp: '2024-01-15 10:31:05'
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('会話履歴の取得に失敗しました');
      setLoading(false);
    }
  };

  const deleteHistory = async (channelId) => {
    if (!window.confirm('このチャンネルの会話履歴を削除しますか？')) return;
    
    try {
      // API実装後に有効化
      // await axios.delete(`/api/history/${channelId}`);
      
      // ダミーレスポンス（開発用）
      setHistory([]);
      alert('会話履歴を削除しました');
    } catch (err) {
      setError('会話履歴の削除に失敗しました');
    }
  };

  const exportHistory = () => {
    if (history.length === 0) {
      alert('エクスポートする履歴がありません');
      return;
    }
    
    const csvContent = [
      ['日時', 'ユーザーID', 'メッセージ'],
      ...history.map(item => [item.timestamp, item.userId, item.message])
    ].map(row => row.map(field => `"${field}"`).join(',')).join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `history_${selectedChannel}_${new Date().toISOString().slice(0, 10)}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <div className="card">
        <h2>会話履歴表示</h2>
        <p>チャンネルごとの会話履歴を表示・管理できます</p>
      </div>

      <div className="card">
        <h3>チャンネル選択</h3>
        <div className="form-group">
          <label>チャンネルを選択:</label>
          <select
            value={selectedChannel}
            onChange={(e) => {
              setSelectedChannel(e.target.value);
              fetchHistory(e.target.value);
            }}
          >
            <option value="">-- チャンネルを選択してください --</option>
            {channels.map(channel => (
              <option key={channel.channelId} value={channel.channelId}>
                {channel.channelId} ({channel.type === 'group' ? 'グループ' : 'ユーザー'})
              </option>
            ))}
          </select>
        </div>

        {selectedChannel && (
          <div style={{ marginTop: '15px' }}>
            <button 
              className="btn btn-primary" 
              onClick={exportHistory}
              disabled={history.length === 0}
            >
              履歴エクスポート
            </button>
            <button 
              className="btn btn-danger" 
              onClick={() => deleteHistory(selectedChannel)}
              disabled={history.length === 0}
            >
              履歴削除
            </button>
          </div>
        )}
      </div>

      {selectedChannel && (
        <div className="card">
          <h3>会話履歴 ({history.length}件)</h3>
          
          {loading && <div className="loading">読み込み中...</div>}
          {error && <div className="error">{error}</div>}
          
          {!loading && !error && (
            <>
              {history.length === 0 ? (
                <p>会話履歴がありません。</p>
              ) : (
                <div className="history-list">
                  {history.map(item => (
                    <div 
                      key={item.id} 
                      className={`history-item ${item.userId === 'bot' ? 'bot' : 'user'}`}
                    >
                      <div className="history-meta">
                        {item.timestamp} - {item.userId === 'bot' ? 'Bot' : `User: ${item.userId}`}
                      </div>
                      <div>{item.message}</div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default HistoryViewer;
