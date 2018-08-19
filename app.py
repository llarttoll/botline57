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

line_bot_api = LineBotApi('5l5X/eBThowPyjGB4q2dOtMw8a5q8ov6xi49fO56/9EBa3bhaN63jTq+qNnIgYirIaULalh+MkBFFLKSbZ0Y+TgxqaXQKOVajJx7U4UmFI1LF8YDEmXu0XerH4vEh0uFmHU5130sXEOyAaoKE6IorAdB04t89/1O/w1cDnyilFU=')
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
    elif(message == 'channel2 on'):
        anto.pub('myChannel2', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On channel2"))
    elif(message == 'channel2 off'):
        anto.pub('myChannel2', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel2"))
    
if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)
