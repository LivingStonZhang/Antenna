from myutil import myutil
from product_api import product_api
import os
import datetime
start = datetime.datetime.now()
app_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=os.path.abspath(app_path+'../').rstrip('/')+'/'
root_path=root_path.replace('\\','/')
asin_dir = myutil.get_path(root_path,['src','asins'])
asins_list = myutil.get_asins_from_asindir(asin_dir)
config_dir=myutil.get_path(root_path,['app','config'])
position = int(myutil.get_config_value(root_path,'aws','position'))
aws_access_key = myutil.get_config_value(root_path,'aws','aws_access_key')
aws_secret_key = myutil.get_config_value(root_path,'aws','aws_secret_key')
associate_tag = myutil.get_config_value(root_path,'aws','associate_tag')
product_api = product_api.Product_API(aws_access_key,aws_secret_key,associate_tag)
output_file = myutil.get_path(root_path,['src','output'])+'details.txt'
data = product_api.get_product_details_test('0804138141')
print(data)




