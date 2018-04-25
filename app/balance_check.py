__author__ = 'ACC53-1'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from myutil import myutil
import time
import os

def auto_login(driver,email,passwd):
	if driver:
		try:
			if driver.find_element_by_name("email"):
				elem_email=driver.find_element_by_name("email")
				elem_passwd = driver.find_element_by_name("password")
				elem_email.clear()
				elem_email.send_keys(email)
				elem_passwd.send_keys(passwd)
				elem_passwd.send_keys(Keys.RETURN)
				assert 'Amazon' in self.title
				global loged_email
				loged_email=email
				print('loged email:',loged_email)
		except:
			pass

app_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=os.path.abspath(app_path+'../').rstrip('/')+'/'
root_path=root_path.replace('\\','/')
prime_email = myutil.get_config_value(root_path,'acc_info','prime_email')
prime_password = myutil.get_config_value(root_path,'acc_info','prime_password')
driver=webdriver.Chrome('sys/chromedriver.exe')
base_url = 'http://www.amazon.com/gp/css/gc/balance'
driver.get(base_url)
auto_login(driver,prime_email,prime_password)
time.sleep(10)
driver.quit()
