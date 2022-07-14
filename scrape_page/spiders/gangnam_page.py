import scrapy
import pymongo
from pymongo import bulk
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne, DeleteOne
from scrape_page.filter_date import firstday_of_previous_month
from datetime import date
import datetime

from scrape_page.config import doc_product


class GangnamSpider(scrapy.Spider):
    name = 'gangnam'
    # scray 시작 시 실행되는 함수

    def start_requests(self):

        # 강남구 첫페이지 인덱스: 0
        for i in range(20, -1, -1):
            _link = 'https://www.gangnam.go.kr/board/B_000001/list.do?mid=ID05_040101&pgno={}&deptField=BDM_DEPT_ID&deptId=&keyfield=bdm_main_title&keyword='.format(
                i)
            yield scrapy.Request(url=_link, callback=self.product, meta={'ua': 'desktop', 'current_page': 1, 'dont_merge_cookies': True, 'i': i}, dont_filter=True, priority=10000)

        # 콜백
    def product(self, response):

        bulk_list = []
        trs = response.css(
            "#contents-wrap > div > div > div > div:nth-child(1) > div > table > tbody > tr")

        # for문 돌면서 각 페이지 데이터 뽑아오기
        for i in range(1, len(trs)+1):
            _dict = {}

            _link_num = response.css(
                '#contents-wrap > div > div > div > div:nth-child(1) > div > table > tbody > tr:nth-child({}) > td.align-l.tit > a ::attr(href)'.format(i)).get()[0:]
            _link_templet = 'https://www.gangnam.go.kr{}'.format(_link_num)
            _link = _link_templet

            _title = response.css(
                '#contents-wrap > div > div > div > div:nth-child(1) > div > table > tbody > tr:nth-child({}) > td.align-l.tit > a ::text'.format(i)).get().strip()
            _views = response.css(
                '#contents-wrap > div > div > div > div:nth-child(1) > div > table > tbody > tr:nth-child({}) > td.view-cnt ::text'.format(i)).get().strip()

            if ',' in _views:
                _views = _views.replace(',', '')
            _department = response.css(
                '#contents-wrap > div > div > div > div:nth-child(1) > div > table > tbody > tr:nth-child({}) > td:nth-child(3) ::text'.format(i)).get().strip()
            print(_link, _title, _views, _department)

            _category = response.css(
                '#container > div > div.title-wrap.col-xs-12 > h3::text').get().strip()

            collectdate = str(datetime.datetime.now())[0:10]

            _dict['title'] = _title
            _dict['department'] = _department
            _dict['link'] = _link
            _dict['collected_date'] = collectdate
            _dict['views'] = int(_views)  # 조회수
            _dict['city'] = '서울특별시강남구'
            _dict['category'] = _category

            bulk_list.append(UpdateOne({'$and': [{'link': _link}, {'title': _title}]}, {
                             '$set': _dict}, upsert=True))

        # pymongo bulk write
        print('=벌크리스트=>', bulk_list)
        if len(bulk_list) != 0:
            doc_product.bulk_write(bulk_list)
