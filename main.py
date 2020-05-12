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

x = "好きな" 
y = "は？"
word_dic = {"萌子":"好き!", "元気？":"元気だよ、君は元気？", "うんち":"汚い...", "暇":"話そう？", "しーくん":"出会い厨くんのことだね", 
            x+"曲"+y:"https://www.youtube.com/watch?v=bmkY2yc1K7Q", x+"食べ物"+y:"芋けんぴ", x+"飲み物"+y:"カフェオレ", 
            x+"人"+y:"豚足", x+"色"+y:"しろ", x+"お菓子"+y:"芋けんぴ", x+"季節"+y:"春", x+"本"+y:"政宗くんのリベンジ",
            x+"ゲーム"+y:"グラブル", "エルフクイーン":"なんちゅうカード入れとるんじゃぁぁぁぁ！！", 
            "ほっけええええええええい！":"豚饅頭さん、私も好きですよ"}
          

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
    if userhand == "グー":
        message = bot_hand("あいこだね","私の負け","私の勝ち")
    elif userhand == "チョキ":
        message = bot_hand("私の勝ち","あいこだね","私の負け")
    elif userhand == "パー":
        message = bot_hand("私の負け","私の勝ち","あいこだね")
    else:
        message = "グーかチョキかパーで入力してね"
    return message 

def main_brain(your_message):
    if your_message == "じゃんけん":
        message = "「グー」か「チョキ」か「パー」で入力してね、最初はグーじゃんけん...."
    elif your_message in word_dic:
        message = word_dic[your_message]
    else:
        message = "「好きな〜は？」みたいに話かけてみてね、じゃんけんは今はおやすみだよ(例：曲,お菓子,本,)"
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
    message = main_brain(event.message.text)
    if message == "「グー」か「チョキ」か「パー」で入力してね、最初はグーじゃんけん....":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="今はお休みなの"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
