import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalChannels: 0,
    totalMessages: 0,
    activeChannels: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      // API実装後に有効化
      // const response = await axios.get('/api/stats');
      // setStats(response.data);
      
      // ダミーデータ（開発用）
      setTimeout(() => {
        setStats({
          totalChannels: 5,
          totalMessages: 150,
          activeChannels: 3
        });
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('統計データの取得に失敗しました');
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">読み込み中...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div>
      <div className="card">
        <h2>システム概要</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#e3f2fd', borderRadius: '8px' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#1976d2' }}>{stats.totalChannels}</h3>
            <p style={{ margin: 0 }}>総チャンネル数</p>
          </div>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f3e5f5', borderRadius: '8px' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#7b1fa2' }}>{stats.totalMessages}</h3>
            <p style={{ margin: 0 }}>総メッセージ数</p>
          </div>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#e8f5e8', borderRadius: '8px' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#388e3c' }}>{stats.activeChannels}</h3>
            <p style={{ margin: 0 }}>アクティブチャンネル</p>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>機能一覧</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
          <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>チャンネル管理</h4>
            <p>LINE Botが利用されているチャンネルの一覧表示と設定管理</p>
          </div>
          <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>会話履歴表示</h4>
            <p>各チャンネルでの会話履歴の表示と削除機能</p>
          </div>
          <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>プロンプト設定</h4>
            <p>AIの役割やペルソナの設定・変更</p>
          </div>
          <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>システム設定</h4>
            <p>OpenAIモデルやその他のシステム設定</p>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>ステッカーコマンド一覧</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f8f9fa' }}>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>コマンド</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>説明</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>タイプ</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>prompt</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>AIの役割を設定</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>receive</td>
              </tr>
              <tr>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>status</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>チャンネル状態表示</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>reactive</td>
              </tr>
              <tr>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>delete_histoly</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>会話履歴削除</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>receive</td>
              </tr>
              <tr>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>memory</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>記憶数設定</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>receive</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
