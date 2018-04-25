from myutil import myutil
from product_api import product_api
import os,threading
from queue import Queue
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
def get_book_details():
    global position
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

lock = threading.Lock()
# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        print('worker:'+str(item))
        get_book_details()
        q.task_done()
# Create the queue and thread pool.
q = Queue()
for i in range(2):
    t = threading.Thread(target=worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

for item in range(len(asins_list)-position):
    q.put(item)
q.join()
end = datetime.datetime.now()
print('Spend Time: '+str((end-start).seconds))




