from myutil import myutil
from product_api import orders
import os
import datetime
start = datetime.datetime.now()
app_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=os.path.abspath(app_path+'../').rstrip('/')+'/'
root_path=root_path.replace('\\','/')
asin_dir = myutil.get_path(root_path,['src','asins'])
config_dir=myutil.get_path(root_path,['app','config'])
position = int(myutil.get_config_value(root_path,'aws','position'))
mws_access_key = myutil.get_config_value(root_path,'mws','mws_access_key')
mws_secret_key = myutil.get_config_value(root_path,'mws','mws_secret_key')
mws_seller_id = myutil.get_config_value(root_path,'mws','seller_id')
region = myutil.get_config_value(root_path,'aws','region')
orders_client = orders.Orders(mws_access_key,mws_secret_key,mws_seller_id,region)
orderids_list = orders_client.get_orderids("2015-11-01","2015-11-02")
asins_list = []
if orderids_list:
    for orderid in orderids_list:
        asin = orders_client.get_order_asin(orderid)
        asins_list.append(asin)
print(asins_list)

file_date = datetime.date.today()
#output_file = myutil.get_path(root_path,['src','output'])+'details_'+str(file_date)+'.txt'