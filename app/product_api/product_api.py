
from amazon.api import AmazonAPI
import datetime,time
class Product_API:
    def __init__(self,aws_access_key,aws_secret_key,associate_tag):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.associate_tag = associate_tag
        self.amazon = AmazonAPI(self.aws_access_key, self.aws_secret_key, self.associate_tag)

    def get_product_details(self,productid,sales_rank_limit):
        data = ''
        print(productid)
        try_time = 0
        while try_time<3:
            try:
                product = self.amazon.lookup(ItemId=productid)
                sales_rank = product.sales_rank
                if str(sales_rank)=='None' or int(sales_rank)>int(sales_rank_limit):
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
                #list_price = product.list_price[0]

                # language = ','.join(list(product.languages))
                # data = '\t'.join([productid,title,str(manufacture),str(authors),str(binding_new),str(image),str(prime_price),\
                        # str(sales_rank),str(binding),str(date),str(language),str(total_new),str(total_used),str(lowest_new_price),str(lowest_used_price)])
                        
                data = '\t'.join([productid,title,str(manufacture),str(authors),str(binding_new),str(image),str(prime_price),\
                        str(sales_rank),str(binding),str(date),str(language),str(total_new),str(total_used),str(lowest_new_price),str(lowest_used_price)])
        

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



