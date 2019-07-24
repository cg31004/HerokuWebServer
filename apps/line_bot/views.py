# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    TextSendMessage, # reply user
    # 下列為用戶發送給 Line 訊息
    MessageEvent, # 聽取 message 事件
    TextMessage, # 聽取用戶輸入訊息
    PostbackEvent, # 聽取 Postback 事件
    ImageMessage,
)
from .message_manage.main_handle import handler
import json
from apps.line_bot.models import ControllerModel,ScheduleModel
from django.db import IntegrityError
from datetime import date, datetime, timedelta,time
# 這邊是Linebot的授權TOKEN(等等註冊LineDeveloper帳號會取得)，我們為DEMO方便暫時存在settings裡面存取，實際上使用的時候記得設成環境變數，不要公開在程式碼裡喔！
# line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
# parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


 

#==================================================================================================================
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        json_store = json.dumps(body) # == <class 'str'>
        decoded = json.loads(json_store) # == <class 'str'>
        decoded = json.loads(decoded) # == <class 'dict'>
        logLength = len(decoded["events"])
    for i in range(logLength):
        if decoded["events"][i]["type"] not in ["message", "join", "leave",'follow']:
            # no record 'MESSAGE', 'JOIN' & 'LEAVE, they are garbage.
            continue

        try:
            ControllerModel.objects.create(
                line_id = decoded["events"][i]['source']["userId"],
                mod = 0,
                movie_id = None,
                date = None,
                control = None,
            )
            # LineModel.objects.all().delete()
        except IntegrityError as e:
        ###   帳號已經創立
            continue
        except Exception as e:
            print(e) 

    # ==== reply user of Line with WebhookHandler.handler.handle() =================

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        return HttpResponseForbidden()
    return HttpResponse()
