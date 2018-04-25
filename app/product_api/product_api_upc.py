__author__ = 'Joseph'
from amazon.api import AmazonAPI, AsinNotFound
import datetime,re,time
from urllib.error import HTTPError
class Product_API:
    def __init__(self,aws_access_key,aws_secret_key,associate_tag,region):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.associate_tag = associate_tag
        self.amazon = AmazonAPI(self.aws_access_key, self.aws_secret_key, self.associate_tag,region=region)
    def formate_string(self,string):
        return '' if string is None else str(string)
        
    def formate_content(self,content):
        return content.replace('"','').replace('\t','').replace('\n','') if content else '' 
        
    def get_upc_details(self,productid):
        data = {}
        try:
            products = self.amazon.lookup(ItemId=productid, IdType='UPC', SearchIndex='All')
            try:
                #print('changdu',len(products))
                #print(productid)
                for i in range(len(products)):
                    asin = products[i].asin
                    upc = products[i].upc
                    data[upc] = True
                for upc in productid.split(','):
                    data[upc] = True
            except:
                pass
        except AsinNotFound:
            pass
        except HTTPError:
            time.sleep(0.5)
            self.get_product_details(productid)
        return data
          

# associate_tag = "christian"
# aws_access_key = "AKIAI2KC4CSH4A4ZVSGA"
# aws_secret_key = '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'
# start = datetime.datetime.now()
# amazon = AmazonAPI(aws_access_key, aws_secret_key, associate_tag)
# product_api = Product_API(aws_access_key,aws_secret_key,associate_tag,'US')
# print(product_api.get_upc_details('795186110222,795186121167,795186124847,784029225353,784029225384'))
# end = start = datetime.datetime.now()
# print((end-start).seconds)




