import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "state1", "state2","state3", "state4", "state5", "state6", "state6a", 
            "state7", "state8", "state9", "state10", "final"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "state1",
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {
            "trigger": "advance",
            "source": "state1",
            "dest": "state4",
            "conditions": "is_going_to_state4",
        },
        {
            "trigger": "advance",
            "source": "state2",
            "dest": "state5",
            "conditions": "is_going_to_state5",
        },
        {
            "trigger": "advance",
            "source": ["state2", "state10"],
            "dest": "state6",
            "conditions": "is_going_to_state6",
        },
        {
            "trigger": "advance",
            "source": "state2",
            "dest": "state7",
            "conditions": "is_going_to_state7",
        },
        {
            "trigger": "advance",
            "source": "state3",
            "dest": "state9",
            "conditions": "is_going_to_state9",
        },
        {
            "trigger": "advance",
            "source": ["state4", "state5"],
            "dest": "state8",
            "conditions": "is_going_to_state8",
        },
        {
            "trigger": "advance",
            "source": "state6",
            "dest": "state6a",
            "conditions": "is_going_to_state6a",
        },
        {
            "trigger": "advance",
            "source": ["state4", "state5", "state6a", "state7"],
            "dest": "state9",
            "conditions": "is_going_to_state9",
        },
        {
            "trigger": "advance",
            "source": "state7",
            "dest": "state10",
            "conditions": "is_going_to_state10",
        },
        {
            "trigger": "advance",
            "source": ["state3", "state6", "state6a", "state8", "state9", "state10"],
            "dest": "final",
            "conditions": "is_going_to_final",
        },
        {
            "trigger": "go_back", 
            "source": "final", 
            "dest": "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False and machine.state == "user":
            text = ["您好！",
                    "歡迎使用宿網小幫手，若要使用請點選下方按鈕，謝謝！"]
            buttons = ["開始使用"]
            send_buttons_message(event.reply_token, text, buttons)
        elif response == False:
            send_text_message(event.reply_token, "請點選上方訊息之按鈕\n或輸入\"開始使用\"以重新啟用服務，謝謝！")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
