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

mind_quest = {1:"お気に入りの花が枯れかかっているときにとる行動は？\n1.ハサミでばっさり切る\n2.即効ゴミ箱行き\n3.ドライフラワーにして二度楽しむ\n4.水をあげる"}

mind_answer = {1:"1 を選んだあなたは感情に任せてとんでもない行動を取ってしまいがち", 2:"2 を選んだあなたは後腐れせずにさっぱり別れられるタイプ",
               3:"3 を選んだあなたは恋の終わりを穏やかに受け入れるタイプ", 4:"4 を選んだあなた＝諦められず、必死に相手を引き止めるタイプ"}

mind_message = {1:"これで恋の終わりにあなたが取る行動がわかっちゃうよ\n\n"}

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
    mind_num = []
    if event.source.user_id not in sessions:
        sessions[event.source.user_id] = 0
    if sessions[event.source.user_id] == 0:
        if event.message.text == "じゃんけん":
            message = "「グー」か「チョキ」か「パー」で入力してね、最初はグーじゃんけん...."
            sessions[event.source.user_id] = 1
        elif event.message.text == "心理テスト":
            i = ramdom.randint(1,2)
            mind_num[0] = i
            message = mind_quest[mind_num[0]]
            sessions[event.source.user_id] = 2
        elif event.message.text in word_dic:
            message = word_dic[event.message.text]
        else:
            message = "「好きな〜は？」みたいに話かけてみてね(例:本,曲,食べ物,etc)\n「じゃんけん」でじゃんけん、「心理テスト」で心理テストができちゃうよ"
    elif sessions[event.source.user_id] == 1:
        result = hands_to_int(event.message.text)
        if result[0] == True:
           sessions[event.source.user_id] = 0
        message = result[1]
    elif sessions[event.source.user_id] == 2:   
        if int(event.message.text) <= 4  :
            message = mind_message[mind_num[0]] + mind_answer[int(event.message.text)]
            sessions[event.source.user_id] = 0
        else:
            message = "１〜４の数字で入力してね"
   
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
