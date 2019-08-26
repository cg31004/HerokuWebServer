import requests
import json
from linebot import (
    LineBotApi, WebhookHandler
)

from django.conf import settings
import os

######    push pic
def pushmenu(userid):
    line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
    #######   start menu
        headers = {"Authorization":"Bearer {}".format(settings.LINE_CHANNEL_ACCESS_TOKEN),"Content-Type":"application/json"}

        # req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(rich_menu.rich_menu_id),
                            # headers=headers)
        req = requests.request('POST', 'https://api.line.me/v2/bot/user/{}/richmenu/{}'.format(userid,rich_menu.rich_menu_id), 
                            headers=headers)

if __name__ == '__main__':
    ######    delete 
    line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

    ######   create a new menu

    headers = {"Authorization":"Bearer {}".format(settings.LINE_CHANNEL_ACCESS_TOKEN),"Content-Type":"application/json"}

    body = {
        "size": {
        "width": 2500,
        "height": 843
        },
        "selected": False,
        "name": "richmenu-1",
        "chatBarText": "Menu",
        "areas": [
        {
            "bounds": {
            "x": 0,
            "y": 0,
            "width": 1250,
            "height": 578
            },
            "action": {
            "type":"postback",
            "data":"RichMenu-1"
            }
        },
        {
            "bounds": {
            "x": 1250,
            "y": 0,
            "width": 1250,
            "height": 578
            },
            "action": {
            "type":"postback",
            "data":"RichMenu-2"
            }
        },
        {
            "bounds": {
            "x": 0,
            "y": 579,
            "width": 2500,
            "height": 265
            },
            "action": {
            "type":"postback",
            "data":"BACK-back"
            }
        }
    ]
    }

    req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                        headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req)
    print(req.text)

    ######   print all list
    line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

    rich_menu_list = line_bot_api.get_rich_menu_list()

    print(os.path.abspath(os.path.dirname('__file__')))
    for rich_menu in rich_menu_list:
        print(rich_menu.rich_menu_id)
        
        with open("picture3.jpg", 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu.rich_menu_id, "image/jpeg", f)