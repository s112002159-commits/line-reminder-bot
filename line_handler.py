from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)

from commands import process_command
from storage import save_user, save_group


def handle_event(event):
    """
    LINE事件處理中心
    """

    # 記錄使用者
    if hasattr(event.source, "user_id"):
        save_user(
            event.source.user_id
        )


    # 記錄群組
    if hasattr(event.source, "group_id"):
        save_group(
            event.source.group_id
        )


    # 文字訊息處理
    if event.message.type == "text":

        text = event.message.text

        reply = process_command(text)


        return reply


    return "目前只支援文字指令"
