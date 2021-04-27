# coding=utf8
from flask import Flask, request, abort
import json
import requests
app = Flask(__name__)


@app.route("/webhook", methods=['GET','POST'])
def webhook():
    if request.method == "GET":
        VERIFY_TOKEN = "輸入自己的驗證Token"
        print(request)
        mode = request.args.get('hub.mode')
        sendToken = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == "subscribe" and sendToken == VERIFY_TOKEN:
            return challenge
        else:
            return "error"
    else:
        try:
            message_entries = json.loads(request.data.decode('utf8'))['entry']
            for entry in message_entries:
                messagings = entry['messaging']
                for message in messagings:
                    sender = message['sender']['id']
                    if "message" in message:
                        text = message['message']['text']
                        result = send_fb_message(sender, text)
                print("Good2")
        except Exception as e:
            print(str(e))
        return "Success"
    
def send_fb_message(to, message):
    post_message_url = 'https://graph.facebook.com/v10.0/me/messages?access_token={token}'.format(token="這裡要放自己的Token123")
    response_message = json.dumps({"messaging_type":"RESPONSE",
                                    "recipient":{"id": to}, 
                                   "message":{"text":message}})
    req = requests.post(post_message_url, 
                        headers={"Content-Type": "application/json"}, 
                        data=response_message)
    return req.text

@app.route("/", methods=['GET'])
def index():
    return "已經成功開啟APP!!!!"

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = TextSendMessage(text=event.message.text)
#     line_bot_api.reply_message(
#         event.reply_token,
#         message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
