import pandas as pd
from selenium import webdriver
import chromedriver_binary
import get_instagram_info
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data = pd.read_csv('../data/data_official.csv')
url_home = 'https://www.instagram.com'
urls = []
for user in data['Followers']:
    urls.append(url_home + '/' + user)

with open('../conf/config.yml') as f:
    config = yaml.safe_load(f)

PHONE_NUMBER = config['phone_number']
PASSWORD = config['password']
URL_TARGET = config['target']

followers_getter = get_instagram_info.GetterInstagramFollower(PHONE_NUMBER, PASSWORD)
followers_getter.login()

for idx, url in enumerate(urls):
    followers_getter.get_page(url)
    logger.info(f"{idx} / {len(url)}")