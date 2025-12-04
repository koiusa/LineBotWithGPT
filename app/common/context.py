from linebot import (LineBotApi, WebhookHandler)
from linebot.models import TextSendMessage


class eventcontext:
    types = ["text", "sticker", "image"]
    line_event = None
    line_bot_api = None
    # LINEメッセージの最大文字数制限
    MAX_MESSAGE_LENGTH = 1000

    def __init__(self, event: WebhookHandler, linebot: LineBotApi):
        self.line_event = event
        self.line_bot_api = linebot
        print(self.line_event)

    def split_long_message(self, text: str, max_length: int = None) -> list:
        """長文メッセージを指定文字数で分割する
        
        Args:
            text: 分割するテキスト
            max_length: 1メッセージあたりの最大文字数（デフォルト: MAX_MESSAGE_LENGTH）
            
        Returns:
            分割されたテキストのリスト
        """
        if max_length is None:
            max_length = self.MAX_MESSAGE_LENGTH
            
        if len(text) <= max_length:
            return [text]
        
        messages = []
        lines = text.split('\n')
        current_message = ""
        
        for line in lines:
            # 1行が最大長を超える場合は強制的に分割
            if len(line) > max_length:
                if current_message:
                    messages.append(current_message)
                    current_message = ""
                
                # 長い行を分割
                for i in range(0, len(line), max_length):
                    chunk = line[i:i + max_length]
                    messages.append(chunk)
            # 現在のメッセージに行を追加できる場合
            elif len(current_message) + len(line) + 1 <= max_length:
                if current_message:
                    current_message += "\n" + line
                else:
                    current_message = line
            # 追加できない場合は現在のメッセージを確定して新しいメッセージを開始
            else:
                if current_message:
                    messages.append(current_message)
                current_message = line
        
        # 残りのメッセージを追加
        if current_message:
            messages.append(current_message)
        
        return messages

    def reply_message(self, message):
        self.line_bot_api.reply_message(
            self.line_event.reply_token, message)
    
    def reply_messages(self, messages: list):
        """複数のメッセージを送信する（最初はreply、以降はpush）
        
        Args:
            messages: TextSendMessageのリスト、または文字列のリスト
        """
        if not messages:
            return
        
        # 文字列のリストの場合はTextSendMessageに変換
        if isinstance(messages[0], str):
            messages = [TextSendMessage(text=msg) for msg in messages]
        
        # 最初のメッセージはreplyで送信
        self.line_bot_api.reply_message(
            self.line_event.reply_token, messages[0])
        
        # 2つ目以降のメッセージはpushで送信
        if len(messages) > 1:
            channel_id = self.line_event.source.sender_id if hasattr(self.line_event.source, 'sender_id') else (
                self.line_event.source.group_id if hasattr(self.line_event.source, 'group_id') else 
                self.line_event.source.user_id
            )
            for msg in messages[1:]:
                self.line_bot_api.push_message(channel_id, msg)
