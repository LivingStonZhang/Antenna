__author__ = 'Joseph'
from myutil import myutil
from product_api import product_api
import os
from datetime import datetime
start = datetime.now()
app_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=os.path.abspath(app_path+'../').rstrip('/')+'/'
root_path=root_path.replace('\\','/')
file_name = input('Please input the file name:')
source_asin_dir = myutil.get_path(root_path,['src','source_asins'])
filter_asin_dir = myutil.get_path(root_path,['src','filter_asins'])
source_asins = myutil.get_source_asins_from_asindir(source_asin_dir)
print(len(source_asins))
filter_asins = myutil.get_filter_asins_from_filter_asindir(filter_asin_dir)
print(len(filter_asins))
print('\n')
asins_list = myutil.get_asins(source_asins,filter_asins)
print(len(asins_list))
asin_path = myutil.get_path(root_path,['src','asins_temp'])
myutil.write_to_asinfile(file_name,asin_path,asins_list)
end = datetime.now()
print((end-start).seconds)





