import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass
"""
def send_button_message(reply_token, text, buttons):
    act = []
    for buttons in buttons:
        act.append(
            MessageTemplateAction(
                label = buttons,
                text = buttons
            )
        )
    buttons_template = TemplateSendMessage(
        alt_text = text[0],
        template = ButtonsTemplate(
            title = text[0],
            text = text[1],
            actions = act
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, buttons_template)

    return "OK"
