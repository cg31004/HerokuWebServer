import scrapy
from ..items import NewsItem, ContentItem
from time import sleep
from apps.news.models import NewsModel, ContentModel
import re
from django.db import IntegrityError

class newsSpider(scrapy.Spider):
    name = "scrapy_nba"

    def start_requests(self):
        for page in range(1,5):
            sleep(0.5)
            yield scrapy.Request(url = "https://nba.udn.com/nba/cate/6754/-1/newest/{}".format(page), callback = self.parse_page)


    def parse_page(self,response):
        target = response.css("div#news_list_body dl dt")
        count=0
        for tag in target:
            try:
                count+=1
                content_url = tag.css("a::attr(href)").extract_first()
                content_url = "https://nba.udn.com{}".format(content_url)
                news_id = "".join(re.compile(r'story/\d*/\d*$').search(content_url).group(0).split("/")[1:]) 
                NewsModel.objects.create(
                    title = tag.css("a h3::text").extract_first(),
                    introduction = tag.css("a p::text").extract_first(),
                    news_id = int(news_id),
                )
                yield scrapy.Request(url = content_url , callback = self.parse_content)
            except IntegrityError as e:
                ###   新聞已經匯入
                # pass
                break
        if count>0:
            print('有新的新聞')

    def parse_content(self,response):
        contentitem = ContentItem()
        all_span = response.css("div#story_body_content span p::text")
        news_id = "".join(re.compile(r'story/\d*/\d*$').search(response.request.url).group(0).split("/")[1:])
        content_text = ''
        for sig in all_span:
            content_text += sig.extract()
        ContentModel.objects.create(
            content_id = int(news_id),
            content_title = response.css("div#story_body_content h1::text").extract_first(),
            content_url = response.request.url,
            content_text= content_text,
            news_date = response.css("div#shareBar div span::text").extract_first(),
        )




