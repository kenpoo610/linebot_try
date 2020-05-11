from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def bot_hand(a,b,c):
    bothand = random.randint(1,3)
    if bothand == 1:
        message_bot = "グーだよ、" + a
    elif bothand == 2:
        message_bot = "チョキだよ、" + b
    else:
        message_bot = "パーだよ、" + c
    return message_bot    

def hands_to_int(userhand):
    if userhand == "好き":
        message = "私も好きだよ"
    elif userhand == "グー":
        message = bot_hand("あいこだね","私の負け","私の勝ち")
    elif userhand == "チョキ":
        message = bot_hand("私の勝ち","あいこだね","私の負け")
    elif userhand == "パー":
        message = bot_hand("私の負け","私の勝ち","あいこだね")
    elif userhand == "ほっけええええええええい！":
        message = "豚饅頭さん、私も好きですよ
    else:
        message = "グーかチョキかパーで入力してね"
    return message    
        


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = event.message.text
    message = hands_to_int(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
