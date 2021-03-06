from flask import Flask, request
import antolib
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi('Z1m8F5v+DDV1tZQO51S1OmqP4alRw4E95cbkyoT5p+9uUoVc2hf6+izT/scpH3LnIaULalh+MkBFFLKSbZ0Y+TgxqaXQKOVajJx7U4UmFI0mNzwirHrWSooIcNY5wuyG3V/fiiQqHqaKDEQZou6eQgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ca74af7f392af33d8cd5c25d8929e37f')

app = Flask(__name__)

# username of anto.io account
user = 'llarttoll'
# key of permission, generated on control panel anto.io
key = 'OlduDgwj3YaUhoMT90FrWYUcYINHSXF0yq8PIzck'
# your default thing.
thing = 'NodeMCU'

anto = antolib.Anto(user, key, thing)


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
    # message = event.message.text
    # line_bot_api.reply_message(
    #    event.reply_token,
    #     TextSendMessage(text="Turn Off channel1"))
message = event.message.text
    if(message == 'เปิดไฟ'):
        anto.pub('LED1', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ไฟเปิดแล้ว"))
    elif(message == 'ปิดไฟ'):
        anto.pub('LED1', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ไฟปิดแล้ว"))
    elif(message == 'test'):
        anto.pub('myChannel2', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ok sir"))
    elif(message == 'channel2 off'):
        anto.pub('myChannel2', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel2"))
    
if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)
