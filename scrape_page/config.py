import pymongo
from pymongo import bulk
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne, DeleteOne
import time
import datetime
from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path('./.env')
load_dotenv(dotenv_path=env_path)


if os.getenv('PYTHON_ENV') == 'local':
    env_path = Path('./env/local.env')
    load_dotenv(dotenv_path=env_path)

    connection = pymongo.MongoClient()
    db = connection[os.getenv('DATABASE')]
    all_link = db[os.getenv('COLLECTION_ALL_LINKS')]
    link = db[os.getenv('COLLECTION_LINKS')]
    products = db[os.getenv('COLLECTION_PRODUCTS')]

    sheet_url = os.getenv('SHEET_URL')
    sheet_json = os.getenv('SHEET_JSON')


elif os.getenv('PYTHON_ENV') == 'staging':
    env_path = Path('./env/staging.env')
    load_dotenv(dotenv_path=env_path)

    connection = pymongo.MongoClient(os.getenv('STAGING_ATLAS_URL'))
    db = connection[os.getenv('STAGING_ATLAS_DATABASE')]

    connection_local = pymongo.MongoClient(os.getenv('ATLAS_URL'))
    db_local = connection_local[os.getenv('ATLAS_DATABASE')]
    doc_local = db_local[os.getenv('ATLAS_COLLECTION_PRODUCTS')]

    sub_db = connection[os.getenv('STAGING_ATLAS_DATABASE_SUB')]
    cities_info = sub_db[os.getenv('STAGING_ATLAS_COLLECTION_SUB')]
    doc_code = sub_db[os.getenv('STAGING_ATLAS_COLLECTION_CODE')]

    all_link = db[os.getenv('STAGING_ATLAS_COLLECTION_ALL_LINKS')]
    link = db[os.getenv('STAGING_ATLAS_COLLECTION_LINKS')]
    products = db[os.getenv('STAGING_ATLAS_COLLECTION_PRODUCTS')]

    sheet_url = os.getenv('STAGING_ATLAS_SHEET_URL')
    sheet_json = os.getenv('STAGING_ATLAS_SHEET_JSON')


elif os.getenv('PYTHON_ENV') == 'production':
    env_path = Path('./env/production.env')
    load_dotenv(dotenv_path=env_path)

    connection = pymongo.MongoClient(os.getenv('PRODUCTION_ATLAS_URL'))
    db = connection[os.getenv('PRODUCTION_ATLAS_DATABASE')]

    all_link = db[os.getenv('PRODUCTION_ATLAS_COLLECTION_ALL_LINKS')]
    link = db[os.getenv('PRODUCTION_ATLAS_COLLECTION_LINKS')]
    products = db[os.getenv('PRODUCTION_ATLAS_COLLECTION_PRODUCTS')]

    sheet_url = os.getenv('PRODUCTION_ATLAS_SHEET_URL')
    sheet_json = os.getenv('PRODUCTION_ATLAS_SHEET_JSON')


if os.getenv('PYTHON_ENV') == 'local':

    print('ENV=>', os.getenv('ENV'))

    print('(LOCAL) db =>', os.getenv('DATABASE'))
    print('(LOCAL) all_link =>', os.getenv('COLLECTION_ALL_LINKS'))
    print('(LOCAL) link =>', os.getenv('COLLECTION_LINKS'))
    print('(LOCAL) products=>', os.getenv('COLLECTION_PRODUCTS'))

    print('(LOCAL) sheet_url =>', os.getenv('SHEET_URL'))
    print('(LOCAL) sheet_json =>', os.getenv('SHEET_JSON'))


elif os.getenv('PYTHON_ENV') == 'staging':

    print('ENV=>', os.getenv('ENV'))

    print('(ATLAS) db_local =>', os.getenv(
        'ATLAS_DATABASE'))
    print('(ATLAS) doc_local=>', os.getenv(
        'ATLAS_COLLECTION_PRODUCTS'))
    print('(STAGING_ATLAS) db =>', os.getenv(
        'STAGING_ATLAS_DATABASE'))
    print('(STAGING_ATLAS) all_link=>', os.getenv(
        'STAGING_ATLAS_COLLECTION_ALL_LINKS'))
    print('(STAGING_ATLAS) link=>', os.getenv(
        'STAGING_ATLAS_COLLECTION_LINKS'))
    print('(STAGING_ATLAS) products>', os.getenv(
        'STAGING_ATLAS_COLLECTION_PRODUCTS'))
    print('(STAGING_ATLAS) sub_db =>', os.getenv(
        'STAGING_ATLAS_DATABASE_SUB'))
    print('(STAGING_ATLAS) cities_info=>', os.getenv(
        'STAGING_ATLAS_COLLECTION_SUB'))
    print('(STAGING_ATLAS) doc_code=>', os.getenv(
        'STAGING_ATLAS_COLLECTION_CODE'))
    print('(STAGING_ATLAS) sheet_url =>', os.getenv(
        'STAGING_ATLAS_SHEET_URL'))
    print('(STAGING_ATLAS) sheet_json =>', os.getenv(
        'STAGING_ATLAS_SHEET_JSON'))


elif os.getenv('PYTHON_ENV') == 'production':

    print('ENV=>', os.getenv('ENV'))

    print('(PRODUCTION_ATLAS) db =>', os.getenv(
        'PRODUCTION_ATLAS_DATABASE'))
    print('(PRODUCTION_ATLAS) all_link=>', os.getenv(
        'PRODUCTION_ATLAS_COLLECTION_ALL_LINKS'))
    print('(PRODUCTION_ATLAS) link=>', os.getenv(
        'PRODUCTION_ATLAS_COLLECTION_LINKS'))
    print('(PRODUCTION_ATLAS) products>', os.getenv(
        'PRODUCTION_ATLAS_COLLECTION_PRODUCTS'))
    print('(PRODUCTION_ATLAS) sheet_url =>', os.getenv(
        'PRODUCTION_ATLAS_SHEET_URL'))
    print('(PRODUCTION_ATLAS) sheet_json =>', os.getenv(
        'PRODUCTION_ATLAS_SHEET_JSON'))
