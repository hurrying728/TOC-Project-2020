from transitions.extensions import GraphMachine
from linebot.models import *

from utils import send_text_message
from utils import send_button_message

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text == "使用分享器"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text == "無使用分享器"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        text = ["尚未開放註冊宿網","請選擇連接宿網之方式"] 
        buttons = ["使用分享器", "無使用分享器"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state1(self, event):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state3")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")

    def on_enter_state4(self, event):
        print("I'm entering state4")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state4")
        self.go_back()

    def on_exit_state4(self):
        print("Leaving state4")
