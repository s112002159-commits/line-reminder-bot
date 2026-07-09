from linebot.models import TextMessage,TextSendMessage
from commands import command
from storage import load,save

def handle_event(event):
 if isinstance(event.message,TextMessage):
  txt=event.message.text
  r=command(txt)
  if r: event.reply_token and event.reply(TextSendMessage(r))
