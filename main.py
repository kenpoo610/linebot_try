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

mind_quest = {1:"お気に入りの花が枯れかかっているときにとる行動は？\n1.ハサミでばっさり切る\n2.即効ゴミ箱行き\n3.ドライフラワーにして二度楽しむ\n4.水をあげる",
 2:"あなたは殺人現場に出くわしてしまいました。犯人と遭遇し目が合った、そんなとき起きた出来事とは？\n1.警官が駆け付けた\n2.火事が起きた\n3.通行人が現れた\n4.犯人が逃げ出した",
3:"あなたが雨の中、道を歩いていると、段ボールに入っている子猫を見つけました。その子猫は、どんな様子ですか？\n1.元気に鳴いている\n2.体調が悪そうにしている\n3.毛づくろいをしている\n4.こちらをじっと見つめている"}

mind_answer = {1:{1:"1 を選んだあなたは感情に任せてとんでもない行動を取ってしまいがち", 2:"2 を選んだあなたは後腐れせずにさっぱり別れられるタイプ",3:"3 を選んだあなたは恋の終わりを穏やかに受け入れるタイプ", 4:"4 を選んだあなた＝諦められず、必死に相手を引き止めるタイプ"}, 
2:{1:"1の「警官が駆け付けた」を選んだあなたの不幸引き寄せ度は0％\n稀代の強運の持ち主であり悪いものを寄せ付けることはほとんどなさそう", 2:"2の「火事が起きた」を選んだあなたの不幸引き寄せ度は70％\n更に火事が起きるというダブルパンチを想像したあなたは悪いことを招きやすい不幸体質を持っているようだね", 3:"3の「通行人が現れた」を選んだあなたの不幸引き寄せ度は50％\n表れたのは頼りない一般市民を想像してしまったあなたは定期的に不幸を招き寄せているかもしれないね", 4:"4の「犯人が逃げ出した」を選んだあなたの不幸引き寄せ度は20％\n我が道を行く芯の通った性格のあなたは不幸とは無縁の体質のようだね"},
3:{1:"あなたは乗せられて、気づけばハマっているタイプ\nあの人にも、いい所あるし...という言い訳もしてしまいがち", 2:"あなたは思わず母性本能、父性本能が働いてしまうタイプ\n熱しやすいですが、冷めやすいという特徴もあるよ", 3:"あなたはダメ男ダメ女に引っかかりづらいタイプ\n冷静で、客観的に見ることができるため、引っかかりづらいよ", 4:"あなたは人の良さが全面に出ていて、引っかかりやすいタイプ\n押しに弱く、頼み事を何でも聞いてしまうため、都合のいい人になりがち"}}

mind_message = {1:"これで恋の終わりにあなたが取る行動がわかっちゃうよ\n\n", 2:"あなたの不幸引き寄せ度を知ることができちゃうよ\n\n", 3:"あなたがどれほどダメ男ダメ女に引っかかりやすいかが分かっちゃうよ\n\n"}

mind_num = {}

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
        elif event.message.text == "心理テスト":
            i = random.randint(1,3)
            mind_num[event.source.user_id] = i
            message = mind_quest[mind_num[event.source.user_id]]
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
        if int(event.message.text) <= 4 and int(event.message.text) > 0:
            message = mind_message[mind_num[event.source.user_id]] + mind_answer[mind_num[event.source.user_id]][int(event.message.text)]
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
