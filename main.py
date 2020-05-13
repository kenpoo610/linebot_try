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
word_dic = {"元気？":"元気だよ、君は元気？", "暇":"話そう？", "しーくん":"出会い厨くんのことだね", 
            x+"曲"+y:"https://www.youtube.com/watch?v=bmkY2yc1K7Q", x+"食べ物"+y:"芋けんぴ", x+"飲み物"+y:"カフェオレ", 
            x+"人"+y:"豚足", x+"色"+y:"しろ", x+"お菓子"+y:"芋けんぴ", x+"季節"+y:"春", x+"本"+y:"青春ブタ野郎シリーズ",
            x+"ゲーム"+y:"グラブル", "エルフクイーン":"なんちゅうカード入れとるんじゃぁぁぁぁ！！", 
            "ほっけええええええええい！":"豚饅頭さん、私も好きですよ", "眠い":"私も眠いの", x+"物"+y:"漫画だよ",
            x+"漫画"+y:"政宗くんのリベンジ"}

sessions = {}

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
        return True, bot_hand("あいこだね","私の負け","私の勝ち")
        
    elif userhand == "チョキ":
        return True, bot_hand("私の勝ち","あいこだね","私の負け")
        
    elif userhand == "パー":
        return True, bot_hand("私の負け","私の勝ち","あいこだね")
        
    else:
        return False, "グーかチョキかパーで入力してね"
    

def main_brain(event):
    if event.source.user_id not in sessions:
        sessions[event.source.user_id] = 0
    if sessions[event.source.user_id] == 0:
        if event.message.text == "じゃんけん":
            message = "「グー」か「チョキ」か「パー」で入力してね、最初はグーじゃんけん...."
            sessions[event.source.user_id] = 1
    elif sessions[event.source.user_id] == 1:
        result = hand_to_int(event.message.text)
        if result[0] == True:
           sessions[event.source.user_id] = 0
        message = result[1]
  
    elif event in word_dic:
        message = word_dic[event.message.text]
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
    message = main_brain(event)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
