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
        return content.replace('"',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('\u2028', ' ').replace('\u2029', ' ') if content else '' 

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
        try_time = 1

        input_asins = dict([item, True] for item in productid.split(','))
        # print(input_asins)
        # print(productid)
        # products = self.amazon.lookup(ItemId=productid)
        # try:
        #     products = self.amazon.lookup(ItemId=productid)
        # except:
        #     print('ASIN(s) ', productid ,' not found')
        #     return data,input_asins
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
                with open('src/output/log.txt', 'a', encoding='utf-8') as f:
                    f.write(str(err) + '\t' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n')

                if hasattr(err, 'code') and err.code == 503:
                    print('503 error')
                    time.sleep(1)
                else:
                    print('ASIN(s) ', productid ,' not found')
                    return data,input_asins
                


        # while try_time<10:
        #     try:                    
        if type(products) is not list:
            products = [products]

        for item in products:
            asin = item.asin
            print(asin)

            found_asins[asin] = True
            
            # authors = item.authors
            # authors = ';'.join(authors)
            # date = item.publication_date
            # date = datetime.datetime.strftime(date,'%B %d,%Y') if date else ''
            #artists = item.artists
            #artists = ';'.join(artists)
            isEligibleForPrime = self.formate_string(item.isEligibleForPrime)
            isPreorder = item.isPreorder
            if isPreorder:
                continue
            #exit()
            brand = self.formate_content(item.brand)
            brand = self.formate_string(brand)
            title = self.formate_content(item.title)
            manufacturer = self.formate_content(item.manufacturer)
            manufacturer = self.formate_string(manufacturer)
            has_review = self.formate_string(item.reviews)
            upc = self.formate_string(item.upc)
            color = item.color
            availability = self.formate_string(item.availability)
            #part_number = item.part_number
            editorial_review = ''
            try:
                editorial_review = item.editorial_review
            except:
                pass

            # editorial_review = item.editorial_review

            description = self.formate_content(editorial_review)
            features = item.features
            bullet_points = []
            for feature in features:
                if feature:
                    bullet_points.append(self.formate_content(feature))
            bullet_point = ';'.join(bullet_points)
            bullet_points = self.formate_string(bullet_points)
            #attributes = item.get_attribute('')
            #browse_nodes = item.browse_nodes
            new_sellers = self.formate_string(item.TotalNew)
            if new_sellers == '':
                new_sellers = '0'
            image = self.formate_string(item.large_image_url)
            rank = self.formate_string(item.sales_rank)
            cankao_price = self.formate_string(item.price_and_currency[0])
            #list_price = item.list_price[0]
            product_group = self.formate_string(item.product_group)
            binding = self.formate_string(item.binding)
            
            color = self.formate_string(item.color)
            color =self.formate_content(color)

            length = self.formate_string(item.length)
            width = self.formate_string(item.width)
            MaterialType = self.formate_string(item.MaterialType)
            MetalType = self.formate_string(item.MetalType)
            #print(item.MetalType)
            #exit()
            height = self.formate_string(item.height)
            weight = item.package_weight
            if not weight:
                weight = item.weight
            weight = self.formate_string(weight)
            size = self.formate_string(item.size)
            size =self.formate_content(size)
            browses_dic = {}
            browse_nodes = item.browse_nodes
            browses_name = ''
            for browse_node in browse_nodes:
                browses_list = []
                child_name=browse_node.name
                if browses_dic.get(child_name,True):
                    browses_list.append(str(child_name))
                browses_dic[child_name] = False
                ancestors = browse_node.ancestors
                for ancestor in ancestors:
                    ancestor_name = ancestor.name
                    if browses_dic.get(ancestor_name,True):
                        browses_list.append(str(ancestor_name))
                    browses_dic[ancestor_name] = False
                browses_list = browses_list[::-1]
                browses_name = browses_name +';'+'>'.join(browses_list)
            browses_name = self.formate_string(browses_name[1:])
            weight_new = weight
            if not weight_new:
                weight_new = '0'
            #if image and brand and prime_price and int(totalNew) and float(weight_new)<=30 :
            #    data.append('\t'.join([asin,title,manufacturer,brand,image,rank,availability,product_group,binding,weight,size,totalNew,isEligibleForPrime,browses_name,bullet_point,description,color,prime_price,upc,length,width,height]))
            data.append('\t'.join([asin,title,brand,rank,product_group,availability,new_sellers,has_review,cankao_price]))
            #     break
            # except:
            #     #data=[productid]
            #     print('Try time: ',try_time)
            #     try_time +=1
        #print(data)
        for asin in input_asins:
            if asin not in found_asins:
                left_asins[asin] = True
        print(left_asins)

        return data,left_asins



# associate_tag = 'christian'
# aws_access_key = 'AKIAI2KC4CSH4A4ZVSGA'
# aws_secret_key = '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'
# start = datetime.datetime.now()
# amazon = AmazonAPI(aws_access_key, aws_secret_key, associate_tag)
# product_api = Product_API(aws_access_key,aws_secret_key,associate_tag,'US')
# print(product_api.get_product_details('B01BB2H9YK,B014DTV2LE'))
# end = start = datetime.datetime.now()
# print((end-start).seconds)