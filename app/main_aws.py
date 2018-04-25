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
sales_rank_limit = myutil.get_config_value(root_path,'aws','sale_rank_limit')
product_api = product_api.Product_API(aws_access_key,aws_secret_key,associate_tag)
file_date = datetime.date.today()
output_file = myutil.get_path(root_path,['src','output'])+'details_'+str(file_date)+'.txt'
while position<len(asins_list):
    data = product_api.get_product_details(myutil.convert_isbn(asins_list[position]),sales_rank_limit)
    if data:
        try:
            myutil.write_to_file(output_file,data)
            #print(data)
        except:
            pass
    # else:
    #     print(asins[position])
    print('position: '+str(position))
    position +=1
    myutil.set_config_value(root_path,'aws','position',str(position))
end = datetime.datetime.now()
print('Spend Time: '+str((end-start).seconds))




