# -*- coding: utf-8 -*-
from pathlib import Path
import os
from dotenv import load_dotenv

from pymongo import bulk
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne, DeleteOne
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from config import products, sheet_json, sheet_url
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

env_path = Path('./.env')
load_dotenv(dotenv_path=env_path)

# google spread sheet setting

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
json_file_name = sheet_json
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = sheet_url
# 스프레스시트 문서 가져오기
API_NAME = "sheets"
API_VERSION = "V4"
doc = gc.open_by_url(spreadsheet_url)
service=discovery.build(API_NAME,API_VERSION,credentials=credentials)
sheet=service.spreadsheets()
# 시트 선택하기

sheet.values().clear(
    spreadsheetId=os.getenv('SPREADSHEET_ID'),
    range=os.getenv('SPREADSHEET_NAME')+"A2:F",
).execute()

worksheet = doc.worksheet(os.getenv('SPREADSHEET_NAME'))

# scrapping collection에서 데이터 가져와서 당일 및 최근 3일 데이터 google sheet에 넣어주기
total_result=products.aggregate([{ '$match': { 'city':{'$regex': '서울특별시.*' }} },{'$group':{"_id": 
{"city":"$city","cate":"$cate"}, "mongo_ids": {"$addToSet": "$_id"},'count': {'$sum': 1}}}])   
today=str(date.today())
three_days_ago=str(date.today()-timedelta(days=3))
_list_dep_1=[]
count=0
for i in total_result:
    count +=1
    _list_dep_2=[]
    gyeonggi_data=i['_id']
    city_name=gyeonggi_data['city']
    cate_name=gyeonggi_data['cate']
    _list_dep_2.append(city_name)
    _list_dep_2.append(cate_name)
    _list_dep_2.append(i['count'])
    today_count=products.count_documents({'$and':[{'city':city_name},{'cate':cate_name },{'created_date':{'$gte': today}}]})
    three_days_count=products.count_documents({'$and':[{'city':city_name},{'cate':cate_name },{'created_date':{'$gte': three_days_ago}}]})
    _list_dep_2.append(today_count)
    _list_dep_2.append(three_days_count)
    _list_dep_1.append(_list_dep_2)

worksheet.update('B2',_list_dep_1)
