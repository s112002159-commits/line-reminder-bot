from flask import Flask, request, abort

from linebot.v3.webhook import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from config import (
    LINE_CHANNEL_SECRET,
    PORT
)

from scheduler import (
    send_daily_report
)

from line_handler import (
    handle_text_message
)

app = Flask(__name__)

parser = WebhookParser(
    LINE_CHANNEL_SECRET
)

# ===========================
# 首頁
# ===========================
@app.route("/")
def home():

    return "LINE Reminder Bot Running", 200


# ===========================
# Wake
# ===========================
@app.route("/wake")
def wake():

    return "awake", 200


# ===========================
# Cron Trigger
# ===========================
@app.route("/trigger")
def trigger():

    try:

        send_daily_report()

        return "success", 200

    except Exception as e:

        print(e)

        return str(e), 500


# ===========================
# Webhook
# ===========================
@app.route("/callback", methods=["POST"])
def callback():

    signature = request.headers.get(
        "X-Line-Signature"
    )

    body = request.get_data(
        as_text=True
    )

    try:

        events = parser.parse(
            body,
            signature
        )

    except InvalidSignatureError:

        abort(400)

    except Exception as e:

        print(e)

        abort(500)

    for event in events:

        if isinstance(
            event,
            MessageEvent
        ):

            if isinstance(
                event.message,
                TextMessageContent
            ):

                handle_text_message(
                    event
                )

    return "OK"

# ===========================
# 404
# ===========================
@app.errorhandler(404)
def not_found(error):

    return (
        "404 Not Found",
        404
    )


# ===========================
# 500
# ===========================
@app.errorhandler(500)
def server_error(error):

    return (
        "500 Internal Server Error",
        500
    )


# ===========================
# Render Health Check
# ===========================
@app.route("/health")
def health():

    return {
        "status": "ok",
        "service": "LINE Reminder Bot"
    }, 200


# ===========================
# 啟動
# ===========================
if __name__ == "__main__":

    print("=" * 50)
    print(" LINE Reminder Bot")
    print("=" * 50)
    print("Server Starting...")
    print(f"PORT : {PORT}")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False
    )
