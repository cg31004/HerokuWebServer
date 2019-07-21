
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
from ..models import (
    RankModel,
    ScheduleModel,
    MovieModel,
    TheaterModel,
    ControllerModel,
)
# from apps.line_bot.models import ControllerModel

ControllerModel.objects.create(
    line_id = '123123123123',
    mod = 0,
    movie_id = None,
    date = None,
    control = None,
)