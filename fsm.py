from transitions.extensions import GraphMachine
from linebot.models import *
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

from utils import send_text_message
from utils import send_button_message

GDriveJSON = 'NckudormhelperReply-3d48be03dd5a.json'
GSpreadSheet = 'NCKUdormHelper_reply'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        return text == "開始使用"

    def is_going_to_before_register(self, event):
        text = event.message.text
        return text == "尚未開始註冊宿網"

    def is_going_to_after_register(self, event):
        text = event.message.text
        return text == "已開始註冊宿網"

    def is_going_to_use_router(self, event):
        text = event.message.text
        return text == "使用分享器"

    def is_going_to_not_use_router(self, event):
        text = event.message.text
        return text == "無使用分享器"

    def is_going_to_already_register(self, event):
        text = event.message.text
        return text == "已註冊"

    def is_going_to_not_register(self, event):
        text = event.message.text
        return text == "未註冊" or text == "已更換至未註冊網孔"

    def is_going_to_check_wifi(self, event):
        text = event.message.text
        return text == "仍無法連線"

    def is_going_to_check_dns(self, event):
        text = event.message.text
        return text == "仍無法連線"

    def is_going_to_occupied(self, event):
        text = event.message.text
        return text == "網孔已被註冊"

    def is_going_to_reply(self, event):
        text = event.message.text
        return text == "否"

    def is_going_to_wait(self, event):
        text = event.message.text

        global GDriveJSON
        global GSpreadSheet
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).sheet1
        worksheet.append_row((datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), text))
        return True

    def is_going_to_change(self, event):
        text = event.message.text
        return text == "紅色叉叉"

    def is_going_to_call(self, event):
        text = event.message.text
        return text == "黃色驚嘆號" or text == "仍無法連線" or text == "欲與室友交換網孔"

    def is_going_to_find_another(self, event):
        text = event.message.text
        return text == "是"

    def is_going_to_final(self, event):
        text = event.message.text
        return text == "我知道了" or text == "連線成功"

    def on_enter_start(self, event):
        print("I'm entering start")

        text = ["請選擇是否已開始註冊宿網", "是否已開始註冊可於計網中心首頁公告確認"] 
        buttons = ["尚未開始註冊宿網", "已開始註冊宿網"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_start(self, event):
        print("Leaving start")

    def on_enter_before_register(self, event):
        print("I'm entering before_register")

        text = ["尚未開放註冊宿網","請選擇連接宿網之方式"] 
        buttons = ["使用分享器", "無使用分享器"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_before_register(self, event):
        print("Leaving before_register")

    def on_enter_after_register(self, event):
        print("I'm entering after_register")

        text = ["已開始註冊宿網", "請選擇註冊情況"]
        buttons = ["已註冊", "未註冊", "網孔已被註冊"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_after_register(self, event):
        print("Leaving after_register")

    def on_enter_use_router(self, event):
        print("I'm entering use_router")

        text = ["請確認分享器設定如下:", 
                "1. DHCP(自動取得IP&DNS)\n2. Router mode(通常是預設值)"]
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_use_router(self, event):
        print("Leaving use_router")

    def on_enter_not_use_router(self, event):
        print("I'm entering not_use_router")

        text = ["無使用分享器", "請確認右下角網路連接狀態顯示何種圖示"]
        buttons = ["紅色叉叉", "黃色驚嘆號"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_not_use_router(self, event):
        print("Leaving not_use_router")

    def on_enter_already_register(self, event):
        print("I'm entering already_register")

        text = ["已註冊宿網","請確認右下角網路連接狀態顯示何種圖示"] 
        buttons = ["紅色叉叉", "黃色驚嘆號"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_already_register(self, event):
        print("Leaving already_register")

    def on_enter_not_register(self, event):
        print("I'm entering not_register")

        text = ["尚未註冊",
                "請輸入網址http://dorm.cc.ncku.edu.tw/進行註冊\n注意：開頭是http沒有s！"] 
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_already_register(self, event):
        print("Leaving already_register")

    def on_enter_check_wifi(self, event):
        print("I'm entering check_wifi")

        text = ["尚未註冊",
                "請直接使用學校宿網連線進入宿網管理系統，並確認無連上個人行動熱點等wifi"]
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_check_wifi(self, event):
        print("Leaving check_wifi")

    def on_enter_check_dns(self, event):
        print("I'm entering check_dns")

        text = ["設定確認",
                "1. DNS&IP自動取得\n2. 關閉proxy及vpn"]
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_check_dns(self, event):
        print("Leaving check_dns")

    def on_enter_occupied(self, event):
        print("I'm entering occupied")

        text = ["網孔已被註冊","請先確認是否為室友註冊"] 
        buttons = ["是", "否"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_occupied(self, event):
        print("Leaving occupied")

    def on_enter_reply(self, event):
        print("I'm entering reply")

        text = "將交由負責人處理，請複製下列格式回覆訊息：\n姓名：\n學號：\n連絡電話：\n寢室：\nIP：(若是要交換兩個ip的註冊訊息請以/隔開不同ip)\n備註：(若無請填無)" 
        reply_token = event.reply_token
        send_text_message(reply_token, text)

        global GDriveJSON
        global GSpreadSheet
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).sheet1
        worksheet.append_row((datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), event.message.text))

    def on_exit_reply(self, event):
        print("Leaving reply")

    def on_enter_change(self, event):
        print("I'm entering change")

        text = ["網路連接狀態顯示紅色叉叉","請更換轉接頭或網路線測試"] 
        buttons = ["連線成功", "仍無法連線"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_change(self, event):
        print("Leaving change")

    def on_enter_call(self, event):
        print("I'm entering call")

        text = ["轉由專人服務", "請致電計網中心(06)2757575分機61010詢問，謝謝！"]
        buttons = ["我知道了"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_call(self, event):
        print("Leaving call")

    def on_enter_find_another(self, event):
        print("I'm entering find_another")

        text = ["已被室友註冊","請更換至其他尚未被註冊之網孔進行註冊"] 
        buttons = ["已更換至未註冊網孔", "欲與室友交換網孔"]

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons)

    def on_exit_find_another(self, event):
        print("Leaving find_another")

    def on_enter_final(self, event):
        print("I'm entering final")

        reply_token = event.reply_token
        send_text_message(reply_token, "感謝您的使用！\n若有其他疑問，請致電計網中心(06)2757575分機61010詢問\n重新使用請輸入\"開始使用\"") 
        self.go_back()

    def on_exit_final(self):
        print("Leaving final")
