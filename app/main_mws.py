from myutil import myutil
from product_api import product_api_mws
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
mws_access_key = myutil.get_config_value(root_path,'mws','mws_access_key')
mws_secret_key = myutil.get_config_value(root_path,'mws','mws_secret_key')
mws_seller_id = myutil.get_config_value(root_path,'mws','seller_id')
region = myutil.get_config_value(root_path,'aws','region')
sales_rank_limit = myutil.get_config_value(root_path,'aws','sale_rank_limit')
product_api = product_api_mws.Product_API_MWS(mws_access_key,mws_secret_key,mws_seller_id,region)
file_date = datetime.date.today()
output_file = myutil.get_path(root_path,['src','output'])+'details_'+str(file_date)+'.txt'
while position<len(asins_list):
    data = product_api.get_product_details(myutil.convert_isbn(asins_list[position]),sales_rank_limit)
    #exit()
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




