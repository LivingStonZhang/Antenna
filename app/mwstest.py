__author__ = 'ACC53-1'
import os
import configparser,time
from myutil import myutil
from mws import mws
root_path=os.path.abspath('..')
root_path=root_path.replace('\\','/')
config_path=myutil.get_path(root_path,['app','config'])+'config.ini'
config = configparser.ConfigParser()
config.read(config_path)
access_key=config.get('mws','mws_access_key')
secret_key=config.get('mws','mws_secret_key')
account_id=config.get('mws','seller_id')
market_place_id=config.get('mws','market_place_id')
region=config.get('mws','region').upper()
print(access_key,secret_key)
product_client=mws.Products(access_key,secret_key,account_id,region)
asins = ['B00Z8F00L6', 'B010EVS2BS', 'B009O0HZCI', 'B00FDVMSCE', 'B00MCA5UW4', 'B00YZLRJJU', 'B00FF0ND9U', 'B00C7GA8SE', 'B00SB2G9OK', 'B010EX3BVM', 'B011W95MY6', 'B00FG14BLC', 'B00Z8EXTCE', 'B00E6T3O18', 'B00N4JEHPS', 'B00ZVP8UW4', 'B00ZM398SK', 'B00YTJ1GLA', 'B00IJ0DITI', 'B00YZMNTXE']
while True:
    try:
        res = product_client.get_lowest_offer_listings_for_asin(market_place_id,asins,'Any')
        break
    except:
        pass
        time.sleep(10)
print(res.parsed)