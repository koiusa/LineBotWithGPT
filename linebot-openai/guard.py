import os
import hashlib
import hmac
import base64


class authorizer:
    signature = None
    body = None

    def request(self, event):
        # 認証用のx-line-signatureヘッダー
        x_line_signature = event["headers"].get("x-line-signature")

        if x_line_signature == None:
            return False

        body = event.get("body")
        channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
        # Generate the signature using HMAC-SHA256
        hash = hmac.new(channel_secret.encode('utf-8'),
                        body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash)

        # Compare the signature from the request headers with the generated signature
        if signature != x_line_signature.encode():
            return False

        self.signature = x_line_signature
        self.body = body
        return True
