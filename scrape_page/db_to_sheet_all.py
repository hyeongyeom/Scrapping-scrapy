# -*- coding: utf-8 -*-
from pathlib import Path
import os
from dotenv import load_dotenv
from pymongo import bulk, UpdateOne
from config import products, cities_info, sheet_json, sheet_url
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from uuid import uuid4

env_path = Path('./.env')
load_dotenv(dotenv_path=env_path)
# google spread sheet setting
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
json_file_name = sheet_json
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = sheet_url
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
API_NAME = "sheets"
API_VERSION = "V4"
service = discovery.build(API_NAME, API_VERSION, credentials=credentials)
sheet = service.spreadsheets()
spreadsheet_id = os.getenv('SPREADSHEET_ID')


worksheet = doc.worksheet(os.getenv('SPREADSHEET_NAME'))
# 1달
_list_dep_1 = []
today_date = date.today().day - 1
previous_month = str(date.today()-relativedelta(months=1) -
                     timedelta(days=today_date))
count_city = 0
bulk_datas = []
# collection data 가져오기
cursor = products.find(
    {'created_date': {'$gte': previous_month}}, no_cursor_timeout=True).batch_size(10000)

for i in cursor:
    _list_dep_2 = []
    _list_dep_2.append(i["city"])
    _list_dep_2.append(i["category"])
    _list_dep_2.append(i["title"])
    _list_dep_2.append(i["department"])
    _list_dep_2.append(i["views"])
    _list_dep_2.append(i["link"])
    _list_dep_2.append(i["created_date"])
    _list_dep_2.append(i["collected_date"])
    _list_dep_1.append(_list_dep_2)

    count_city += 1
    uuid_obj = uuid4()
    updated_date = datetime.utcnow()
    create_date = datetime.strptime(i['collected_date'], '%Y-%m-%d')
    try:
        registered_date = datetime.strptime(i['created_date'], '%Y-%m-%d')
    except ValueError:
        registered_date = datetime.today().strftime('%Y-%m-%d')

    # 기존 product collection update(uid,id,date)
    bulk_data = UpdateOne(
        {"$and": [{"title": i['title']}, {
            "region": i['city']}]},
        {"$set":
         {
             "uid": str(uuid_obj),
             "id": count_city,
             "region": i['city'],
             "category": i['cate'],
             "title": i['title'],
             "department": i['department'],
             "views": int(i['views']),
             "link": i['link'],
             "registered_date": registered_date,
             "created_at": create_date + timedelta(hours=9),
             "created_at_gmt": create_date,
             "updated_at": updated_date + timedelta(hours=9),
             "updated_at_gmt": updated_date
         }
         },
        upsert=True,
    )
    bulk_datas.append(bulk_data)  # bulk insert setting
    cursor.close()
cities_info.bulk_write(bulk_datas)  # db에 넣음

# google spread sheet에도 넣기
result = sheet.values().get(
    spreadsheetId=spreadsheet_id, range=os.getenv('SPREADSHEET_ID')).execute()
rows = result.get('values', [])
print('{0} rows retrieved.'.format(len(rows)))
worksheet.update('B{}'.format(len(rows)), _list_dep_1)
