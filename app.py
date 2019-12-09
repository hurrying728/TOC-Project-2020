import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_button_message

load_dotenv()


machine = TocMachine(
    states=["user", "start", "before_register", "after_register",
            "use_router", "not_use_router", "already_register", "not_register", "check_wifi", 
            "check_dns", "occupied", "reply", "change", "call", "find_another", "final"],
    transitions=[
        {
            "trigger": "advance",
            "source": ["user", "start", "before_register", "after_register",
                       "use_router", "not_use_router", "already_register", "not_register", "check_wifi", 
                       "check_dns", "occupied", "change", "call", "find_another", "final"],
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "before_register",
            "conditions": "is_going_to_before_register",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "after_register",
            "conditions": "is_going_to_after_register",
        },
        {
            "trigger": "advance",
            "source": "before_register",
            "dest": "use_router",
            "conditions": "is_going_to_use_router",
        },
        {
            "trigger": "advance",
            "source": "before_register",
            "dest": "not_use_router",
            "conditions": "is_going_to_not_use_router",
        },
        {
            "trigger": "advance",
            "source": "after_register",
            "dest": "already_register",
            "conditions": "is_going_to_already_register",
        },
        {
            "trigger": "advance",
            "source": ["after_register", "find_another"],
            "dest": "not_register",
            "conditions": "is_going_to_not_register",
        },
        {
            "trigger": "advance",
            "source": "after_register",
            "dest": "occupied",
            "conditions": "is_going_to_occupied",
        },
        {
            "trigger": "advance",
            "source": ["occupied", "find_another"],
            "dest": "reply",
            "conditions": "is_going_to_reply",
        },
        {
            "trigger": "advance",
            "source": "reply",
            "dest": "final",
            "conditions": "is_going_to_wait",
        },
        {
            "trigger": "advance",
            "source": "use_router",
            "dest": "call",
            "conditions": "is_going_to_call",
        },
        {
            "trigger": "advance",
            "source": ["not_use_router", "already_register"],
            "dest": "change",
            "conditions": "is_going_to_change",
        },
        {
            "trigger": "advance",
            "source": "not_register",
            "dest": "check_wifi",
            "conditions": "is_going_to_check_wifi",
        },
        {
            "trigger": "advance",
            "source": "check_wifi",
            "dest": "check_dns",
            "conditions": "is_going_to_check_dns",
        },
        {
            "trigger": "advance",
            "source": ["not_use_router", "already_register", "check_dns"],
            "dest": "call",
            "conditions": "is_going_to_call",
        },
        {
            "trigger": "advance",
            "source": "occupied",
            "dest": "find_another",
            "conditions": "is_going_to_find_another",
        },
        {
            "trigger": "advance",
            "source": ["use_router", "not_register", "check_wifi", "check_dns", 
                       "change", "call", "find_another"],
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
machine_list = []
user_id_list = []

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

        user_id = event.source.user_id
        try:
            user_machine = machine_list[user_id_list.index(user_id)]
        except ValueError:
            user_id_list.append(user_id)
            machine_list.append(machine)
            user_machine = machine_list[user_id_list.index(user_id)]

        print(f"\nFSM STATE: {user_machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = user_machine.advance(event)
        if response == False and user_machine.state == "user":
            text = "您好！\n歡迎使用宿網小幫手，請輸入\"開始使用\"以啟用服務，謝謝！"
            send_text_message(event.reply_token, text)
        elif response == False:
            send_text_message(event.reply_token, "輸入錯誤或閒置過久！\n請點選上方按鈕或輸入\"開始使用\"以重新啟用服務，謝謝！")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
