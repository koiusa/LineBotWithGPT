import React, { useState, useEffect } from 'react';

const ChannelManager = () => {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingChannel, setEditingChannel] = useState(null);

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      setLoading(true);
      // API実装後に有効化
      // const response = await axios.get('/api/channels');
      // setChannels(response.data);
      
      // ダミーデータ（開発用）
      setTimeout(() => {
        setChannels([
          {
            id: '1',
            channelId: 'C1234567890',
            type: 'group',
            prompt: 'あなたは親しみやすいアシスタントです。',
            memory: 5,
            setting: { active: true },
            timestamp: '2024-01-15 10:30:00'
          },
          {
            id: '2',
            channelId: 'U0987654321',
            type: 'user',
            prompt: 'プログラミングに関する質問に答えてください。',
            memory: 10,
            setting: { active: true },
            timestamp: '2024-01-14 15:45:00'
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('チャンネル情報の取得に失敗しました');
      setLoading(false);
    }
  };

  const updateChannel = async (channelId, updates) => {
    try {
      // API実装後に有効化
      // await axios.put(`/api/channels/${channelId}`, updates);
      
      // ダミーレスポンス（開発用）
      setChannels(channels.map(channel => 
        channel.channelId === channelId 
          ? { ...channel, ...updates }
          : channel
      ));
      setEditingChannel(null);
    } catch (err) {
      setError('チャンネル情報の更新に失敗しました');
    }
  };

  const deleteChannel = async (channelId) => {
    if (!window.confirm('このチャンネルを削除しますか？')) return;
    
    try {
      // API実装後に有効化
      // await axios.delete(`/api/channels/${channelId}`);
      
      // ダミーレスポンス（開発用）
      setChannels(channels.filter(channel => channel.channelId !== channelId));
    } catch (err) {
      setError('チャンネルの削除に失敗しました');
    }
  };

  if (loading) return <div className="loading">読み込み中...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div>
      <div className="card">
        <h2>チャンネル管理</h2>
        <p>LINE Botが利用されているチャンネルの一覧と設定管理</p>
      </div>

      <div className="card">
        <h3>登録チャンネル一覧 ({channels.length}件)</h3>
        {channels.length === 0 ? (
          <p>登録されているチャンネルがありません。</p>
        ) : (
          <ul className="channel-list">
            {channels.map(channel => (
              <li key={channel.id} className="channel-item">
                {editingChannel === channel.channelId ? (
                  <EditChannelForm 
                    channel={channel}
                    onSave={(updates) => updateChannel(channel.channelId, updates)}
                    onCancel={() => setEditingChannel(null)}
                  />
                ) : (
                  <ChannelDisplay 
                    channel={channel}
                    onEdit={() => setEditingChannel(channel.channelId)}
                    onDelete={() => deleteChannel(channel.channelId)}
                  />
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

const ChannelDisplay = ({ channel, onEdit, onDelete }) => (
  <div>
    <h3>チャンネルID: {channel.channelId}</h3>
    <p><strong>タイプ:</strong> {channel.type === 'group' ? 'グループ' : 'ユーザー'}</p>
    <p><strong>プロンプト:</strong> {channel.prompt || '未設定'}</p>
    <p><strong>記憶数:</strong> {channel.memory}</p>
    <p><strong>状態:</strong> {channel.setting?.active ? 'アクティブ' : '非アクティブ'}</p>
    <p><strong>登録日時:</strong> {channel.timestamp}</p>
    
    <div style={{ marginTop: '10px' }}>
      <button className="btn btn-primary" onClick={onEdit}>
        編集
      </button>
      <button className="btn btn-danger" onClick={onDelete}>
        削除
      </button>
    </div>
  </div>
);

const EditChannelForm = ({ channel, onSave, onCancel }) => {
  const [prompt, setPrompt] = useState(channel.prompt || '');
  const [memory, setMemory] = useState(channel.memory || 5);
  const [active, setActive] = useState(channel.setting?.active || true);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      prompt: prompt.trim() || null,
      memory: parseInt(memory),
      setting: { active }
    });
  };

  return (
    <div>
      <h3>チャンネル設定編集: {channel.channelId}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>プロンプト（AIの役割）:</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="AIの役割や性格を設定してください"
          />
        </div>
        
        <div className="form-group">
          <label>記憶数（最大10）:</label>
          <input
            type="number"
            min="0"
            max="10"
            value={memory}
            onChange={(e) => setMemory(e.target.value)}
          />
        </div>
        
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={active}
              onChange={(e) => setActive(e.target.checked)}
            />
            アクティブ
          </label>
        </div>
        
        <div>
          <button type="submit" className="btn btn-primary">
            保存
          </button>
          <button type="button" className="btn" onClick={onCancel}>
            キャンセル
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChannelManager;
