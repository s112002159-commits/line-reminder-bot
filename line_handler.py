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


from commands import process_command





def handle_event(event):


    text = event.message.text


    reply = process_command(text)



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
