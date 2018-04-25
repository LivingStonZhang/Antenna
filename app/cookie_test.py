__author__ = 'ACC53-1'
from selenium.webdriver.common.keys import Keys
from myutil import myutil
from selenium import webdriver
import time

driver=webdriver.Chrome('sys/chromedriver.exe')
driver.get("http://www.youdao.com")
cookie= driver.get_cookies()
print(cookie)

driver.quit()
