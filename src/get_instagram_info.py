from selenium import webdriver
import chromedriver_binary
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
import logging
import pandas as pd
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GetterInstagramFollower:
    def __init__(self, phone_number, password):
        options = Options() 
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=options)
        self.phone_number = phone_number
        self.password = password
        self.url_home = 'https://www.instagram.com'

    def login(self):
        self.driver.get(self.url_home)
        time.sleep(3)

        self.driver.find_element_by_css_selector('#loginForm > div.Igw0E.IwRSH.eGOV_._4EzTm.kEKum > div:nth-child(5) > button > span.KPnG0').click()
        time.sleep(3)

        self.driver.find_element_by_name('email').send_keys(self.phone_number)
        self.driver.find_element_by_name('pass').send_keys(self.password)
        self.driver.find_element_by_id('loginbutton').click()
        time.sleep(3)
        
        # self.driver.find_element_by_name('__CONFIRM__').click()
        # time.sleep(3)

    def get_target_follower_raw(self, url_target):
        self.driver.get(url_target)
        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]').click()
        time.sleep(3)
        follower_popup = self.driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.isgrP')

        follower_list_text_prev = 'start'
        while True:
            logger.info('getting followers...')
            if follower_list_text_prev == follower_popup.text:
                break
            else:
                follower_list_text_prev = follower_popup.text
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', follower_popup)
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', follower_popup)
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', follower_popup)
                time.sleep(5)

        follower_list_raw = follower_popup.text.split()

        return follower_list_raw

    def get_target_follower(self, follower_list_raw):
        follower_list = []
        for idx, element in enumerate(follower_list_raw):
            if idx == 0:
                follower_list.append(element)
            if (element == 'フォロー中' or element == 'フォローする') and idx+1 != len(follower_list_raw):
                follower_list.append(follower_list_raw[idx+1])
        
        return follower_list

    def get_number_followers(self, follower_list):
        n_follower_list = []
        for idx, follower in enumerate(follower_list):
            logger.info(f'getting number of followers...{idx}/{len(follower_list)}')
            self.driver.get(self.url_home + '/' + follower)
            time.sleep(3)

            try:
                n_follower_list.append(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text)
            except Exception as e1:
                try:
                    n_follower_list.append(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span').text)
                except Exception as e2:
                    n_follower_list.append('')
                    logger.info(f'some exception occered!!') 

            logger.info(f'{follower}のフォロワー人数: {n_follower_list[idx]}')

        return n_follower_list

    def export_data(self, follower_list, n_follower_list):
        data = pd.DataFrame({
            'Followers': follower_list,
            'NumberOfFollowers': n_follower_list
        })

        data.to_csv('../data/data.csv')
    
    def get_page(self, url):
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)

if __name__ == '__main__':
    with open('../conf/config.yml') as f:
        config = yaml.safe_load(f)

    PHONE_NUMBER = config['phone_number']
    PASSWORD = config['password']
    URL_TARGET = config['target']

    logger.info('start processing!!')
    followers_getter = GetterInstagramFollower(PHONE_NUMBER, PASSWORD)

    logger.info('start login')
    followers_getter.login()

    logger.info('start getting followers raw list')
    follower_list_raw = followers_getter.get_target_follower_raw(URL_TARGET)

    logger.info('start getting followers list from raw')
    follower_list = followers_getter.get_target_follower(follower_list_raw)

    logger.info('start getting number of followers')
    n_follower_list = followers_getter.get_number_followers(follower_list)

    logger.info('exporting data')
    followers_getter.export_data(follower_list, n_follower_list)
