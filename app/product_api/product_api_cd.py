__author__ = 'Joseph'
from amazon.api import AmazonAPI
import datetime,time,re
class Product_API:
    def __init__(self,aws_access_key,aws_secret_key,associate_tag,region):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.associate_tag = associate_tag
        self.amazon = AmazonAPI(self.aws_access_key, self.aws_secret_key, self.associate_tag,region=region)

    def formate_string(self,string):
        return '' if string is None else str(string)
    def formate_content(self,content):
        return content.replace('"','').replace('\t','').replace('\n','').replace('\r','').replace('\u2028', ' ').replace('\u2029', ' ') if content else '' 
    def get_product_details(self,productid):
        data = []
        left_asins = {}
        found_asins = {}
        input_asins = dict([item, True] for item in productid.split(','))
        while True:
            try:
                products = self.amazon.lookup(ItemId=productid)
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
            # authors = products[i].authors
            # authors = ';'.join(authors)
            # date = products[i].publication_date
            # date = datetime.datetime.strftime(date,'%B %d,%Y') if date else ''
            #artists = products[i].artists
            #artists = ';'.join(artists)
            #isEligibleForPrime = products[i].isEligibleForPrime
            isPreorder = products[i].isPreorder
            if isPreorder:
                continue
            #exit()
            brand = self.formate_content(products[i].brand)
            title = self.formate_content(products[i].title)
            manufacture = self.formate_content(products[i].manufacturer)
            artists = products[i].artists
            artists = ';'.join(artists)
            artists = self.formate_content(artists)
            artist = self.formate_content(products[i].artist)
            title_by = title+' by '+artist if artist else title
            review = self.formate_string(products[i].reviews)
            #upc = products[i].upc
            #color = products[i].color
            availability = products[i].availability
            release_date = self.formate_string(products[i].release_date)
            publication_date = self.formate_string(products[i].publication_date)
            title_by = title_by+' ('+str(publication_date)+')' if publication_date else title_by
            #part_number = products[i].part_number
            #editorial_review = products[i].editorial_review
            # features = products[i].features
            # bullet_points = []
            # for feature in features:
            #     if feature:
            #         bullet_points.append(feature.replace('\n','').replace('"','').replace('\t',''))
            # bullet_point = ';'.join(bullet_points)
            #attributes = products[i].get_attribute('')
            #browse_nodes = products[i].browse_nodes
            totalNew = products[i].TotalNew
            image = products[i].large_image_url
            sales_rank = products[i].sales_rank
            prime_price = products[i].price_and_currency[0]
            #list_price = products[i].list_price[0]
            product_group = products[i].product_group
            binding = products[i].binding
            # color = products[i].color
            # weight = products[i].package_weight
            # if not weight:
            #     weight = products[i].weight
            # size = products[i].size
            #language = ','.join(list(products[i].languages))
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
            data.append('\t'.join([asin,title_by,artists,manufacture,brand,image,sales_rank,availability,product_group,binding,publication_date,release_date,totalNew,prime_price,review]))
            #except:
                #pass
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




