from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

from config import (
    LINE_CHANNEL_ACCESS_TOKEN
)


def handle_event(event):


    text = event.message.text


    reply = "收到：" + text



    configuration = Configuration(
        access_token=
        LINE_CHANNEL_ACCESS_TOKEN
    )


    with ApiClient(configuration) as api_client:

        api = MessagingApi(api_client)


        api.reply_message(
            ReplyMessageRequest(

                reply_token=
                event.reply_token,


                messages=[
                    TextMessage(
                        text=reply
                    )
                ]

            )
        )
