from transitions.extensions import GraphMachine
from linebot.models import *

from utils import send_text_message
from utils import send_button_message

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text == "尚未開始註冊宿網"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text == "已開始註冊宿網"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text == "使用分享器"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text == "無使用分享器"

    def is_going_to_state5(self, event):
        text = event.message.text
        return text == "已註冊"

    def is_going_to_state6(self, event):
        text = event.message.text
        return text == "未註冊" or text == "已更換至未註冊網孔"

    def is_going_to_state6a(self, event):
        text = event.message.text
        return text == "仍無法連線"

    def is_going_to_state7(self, event):
        text = event.message.text
        return text == "網孔已被註冊"

    def is_going_to_state8(self, event):
        text = event.message.text
        return text == "紅色叉叉"

    def is_going_to_state9(self, event):
        text = event.message.text
        return text == "黃色驚嘆號" or text == "仍無法連線" or text == "欲與室友交換網孔"

    def is_going_to_state10(self, event):
        text = event.message.text
        return text == "網孔已被註冊"

    def is_going_to_final(self, event):
        text = event.message.text
        return text == "我知道了" or text == "連線成功"

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

        text = ["已開始註冊宿網", "請選擇註冊情況"]
        buttons = ["已註冊", "未註冊", "網孔已被註冊"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state2(self, event):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

        text = ["請確認分享器設定如下:", 
                "1. DHCP(自動取得IP&DNS)\n2. Router mode(通常是預設值)"]
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state3(self, event):
        print("Leaving state3")

    def on_enter_state4(self, event):
        print("I'm entering state4")

        text = ["無使用分享器", "請確認右下角網路連接狀態顯示何種圖示"]
        buttons = ["紅色叉叉", "黃色驚嘆號"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state4(self, event):
        print("Leaving state4")

    def on_enter_state5(self, event):
        print("I'm entering state5")

        text = ["已註冊宿網","請確認右下角網路連接狀態顯示何種圖示"] 
        buttons = ["紅色叉叉", "黃色驚嘆號"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state5(self, event):
        print("Leaving state5")

    def on_enter_state6(self, event):
        print("I'm entering state6")

        text = ["尚未註冊",
                "請直接使用學校宿網連線進入宿網管理系統，\n並確認無連上個人行動熱點等wifi"] 
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state5(self, event):
        print("Leaving state5")

    def on_enter_state6a(self, event):
        print("I'm entering state6a")

        text = ["尚未註冊",
                "請輸入網址http://dorm.cc.ncku.edu.tw/進入宿網管理系統進行註冊\n注意：開頭是http沒有s！"]
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state6a(self, event):
        print("Leaving state6a")

    def on_enter_state7(self, event):
        print("I'm entering state7")

        text = ["網孔已被註冊","請先確認是否為室友註冊"] 
        buttons = ["是，此網孔已被室友先行註冊", "否，室友皆無註冊過此網孔"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state7(self, event):
        print("Leaving state7")

    def on_enter_state8(self, event):
        print("I'm entering state8")

        text = ["網路連接狀態顯示紅色叉叉","請更換轉接頭或網路線測試"] 
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state8(self, event):
        print("Leaving state8")

    def on_enter_state9(self, event):
        print("I'm entering state9")

        text = ["轉由專人服務", "請致電計網中心分機61010詢問，謝謝！"]
        buttons = ["我知道了"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state9(self, event):
        print("Leaving state9")

    def on_enter_state10(self, event):
        print("I'm entering state10")

        text = ["已被室友註冊","請更換至其他尚未被註冊之網孔進行註冊"] 
        buttons = ["已更換至未註冊網孔", "欲與室友交換網孔"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_state10(self, event):
        print("Leaving state10")

    def on_enter_final(self, event):
        print("I'm entering final")

        reply_token = event.reply_token
        send_text_message(reply_token, "感謝您的使用！\n若有其他疑問，請致電計網中心分機61010詢問\n重新使用請輸入\"開始使用\"") 
        self.go_back()

    def on_exit_final(self):
        print("Leaving final")
