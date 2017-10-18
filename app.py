import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('dWflNwrW82xDOgRF0sas8bPd22Hg3wQF+whS9tcR5bDgrtdWzW64ChNqTn5zSX6jUvoK330d/2wE67MRzO6+fej3dNk5+TNDhCzIL+z5WWsjNfwfZHej4mYJzNoLvCyLCXCcUDx8uHRiK3NRAd0j6gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b93be661ac48c8d108784bf03a21219d')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
