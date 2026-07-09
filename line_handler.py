from flask import request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from linebot.v3.exceptions import InvalidSignatureError

import re

from config import (
    LINE_CHANNEL_ACCESS_TOKEN,
    LINE_CHANNEL_SECRET
)

from storage import (
    load_data,
    save_data,
    add_user,
    add_group
)

from event_manager import (
    update_event
)

from commands import (
    help_message,
    members,
    version,
    list_events,
    status,
    clear,
    reset,
    preview
)

# =====================================
# LINE SDK
# =====================================

configuration = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)

handler = WebhookHandler(
    LINE_CHANNEL_SECRET
)

# =====================================
# Reply
# =====================================

def reply(reply_token, text):

    with ApiClient(configuration) as api_client:

        MessagingApi(api_client).reply_message(

            ReplyMessageRequest(

                reply_token=reply_token,

                messages=[

                    TextMessage(text=text)

                ]

            )

        )

# =====================================
# Callback
# =====================================

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

# =====================================
# Message Event
# =====================================

@handler.add(
    MessageEvent,
    message=TextMessageContent
)
def handle_message(event):

    text = event.message.text.strip()

    # -----------------------------
    # 自動記錄好友
    # -----------------------------

    if event.source.type == "user":

        add_user(
            event.source.user_id
        )

    # -----------------------------
    # 自動記錄群組
    # -----------------------------

    elif event.source.type == "group":

        add_group(
            event.source.group_id
        )

    data = load_data()

    user_id = ""

    if hasattr(
        event.source,
        "user_id"
    ):

        user_id = event.source.user_id
          # =====================================
    # /help /h
    # =====================================
    if text in ["/help", "/h"]:

        reply(
            event.reply_token,
            help_message()
        )

        return

    # =====================================
    # /members
    # =====================================
    if text == "/members":

        reply(
            event.reply_token,
            members()
        )

        return

    # =====================================
    # /version
    # =====================================
    if text == "/version":

        reply(
            event.reply_token,
            version()
        )

        return

    # =====================================
    # /list
    # =====================================
    if text == "/list":

        reply(
            event.reply_token,
            list_events()
        )

        return

    # =====================================
    # /status
    # =====================================
    if text == "/status":

        reply(
            event.reply_token,
            status()
        )

        return

    # =====================================
    # #測試 /測試
    # =====================================
    if text in ["#測試", "/測試"]:

        reply(
            event.reply_token,
            preview()
        )

        return

    # =====================================
    # /clear
    # =====================================
    if text == "/clear":

        reply(
            event.reply_token,
            clear(user_id)
        )

        return

    # =====================================
    # /reset
    # =====================================
    if text == "/reset":

        reply(
            event.reply_token,
            reset(user_id)
        )

        return

    # =====================================
    # 準備解析事故輸入
    # =====================================
    match = re.match(

        r"(.+?)：(.+)",

        text

    )

    if not match:

        return

    name = match.group(1).strip()

    content = match.group(2).strip()

    if name not in data["members"]:

        reply(

            event.reply_token,

            "❌ 查無此人"

        )

        return
          # =====================================
    # 更新事故事件
    # =====================================

    update_event(
        name,
        content
    )

    reply(

        event.reply_token,

        f"✅ 已更新 {name}\n\n內容：{content}"

    )

    return
