import os
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from line_handler import handle_event

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',''))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',''))

@app.route('/callback', methods=['POST'])
def callback():
    signature=request.headers.get('X-Line-Signature','')
    body=request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature',400
    return 'OK'

@app.route('/')
def index():
    return jsonify({'status':'LINE Bot running'})

handler.add(MessageEvent=None, message=None)(handle_event)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.getenv('PORT',5000)))
