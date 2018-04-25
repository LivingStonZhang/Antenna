__author__ = 'Joseph'
from mws import mws
import datetime,time
class Product_API_MWS:
    def __init__(self,mws_access_key,mws_secret_key,mws_seller_id,region):
        marketplaceid = {"CA" : "A2EUQ1WTGCTBG2","US" : "ATVPDKIKX0DER","DE" : "A1PA6795UKMFR9","ES" : "A1RKKUPIHCS9HS","FR" : "A13V1IB3VIYZZH",\
                         "IN" : "A21TJRUUN4KGV","IT" : "APJ6JRA9NG5V4","UK" : "A1F83G8C2ARO7P","JP" : "A1VC38T7YXB528","CN" : "AAHKV2X7AFYLW"}
        self.mws_access_key = mws_access_key
        self.mws_secret_key = mws_secret_key
        self.mws_seller_id = mws_seller_id
        self.region = region
        self.marketplaceid = marketplaceid[self.region.upper()]
        self.product_client=mws.Products(self.mws_access_key,self.mws_secret_key,self.mws_seller_id,self.region)

    def get_product_details(self,productid,sales_rank_limit):
        data = ''
        print(productid)
        try_time = 0
        while try_time<3:
            #try:
            try:
                product = self.product_client.get_matching_product(self.marketplaceid,[productid]).parsed.get('Product')
                competitive_price = self.product_client.get_competitive_pricing_for_asin(self.marketplaceid,[productid]).parsed.Product.CompetitivePricing
                #print(competitive_price)
                #print(product)
                product_att = product.AttributeSets.ItemAttributes
                #print(product_att)
                sales_rank = product.SalesRankings.get('SalesRank')[0].Rank if product.SalesRankings.get('SalesRank') else ''
                #print(sales_rank)
                if str(sales_rank)=='' or int(sales_rank)>int(sales_rank_limit):
                    break
                offerLisings = competitive_price.get('NumberOfOfferListings').get('OfferListingCount')
                if offerLisings:
                    offer_dic = {}
                    for offer in offerLisings:
                        offer_dic.update({offer.get('condition').get('value'):offer.get('value')})
                    total_new = offer_dic.get('New')
                    total_used = offer_dic.get('Used')
                else:
                    break
                binding = product_att.get('Binding').get('value')
                binding_new = self.get_binding(binding)
                if not binding_new:
                    break
                date = product.AttributeSets.ItemAttributes.get('PublicationDate').get('value')
                date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
                now = datetime.date.today()
                result = (now-date).days#preorder
                if result<0:
                    break
                #print(product_att)
                authors = product_att.get('Author')
                if authors:
                    authors2list = []
                    author_list = []
                    if type(authors)==list:
                        authors2list = authors
                    else:
                        authors2list.append(authors)
                    #print(authors2list)
                    for author in authors2list:
                        author = author.get('value')
                        if ',' in author:
                            author = author.split(',')
                            author.reverse()
                            author = ' '.join(author)
                        author_list.append(author)
                    authors = ';'.join(author_list)
                competitive_prices = competitive_price.CompetitivePrices.get('CompetitivePrice')
                if competitive_prices:
                    competitive_price_list = []
                    if type(competitive_prices)==list:
                        competitive_price_list = competitive_prices
                    else:
                        competitive_price_list.append(competitive_prices)
                    prices_dic = {}
                    for competitive_prices in competitive_price_list:
                        #print(competitive_prices)
                        prices_dic.update({competitive_prices.get('condition').get('value'):competitive_prices.get('Price').get('LandedPrice').get('Amount').get('value')})
                    new_price = prices_dic.get('New')
                    used_price = prices_dic.get('Used')
                else:
                    new_price = used_price = ''
                date = datetime.datetime.strftime(date,'%B %d,%Y') if date else ''
                title = product_att.get('Title').get('value')+' by '+author_list[0] if authors else product_att.get('Title').get('value')
                title = title+' ('+str(date)+')' if date else title
                manufacture = product_att.get('Manufacturer').get('value')+' ('+date+')' if date else product_att.get('Manufacturer').get('value')
                image = product_att.get('SmallImage').get('URL').get('value').replace('_SL75_','_SL500_')
                prime_price = product_att.get('ListPrice').get('Amount').get('value') if product_att.get('ListPrice') else ''
                languages = product_att.get('Languages').get('Language')
                #print(languages)
                language_dic ={}
                if languages:
                    language_list =[]
                    if type(languages)==list:
                        language_list = languages
                    else:
                        language_list.append(languages)
                    for language in language_list:
                        language_dic.update({language.get('Type').get('value'):language.get('Name').get('value')})
                language = language_dic.get('Published')
                data = '\t'.join([productid,title,str(manufacture),str(authors),str(binding_new),str(image),str(prime_price),\
                         str(sales_rank),str(binding),str(date),str(language),str(total_new),str(total_used),str(new_price),str(used_price)])
                print(data)
                break
            except:
                pass
                time.sleep(0.5)
            try_time +=1
            print(try_time)
        return data

    def get_product_details_test(self,productid):
        data = ''
        print(productid)
        while True:
            product = self.amazon.lookup(ItemId=productid)
            sales_rank = product.sales_rank
            print(sales_rank)
            if str(sales_rank)=='None' or int(sales_rank)>1000000:
                break
            total_new = product.TotalNew
            total_used = product.TotalUsed
            if int(total_new)==int(total_used)==0:
                break
            binding = product.binding
            binding_new = self.get_binding(binding)
            if not binding_new:
                break
            date = product.publication_date
            now = datetime.date.today()
            result = (now-date).days#preorder
            if result<0:
                break
            author = product.author
            lowest_new_price = product.LowestNewPrice[0]
            lowest_used_price = product.LowestUsedPrice[0]
            authors = ';'.join(product.authors)
            date = datetime.datetime.strftime(date,'%B %d,%Y') if date else ''
            title = product.title+' by '+author if author else product.title
            title = title+' ('+str(date)+')' if date else title
            manufacture = product.manufacturer+' ('+date+')' if date else product.manufacturer
            image = product.large_image_url
            prime_price = product.price_and_currency[0]
            list_price = product.list_price[0]

            language = ','.join(list(product.languages))
            data = '\t'.join([productid,str(sales_rank),title,str(manufacture),str(authors),str(binding_new),str(binding),str(date),\
                    str(language),str(image),str(prime_price),str(total_new),str(total_used),str(lowest_new_price),str(lowest_used_price)])
            print(data)
            break
        return data

    def get_binding(self,binding):
        binding_dic = {'Audio CD':'AudioCD','Bath Book':'BathBook','Board book':'BoardBook','Bonded Leather':'BondedLeather','Calendar':'Calendar','Card Book':'CardBook','Cards':'Cards','Audio Cassette':'Cassette','CD-ROM':'CdRom',\
               'Comic':'Comic','Diary':'Diary','DVD-ROM':'DvdRom','Flexibound':'Flexibound','Foam Book':'FoamBook','Hardcover':'Hardcover','Hardcover-spiral':'HardcoverSpiral','Imitation Leather':'ImitationLeather',\
               'Journal':'Journal','Leather Bound':'LeatherBound','Library Binding':'Library','Loose Leaf':'LooseLeaf','Map':'Map','Mass Market Paperback':'MassMarket',\
               'Misc. Supplies':'MiscSupplies','Pamphlet':'Pamphlet','Paperback':'Paperback','Plastic Comb':'PlasticComb','Poster':'Poster',\
               'Rag Book':'RagBook','Ring-bound':'RingBound','School & Library Binding':'School','Sheet music':'SheetMusic','Spiral-bound':'SpiralBound',\
               'Staple Bound':'StapleBound','Stationery':'Stationery','Textbook Binding':'Textbook','Vinyl Bound':'VinylBound','Wall Chart':'WallChart'}
        return binding_dic.get(binding,False)
