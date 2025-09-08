import os
import hashlib
import hmac
import base64



# Flask用: LINE署名検証関数
def verify_line_signature(request):
    x_line_signature = request.headers.get('X-Line-Signature')
    if x_line_signature is None:
        return False
    body = request.get_data(as_text=True)
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
    hash = hmac.new(channel_secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode()
    # 署名比較
    return signature == x_line_signature
