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
from ratelimit.decorators import ratelimit
from .movietaker.movie_handler import rank_insert

from apps.line_bot.message_manage.richmenu import pushmenu

#api
from apps.line_bot.models import TheaterModel,TheaterSerializer
from apps.line_bot.models import ControllerModel,ControllerSerializer
from apps.line_bot.models import RankModel,RankSerializer
from apps.line_bot.models import MovieModel,MovieSerializer



#==================================================================================================================

@csrf_exempt
@ratelimit(key='ip', rate='10/1m',block=True,method="POST")
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        json_store = json.dumps(body) # == <class 'str'>
        decoded = json.loads(json_store) # == <class 'str'>
        decoded = json.loads(decoded) # == <class 'dict'>
        logLength = len(decoded["events"])
    for i in range(logLength):
        if decoded["events"][i]["type"] not in ["message", "join", "leave",'follow','postback']:
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
    #==== push  rich menu to user =====================
    userid = decoded["events"][0]['source']['userId']
    # firsttest()
    pushmenu(userid)
    # ==== reply user of Line with WebhookHandler.handler.handle() =================


    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        return HttpResponseForbidden()
    return HttpResponse()


def deleteAll(request):
    
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    ScheduleModel.objects.filter(movie_date__lt=yesterday).all().delete()

    return HttpResponse('I am killer')

def rank_daily(request):
    today = date.today().strftime('%Y-%m-%d')
    rank_date_check = (RankModel.objects.filter(rank_date=today).all())
    if len(rank_date_check) == 0:
        rank_insert()
    return HttpResponse('Rank Daily')






#### use
# api

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import MultipleObjectsReturned

class RankViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = RankModel.objects.all()
        serializer = RankSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def id(self, request,pk):
        print(pk)
        movie_id = pk
        queryset = RankModel.objects.all()
        try:
            queryset = get_object_or_404(queryset, movie_id=str(movie_id))
        except MultipleObjectsReturned:
            queryset =  RankModel.objects.filter(movie_id=str(movie_id)).all()
        serializer = RankSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def date(self, request,pk):
        rank_date = pk
        queryset = RankModel.objects.all()
        try:
            queryset = get_object_or_404(queryset,rank_date=str(rank_date))
        except MultipleObjectsReturned:
            queryset =  RankModel.objects.filter(rank_date=str(rank_date)).all().order_by("rank")
        serializer = RankSerializer(queryset, many=True)
        return Response(serializer.data)    
    


class ControllerViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = ControllerModel.objects.all()
        serializer = ControllerSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def id(self, request,pk):
        order = int(pk)
        queryset = ControllerModel.objects.all()[order-1]
        serializer = ControllerSerializer(queryset)
        return Response(serializer.data)

class MovieViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = MovieModel.objects.all()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    # @action(methods=['GET'], detail=True)
    # def id(self, request,pk):
    #     order = int(pk)
    #     queryset = ControllerModel.objects.all()[order-1]
    #     serializer = ControllerSerializer(queryset)
    #     return Response(serializer.data)

#api
# class TheaterViewSet(viewsets.ModelViewSet):
#     queryset = TheaterModel.objects.all()
#     serializer_class = TheaterSerializer

# class ControllerViewSet(viewsets.ModelViewSet):
#     queryset = ControllerModel.objects.all()
#     serializer_class = ControllerSerializer