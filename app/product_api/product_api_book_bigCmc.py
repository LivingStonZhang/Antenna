__author__ = 'Joseph'
from amazon.api import AmazonAPI
import datetime,time,sys,os,threading,functools,html

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
        str_temp = content.replace('"',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('\u2028', ' ').replace('\u2029', ' ') if content else '' 
        return html.escape(str_temp)
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
            #isEligibleForPrime = item.isEligibleForPrime
            isEligibleForPrime = self.formate_string(item.isEligibleForPrime)
            isPreorder = item.isPreorder
            if isPreorder:
                continue
            #exit()
            brand = item.brand.replace('"','').replace('\t','').replace('\n','') if item.brand else ''
            title = item.title.replace('"','').replace('\t','').replace('\n','') if item.title else ''
            manufacture = item.manufacturer.replace('"','').replace('\t','').replace('\n','') if item.manufacturer else ''
            authors = item.authors
            authors = ';'.join(authors)
            author = item.author
            editorial_review = ''
            try:
                editorial_review = item.editorial_review
            except:
                pass

            # editorial_review = item.editorial_review
            description = '\'\'\''+self.formate_content(editorial_review)+'\'\'\''
            review = self.formate_string(item.reviews)
            #upc = item.upc
            #color = item.color
            availability = item.availability
            release_date = self.formate_string(item.release_date)
            publication_date = self.formate_string(item.publication_date)
            #part_number = item.part_number
            #editorial_review = item.editorial_review
            # features = item.features
            # bullet_points = []
            # for feature in features:
            #     if feature:
            #         bullet_points.append(feature.replace('\n','').replace('"','').replace('\t',''))
            # bullet_point = '#||#'.join(bullet_points)
            #attributes = item.get_attribute('')
            #browse_nodes = item.browse_nodes
            totalNew = item.TotalNew
            image = ""
            n = 1
            for i in item.images:
                image += self.formate_string(i)
                if (len(item.images)-n)>0:
                    image += ";"
                n += 1
            sales_rank = item.sales_rank
            prime_price = item.price_and_currency[0]
            #list_price = item.list_price[0]
            product_group = item.product_group
            edition = self.formate_content(item.edition)
            binding = item.binding
            # color = item.color
            # weight = item.package_weight
            # if not weight:
            #     weight = item.weight
            # size = item.size
            language = ','.join(list(item.languages))
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
            sales_rank = '' if sales_rank is None else str(sales_rank)
            manufacture = '' if manufacture is None else str(manufacture)
            prime_price = '' if prime_price is None else str(prime_price)
            #list_price = '' if list_price is None else str(list_price)
            brand = '' if brand is None else str(brand)
            image = '' if image is None else str(image)
            availability = '' if availability is None else str(availability)
            product_group = '' if product_group is None else str(product_group)
            # weight = '' if weight is None else str(weight)
            # size = '' if size is None else str(size)
            totalNew = '' if totalNew is None else str(totalNew)
            #bullet_point = '' if bullet_point is None else str(bullet_point)
            #upc = '' if upc is None else str(upc)
            # color = '' if color is None else str(color)
            binding = '' if binding is None else str(binding)
            #isEligibleForPrime = '' if isEligibleForPrime is None else str(isEligibleForPrime)
            #print(bullet_point)
            #print(asin,title,manufacture,brand,image,sales_rank,availability,product_group,weight,size,totalNew,bullet_point,prime_price,list_price,upc,color)
            #exit()
            #print(asin,sales_rank,title,manufacture,authors,binding,date,language,image,prime_price,list_price)
            #try:
            data.append('\t'.join([asin,title,authors,manufacture,brand,image,sales_rank,availability,product_group,binding,publication_date,release_date,totalNew,isEligibleForPrime,browses_name,description,prime_price,language,review,edition]))

        for asin in input_asins:
            if asin not in found_asins:
                left_asins[asin] = True
        print(left_asins)

        return data,left_asins



# associate_tag = christian
# aws_access_key = AKIAI2KC4CSH4A4ZVSGA
# aws_secret_key = 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
# start = datetime.datetime.now()
# amazon = AmazonAPI(aws_access_key, aws_secret_key, associate_tag)
# product_api = Product_API(aws_access_key,aws_secret_key,associate_tag,'US')
# print(product_api.get_product_details('B01928T0DS,B00D7MDXCU'))
# end = start = datetime.datetime.now()
# print((end-start).seconds)