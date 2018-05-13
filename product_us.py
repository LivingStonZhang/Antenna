from app.myutil import myutil
from app.product_api import product_api_product
import os,time
import datetime
from DB.sqliteDB import DButil

DB = DButil()
start = datetime.datetime.now()
app_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=os.path.abspath('').rstrip('/')+'/'
region = os.path.abspath(__file__).split('/')[-1].split('_')[-1].replace('.py','').upper()
data_type = os.path.abspath(__file__).split('/')[-1].split('_')[0].lower()
source_asin_dir = myutil.get_path(root_path,['src','source_asins',region])
filter_asin_dir = myutil.get_path(root_path,['src','filter_asins'])
output_dir = myutil.get_path(root_path,['src','output'])

# delete all file in source_asin_dir
myutil.deleteFile(source_asin_dir)

# delete all file in output_dir
myutil.deleteFile(output_dir+region.lower())

print("region---"+region)
print("data_type---"+data_type)
print("source_asin_dir---"+source_asin_dir)
print("filter_asin_dir---"+filter_asin_dir)
print("output_dir---"+output_dir)


# This source_asins needs get from main database return new asin need to grab details.Generate a new txt file for grab
# one time per day
remote_flag = myutil.checkRemoteAsinLeft()
if(remote_flag == True):
    myutil.getAsinRemote()

    source_asins = myutil.get_source_asins_from_asindir(source_asin_dir)
    output_file = output_dir + region.lower() + '_details.txt'
    left_asins_file = output_dir + region.lower() + 'left_asins.txt'
    filter_asins = myutil.get_filter_asins_from_filter_asindir(filter_asin_dir)
    asins_list = myutil.get_asins(source_asins, filter_asins, data_type)
    print("asin_list---" + str(len(asins_list)))
    asins_list.sort()
    if not len(asins_list):
        print('There is no source asins, please check it.')
    config_dir = myutil.get_path(root_path, ['app', 'config'])
    try:
        position = int(myutil.get_config_value(root_path, 'aws', 'position_' + region.lower()))
    except:
        myutil.set_config_value(root_path, 'aws', 'position_' + region.lower(), '0')
        position = int(myutil.get_config_value(root_path, 'aws', 'position_' + region.lower()))
    aws_access_key = myutil.get_config_value(root_path, 'aws', 'aws_access_key')
    aws_secret_key = myutil.get_config_value(root_path, 'aws', 'aws_secret_key')
    associate_tag = myutil.get_config_value(root_path, 'aws', 'associate_tag')
    product_api = product_api_product.Product_API(aws_access_key, aws_secret_key, associate_tag, region)
    print(position)
    if not position:
        output = open(output_file, 'a', encoding='utf-8')
        output.write('\t'.join(
            ['productid', 'title', 'brand', 'rank', 'product_group', 'availability', 'new_sellers', 'has_reviews',
             'cankao_price']) + '\n')
        output.close()
        position += 1

    while position <= len(asins_list):
        datas = []
        left_asins = {}
        productids = ','.join(asins_list[position - 1:position + 9])
        datas, left_asins = product_api.get_product_details(productids)
        if datas:
            for data in datas:
                myutil.write_to_file(output_file, data)
        if left_asins:
            for asin in left_asins:
                myutil.write_to_file(left_asins_file, asin)
        position += 10
        myutil.set_config_value(root_path, 'aws', 'position_' + region.lower(), str(position))
        time.sleep(0.6)
    end = datetime.datetime.now()
    print((end - start).seconds)
    time.sleep(1)
    datetime = time.strftime('%y%m%d%H%M%S')
    new_file = output_dir + region.lower() + '_details' + str(datetime) + '.txt'
    left_asins_new_file = output_dir + region.lower() + '_left_asins' + str(datetime) + '.txt'
    if os.path.exists(output_file):
        os.rename(output_file, new_file)
    if os.path.exists(left_asins_file):
        os.rename(left_asins_file, left_asins_new_file)
    if os.listdir(source_asin_dir):
        for file in os.listdir(source_asin_dir):
            os.rename(source_asin_dir + file, source_asin_dir + file.replace('.txt', '.finish'))
            # insert data into table details
            details_result = DB.insertDetails(new_file)
            # insert data into table price_unit
            price_unit_result = DB.insertPrice_unit(new_file)
            print(details_result)
            print(price_unit_result)
    myutil.set_config_value(root_path, 'aws', 'position_' + region.lower(), '0')


# Whatever is there asin from remote database. NEED TO CHECK EVERY TIME ! If there is no new asin need to grab. Then
# get the asins from price_unit table . Generate another txt file for grab
DBresult = myutil.DBtoFile()

source_asins = myutil.get_source_asins_from_asindir(source_asin_dir)
output_file = output_dir+region.lower()+'_details.txt'
left_asins_file = output_dir+region.lower()+'left_asins.txt'
filter_asins = myutil.get_filter_asins_from_filter_asindir(filter_asin_dir)
asins_list = myutil.get_asins(source_asins,filter_asins,data_type)
print("asin_list---"+str(len(asins_list)))
asins_list.sort()
if not len(asins_list):
    print('There is no source asins, please check it.')
config_dir=myutil.get_path(root_path,['app','config'])
try:
    position = int(myutil.get_config_value(root_path,'aws','position_'+region.lower()))
except:
    myutil.set_config_value(root_path,'aws','position_'+region.lower(),'0')
    position = int(myutil.get_config_value(root_path,'aws','position_'+region.lower()))
aws_access_key = myutil.get_config_value(root_path,'aws','aws_access_key')
aws_secret_key = myutil.get_config_value(root_path,'aws','aws_secret_key')
associate_tag = myutil.get_config_value(root_path,'aws','associate_tag')
product_api = product_api_product.Product_API(aws_access_key,aws_secret_key,associate_tag,region)
print(position)
if not position:
    output = open(output_file,'a',encoding='utf-8')
    output.write('\t'.join(['productid','title','brand','rank','product_group','availability','new_sellers','has_reviews','cankao_price'])+'\n')
    output.close()
    position +=1

while position<=len(asins_list):
    datas = []
    left_asins = {}
    productids = ','.join(asins_list[position-1:position+9])
    datas,left_asins = product_api.get_product_details(productids)
    if datas:
        for data in datas:
            myutil.write_to_file(output_file,data)
    if left_asins:
        for asin in left_asins:
            myutil.write_to_file(left_asins_file,asin)
    position +=10
    myutil.set_config_value(root_path,'aws','position_'+region.lower(),str(position))
    time.sleep(0.6)
end = datetime.datetime.now()
print((end-start).seconds)
time.sleep(1)
datetime = time.strftime('%y%m%d%H%M%S')
new_file = output_dir+region.lower()+'_details'+str(datetime)+'.txt'
left_asins_new_file = output_dir+region.lower()+'_left_asins'+str(datetime)+'.txt'
if os.path.exists(output_file):
    os.rename(output_file,new_file)
if os.path.exists(left_asins_file):
    os.rename(left_asins_file,left_asins_new_file)
if os.listdir(source_asin_dir):
    for file in os.listdir(source_asin_dir):
        os.rename(source_asin_dir+file,source_asin_dir+file.replace('.txt','.finish'))
        # # insert data into table details
        # details_result = DB.insertDetails(new_file)
        # # insert data into table price_unit
        # price_unit_result = DB.insertPrice_unit(new_file)
        # print(details_result)
        # print(price_unit_result)

        # This is a part for update local database
myutil.set_config_value(root_path,'aws','position_'+region.lower(),'0')
