__author__ = 'Joseph'
from amazon.api import AmazonAPI
import datetime,time,re,sys,os,threading,functools
class Product_API:
    def __init__(self,aws_access_key,aws_secret_key,associate_tag,region):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.associate_tag = associate_tag
        self.amazon = AmazonAPI(self.aws_access_key, self.aws_secret_key, self.associate_tag,region=region)

    def restart_program():
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def formate_string(self,string):
        return '' if string is None else str(string)
        
    def formate_content(self,content):
        return content.replace('"','').replace('\t','').replace('\n','') if content else '' 

    def timed_out(timeout):
        def _timed_out(func):
            @functools.wraps(func)
            def _func(*args, **kwargs):
                result = [None]
                def timed_func():
                    try:
                        result[0] = func(*args, **kwargs)
                    except Exception as e:
                        result[0] = e

                alarm = threading.Thread(target=timed_func, daemon=True)
                try:
                    alarm.start()
                    alarm.join(timeout)
                except Exception as e:
                    raise e
                if isinstance(result[0], Exception):
                    raise result[0]
                return result[0]
            return _func
        return _timed_out

    @timed_out(60)
    def amazonLookup(self,productid):
        return self.amazon.lookup(ItemId=productid)    
        
    def get_product_details(self,productid):
        data = []
        left_asins = {}
        found_asins = {}
        input_asins = dict([item, True] for item in productid.split(','))
        try_time = 0
        while True:
            try_time += 1
            print("try time: " + str(try_time))
            try:
                products = self.amazonLookup(productid)
                if products == None:
                    restart_program()
                break
            except Exception as err:
                with open('C:/shujubu/ScraperApp_Pro/src/output/log.txt', 'a', encoding='utf-8') as f:
                    f.write(str(err) + '\t' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n')

                if hasattr(err, 'code') and err.code == 503:
                    print('503 error')
                    time.sleep(1)
                else:
                    print('ASIN(s) ', productid ,' not found')
                    return data,input_asins
        #print(data)
        if type(products) is not list:
            products = [products]

        for i in range(len(products)):
            asin = products[i].asin
            print(asin)
            found_asins[asin] = True
            actors = self.formate_string(products[i].actors)
            actors = ';'.join(actors)
            actor = products[i].actor
            directors = self.formate_string(products[i].directors)
            directors = ';'.join(directors)
            director = products[i].director
            release_date = self.formate_string(products[i].release_date)
            #isEligibleForPrime = products[i].isEligibleForPrime
            isPreorder = self.formate_string(products[i].isPreorder)
            if isPreorder:
                continue
            #exit()
            #brand = products[i].brand
            manufacturer = self.formate_string(products[i].manufacturer)
            title = self.formate_content(products[i].title)
            if actor:
                title = title + ' by '+actor
            elif director:
                title = title +' by '+director
            studio = self.formate_string(products[i].studio)
            region_code = self.formate_string(products[i].region_code)
            audience_rating = self.formate_string(products[i].audience_rating())
            editorial_review = re.sub("<.*?>", "", self.formate_string(products[i].editorial_review))
            editorial_review = self.formate_content(editorial_review)
            availability = self.formate_string(products[i].availability)
            totalNew = self.formate_string(products[i].TotalNew)
            image = self.formate_string(products[i].large_image_url)
            sales_rank = self.formate_string(products[i].sales_rank)
            buybox_price = self.formate_string(products[i].price_and_currency[0])
            product_group = self.formate_string(products[i].product_group)
            binding = self.formate_string(products[i].binding)
            review = self.formate_string(products[i].reviews)
            data.append('\t'.join([asin,title,manufacturer,studio,image,sales_rank,availability,product_group,binding,actors,directors,totalNew,editorial_review,release_date,audience_rating,region_code,buybox_price,review]))
        for asin in input_asins:
            if asin not in found_asins:
                left_asins[asin] = True
        print(left_asins)

        return data,left_asins
          

# associate_tag = "christian"
# aws_access_key = "AKIAI2KC4CSH4A4ZVSGA"
# aws_secret_key = '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'
# start = datetime.datetime.now()
# amazon = AmazonAPI(aws_access_key, aws_secret_key, associate_tag)
# product_api = Product_API(aws_access_key,aws_secret_key,associate_tag,'US')
# print(product_api.get_product_details('B00023BM0C,B0009OZC8W'))
# end = start = datetime.datetime.now()
# print((end-start).seconds)




