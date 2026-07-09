from flask import Flask, request, abort

from linebot.v3.webhook import (
    WebhookHandler
)

from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from line_handler import handle_event

from config import (
    LINE_CHANNEL_SECRET
)


app = Flask(__name__)


handler = WebhookHandler(
    LINE_CHANNEL_SECRET
)


@handler.add(
    MessageEvent,
    message=TextMessageContent
)
def message_event(event):

    handle_event(event)



@app.route("/")
def home():

    return "LINE Reminder Bot Running"



@app.route("/callback", methods=["POST"])
def callback():

    signature = request.headers.get(
        "X-Line-Signature"
    )

    body = request.get_data(
        as_text=True
    )


    try:

        handler.handle(
            body,
            signature
        )


    except InvalidSignatureError:

        abort(400)



    return "OK"



@app.route("/send-report")
def send_report():

    from scheduler import daily_report

    result = daily_report()

    return result



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
