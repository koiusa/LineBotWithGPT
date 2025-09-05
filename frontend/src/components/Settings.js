import React, { useState, useEffect } from 'react';

const Settings = () => {
  const [settings, setSettings] = useState({
    openaiModel: 'gpt-4.1-turbo',
    defaultMemory: 5,
    maxMemory: 10,
    systemPrompt: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      // API実装後に有効化
      // const response = await axios.get('/api/settings');
      // setSettings(response.data);
      
      // ダミーデータ（開発用）
      setTimeout(() => {
        setSettings({
          openaiModel: 'gpt-4.1-turbo',
          defaultMemory: 5,
          maxMemory: 10,
          systemPrompt: 'あなたは親しみやすいアシスタントです。'
        });
        setLoading(false);
      }, 500);
    } catch (err) {
      setError('設定の取得に失敗しました');
      setLoading(false);
    }
  };

  const saveSettings = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // API実装後に有効化
      // await axios.put('/api/settings', settings);
      
      // ダミーレスポンス（開発用）
      setTimeout(() => {
        setSuccess(true);
        setLoading(false);
        setTimeout(() => setSuccess(false), 4000);
      }, 500);
    } catch (err) {
      setError('設定の保存に失敗しました');
      setLoading(false);
    }
  };

  const testConnection = async () => {
    setLoading(true);
    setError(null);

    try {
      // API実装後に有効化
      // const response = await axios.post('/api/test-connection');
      
      // ダミーレスポンス（開発用）
      setTimeout(() => {
        alert('OpenAI APIへの接続テストが成功しました');
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('接続テストに失敗しました');
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div>
      <div className="card">
        <h2>システム設定</h2>
        <p>OpenAIモデルやその他のシステム設定を管理できます</p>
      </div>

      {error && <div className="error">{error}</div>}
      {success && (
        <div style={{ backgroundColor: '#d4edda', color: '#155724', padding: '10px', borderRadius: '5px', marginBottom: '20px' }}>
          設定を保存しました
        </div>
      )}

      <form onSubmit={saveSettings}>
        <div className="card">
          <h3>OpenAI設定</h3>
          
          <div className="form-group">
            <label>OpenAIモデル:</label>
            <select
              value={settings.openaiModel}
              onChange={(e) => handleInputChange('openaiModel', e.target.value)}
            >
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4.1-turbo">GPT-4.1 Turbo</option>
              <option value="gpt-4o">GPT-4o</option>
            </select>
          </div>

          <div className="form-group">
            <label>システムプロンプト（デフォルト）:</label>
            <textarea
              value={settings.systemPrompt}
              onChange={(e) => handleInputChange('systemPrompt', e.target.value)}
              placeholder="デフォルトのシステムプロンプトを設定してください"
              rows="4"
            />
          </div>

          <button 
            type="button" 
            className="btn btn-primary" 
            onClick={testConnection}
            disabled={loading}
          >
            {loading ? '接続テスト中...' : 'OpenAI接続テスト'}
          </button>
        </div>

        <div className="card">
          <h3>メモリ設定</h3>
          
          <div className="form-group">
            <label>デフォルト記憶数:</label>
            <input
              type="number"
              min="0"
              max={settings.maxMemory}
              value={settings.defaultMemory}
              onChange={(e) => handleInputChange('defaultMemory', parseInt(e.target.value))}
            />
            <small style={{ display: 'block', color: '#666', marginTop: '5px' }}>
              新しいチャンネルのデフォルト記憶数
            </small>
          </div>

          <div className="form-group">
            <label>最大記憶数:</label>
            <input
              type="number"
              min="1"
              max="50"
              value={settings.maxMemory}
              onChange={(e) => handleInputChange('maxMemory', parseInt(e.target.value))}
            />
            <small style={{ display: 'block', color: '#666', marginTop: '5px' }}>
              各チャンネルで設定可能な最大記憶数
            </small>
          </div>
        </div>

        <div className="card">
          <h3>ステッカーコマンド設定</h3>
          
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f8f9fa' }}>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>コマンド</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>パッケージID</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>ステッカーID</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>アクション</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>prompt</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>1</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>4</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>1</td>
                </tr>
                <tr>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>status</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>1</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>2</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>2</td>
                </tr>
                <tr>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>delete_histoly</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>1</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>10</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>3</td>
                </tr>
                <tr>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>memory</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>1</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>13</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>4</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <p style={{ marginTop: '15px', color: '#666', fontSize: '14px' }}>
            ステッカーコマンドの設定はstickercommand.jsonファイルで管理されています。
          </p>
        </div>

        <div className="card">
          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={loading}
          >
            {loading ? '保存中...' : '設定を保存'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Settings;
