__author__ = 'can'
import random,time,shutil,os
def is_number(n):
    try:
        0+n
        return True
    except:
        return False
def is_number_str(n):
    try:
        float(n)
        return True
    except:
        return False
class Product(object):
    def __init__(self,sku,asin,**kwargs):
        self.sku=sku
        self.asin=asin
        self.isbn=None
        self.inner_price=None
        self.outer_price=None
        self.source_price=None
        self.margin=None
        self.reference=None
        self.category=None
        self.shipping_fee=None
        self.retail_price=None
        self.competitor_on_bottom=False
        self.quantity=3
        self.categories=['book','product']
        self.compare_methods=['equal','lower','higher']
        self.default_compare_method='lower'
        inner_price=kwargs.get('inner_price',None)
        if is_number_str(inner_price):
            self.inner_price=float(inner_price)
    def set_isbn(self,isbn):
        self.isbn=isbn
    def set_inner_price(self,inner_price):
        if is_number_str(inner_price):
            self.inner_price=float(inner_price)
    def set_outer_price(self,outer_price):
        if is_number_str(outer_price):
            self.outer_price=float(outer_price)
        elif outer_price!=None:
            self.outer_price='n'
    def set_shipping_fee(self,shipping_fee):
        if is_number_str(shipping_fee):
            self.shipping_fee=float(shipping_fee)
    def set_base_price(self,base_price):
        if is_number_str(base_price):
            self.base_price=float(base_price)
    def set_source_price(self,source_price):
        if is_number_str(source_price):
            self.source_price=float(source_price)
    def set_compare_method(self,compare_method):
        if compare_method in self.compare_methods:
            self.compare_method=compare_method
        else:
            self.compare_method=self.default_compare_method
    def set_category(self,category):
        self.category=category
    def set_quantity(self,quantity):
        self.quantity=quantity
    def set_competitor_on_bottom(self,competitor_on_bottom):
        if competitor_on_bottom=='True' or competitor_on_bottom=='1':
            self.competitor_on_bottom=True
        else:
            self.competitor_on_bottom=False
class Analysis(object):
    def __init__(self,**kwargs):
        self.compare_methods=['equal','lower','higher']
        self.base_price=kwargs.get('base_price',4.00)
        self.compare_method=kwargs.get('compare_method','lower')
        self.down_percent=kwargs.get('down_percent',0.7)
        self.up_percent=kwargs.get('up_percent',0.07)
        self.higher_percent=kwargs.get('higher_percent',0.05)
        self.gap_max=kwargs.get('gap_max',300)
        self.gap_points=kwargs.get('gap_points',(20,1.5,0.06))
        self.monopoly_up_percent=kwargs.get('monopoly_up_percent',0.1)
        self.monopoly_max=kwargs.get('monopoly_max',500)
        self.source_min_profit=kwargs.get('source_min_profit',2)
        self.source_profit_times=kwargs.get('source_profit_times',2.6)
        self.source_monopoly_points=kwargs.get('source_monopoly_points',(3,15))
        self.source_monopoly_points=list(self.source_monopoly_points)
        self.ajax_up_points=kwargs.get('ajax_up_points',(0.3,0.04))
        self.ajax_up_points=list(self.ajax_up_points)
        self.getprice_method=kwargs.get('getprice_method','api')
        self.h=time.localtime().tm_hour
        self.h=str(self.h)
        self.workingasins_dic=kwargs.get('workingasins_dic',{})
        self.up_hours=kwargs.get('up_hours',(str(i) for i in range(24)))
        if type(self.up_hours)==type(''):
            self.up_hours=self.up_hours.split(',')
        self.is_ajax_requantity=kwargs.get('is_ajax_requantity',False)
        self.is_source_requantity=kwargs.get('is_source_requantity',False)
        self.compare_methods=['equal','lower','higher']
        self.default_compare_method='lower'
        # print(self.gap_points)
    def set_retail_parameters(self,**kwargs):
        self.base_price=kwargs.get('base_price',4.00)
        self.compare_method=kwargs.get('compare_method','lower')
        self.down_percent=kwargs.get('down_percent',0.7)
        self.up_percent=kwargs.get('up_percent',0.07)
        self.higher_percent=kwargs.get('higher_percent',0.05)
        self.gap_max=kwargs.get('gap_max',300)
        self.gap_points=kwargs.get('gap_points',(20,1.5,0.06))
        self.monopoly_up_percent=kwargs.get('monopoly_up_percent',0.1)
        self.monopoly_max=kwargs.get('monopoly_max',500)
        self.source_min_profit=kwargs.get('source_min_profit',2)
        self.source_profit_times=kwargs.get('source_profit_times',2.6)
        self.source_monopoly_points=kwargs.get('source_monopoly_points',(3,15))
        self.source_monopoly_points=list(self.source_monopoly_points)
        self.ajax_up_points=kwargs.get('ajax_up_points',(0.3,0.04))
        self.ajax_up_points=list(self.ajax_up_points)
        self.getprice_method=kwargs.get('getprice_method','api')
        self.up_hours=kwargs.get('up_hours',(str(i) for i in range(24)))
        if type(self.up_hours)==type(''):
            self.up_hours=self.up_hours.split(',')
        self.is_ajax_requantity=kwargs.get('is_ajax_requantity',False)
        self.is_source_requantity=kwargs.get('is_source_requantity',False)
        self.compare_methods=['equal','lower','higher']
        self.default_compare_method='lower'
    def set_product(self,product):
        self.product=product
    def set_compare_method(self,compare_method):
        if compare_method in self.compare_methods:
            self.compare_method=compare_method
        else:
            self.compare_method=self.default_compare_method
    def set_down_percent(self,down_percent):
        self.down_percent=down_percent
    def set_up_percent(self,up_percent):
        self.up_percent=up_percent
    def set_higher_percent(self,higher_percent):
        self.higher_percent=higher_percent
    def set_gap_max(self,gap_max):
        self.gap_max=gap_max
    def set_gap_points(self,gap_points):
        self.gap_points=list(gap_points)
    def set_monopoly_up_percent(self,monopoly_up_percent):
        self.monopoly_up_percent=monopoly_up_percent
    def set_monopoly_max(self,monopoly_max):
        self.monopoly_max=monopoly_max
    def set_source_min_profit(self,source_min_profit):
        self.source_min_profit=source_min_profit
    def set_source_monopoly_points(self,source_monopoly_points):
        self.source_monopoly_points=list(source_monopoly_points)
    def set_retail_option(self,usdhuilv=1):
        if is_number(self.product.inner_price):
            if is_number(self.product.outer_price) and self.product.outer_price>3:
                price_gap=self.product.inner_price-self.product.outer_price
                m,n,p=self.gap_points
                if abs(price_gap)>m or ((abs(abs(price_gap)-(m+n)/2.0))<(m-n)/2.0 and abs(price_gap)>p*self.product.inner_price):
                    self.product.reference=self.product.inner_price
                    if price_gap>0:
                        if price_gap>self.gap_max:
                            if self.compare_method=='equal' or self.compare_method=='higher':
                                self.product.margin=0.01*self.product.outer_price-price_gap
                            elif self.compare_method=='lower' and self.product.competitor_on_bottom==True:
                                self.product.margin=-0.01-price_gap
                            else:
                                self.product.margin=0-price_gap+random.randrange(0,10)/10.0
                        else:
                            self.product.margin=0-(price_gap*self.down_percent)
                    else:
                        if price_gap<-100*usdhuilv:
                            self.product.margin=0-5.01-price_gap
                        elif price_gap<-10*usdhuilv:
                            self.product.margin=random.randrange(-50,50)/50.0-(price_gap*1.01)
                        else:
                            if self.product.inner_price<15:
                                self.product.margin=1000/self.product.inner_price
                            else:
                                self.product.margin=random.randrange(-50,50)/50.0-(price_gap*1.05)
                else:
                    self.product.reference=self.product.outer_price
                    if self.compare_method=='equal':
                        if price_gap<0.001 and self.product.inner_price<self.monopoly_max and self.h in self.up_hours:
                            if self.product.inner_price<15:
                                self.product.margin=1000/self.product.inner_price
                            else:
                                self.product.margin=random.randrange(0,50)/50.0+self.product.inner_price*self.up_percent
                        else:
                            self.product.margin=0
                    elif self.compare_method=='higher':
                        if self.product.inner_price<self.monopoly_max:
                            if self.product.inner_price<15:
                                self.product.margin=1000/self.product.inner_price
                            else:
                                self.product.margin=random.randrange(0,50)/50.0+self.product.outer_price*self.higher_percent
                        else:
                            self.product.margin=0
                    elif self.compare_method=='lower' and self.product.competitor_on_bottom==True:
                        if price_gap<0.001 and self.product.inner_price<self.monopoly_max and self.h in self.up_hours:
                            if self.product.inner_price<15:
                                self.product.margin=1000/self.product.inner_price
                            else:
                                self.product.margin=random.randrange(0,50)/50.0+self.product.inner_price*self.up_percent
                        else:
                            self.product.margin=-0.01
                    else:
                        if price_gap<0.001 and self.product.inner_price<self.monopoly_max:
                            if self.product.inner_price<15:
                                self.product.margin=1000/self.product.inner_price
                            else:
                                self.product.margin=random.randrange(0,50)/50.0+self.product.inner_price*self.up_percent
                        else:
                            self.product.margin=0
            elif self.product.source_price==None:
                self.product.reference=self.product.inner_price
                if self.product.inner_price<self.monopoly_max:
                    if self.product.inner_price<15:
                        self.product.margin=1000/self.product.inner_price
                    else:
                        self.product.margin=self.product.inner_price*self.monopoly_up_percent+(400/self.product.inner_price)
                else:
                    self.product.margin=random.randrange(-50,500)/20.0
        elif is_number(self.product.outer_price):
            self.product.reference=self.product.outer_price
            self.product.margin=random.randrange(0,50)/50.0+self.product.outer_price*self.higher_percent
        else:
            self.product.reference=self.monopoly_max+random.randrange(-500,500)/10.0
            self.product.margin=0
        if is_number(self.product.margin):
            self.product.margin=self.product.margin*usdhuilv
    def set_ajax_retail_option(self,usdhuilv=1):
        m,n=self.ajax_up_points
        if is_number(self.product.outer_price) and is_number(self.product.inner_price):
            if self.product.outer_price>2.66*usdhuilv:
                price_gap=self.product.inner_price-self.product.outer_price
                self.product.reference=self.product.outer_price
                if self.base_price*usdhuilv>=self.product.outer_price:
                    # if price_gap<0.001:
                    #     self.product.margin=m + self.product.inner_price*n
                    # else:
                    self.product.margin=random.randrange(20,5000)/10.0
                elif 350*usdhuilv>self.product.outer_price>self.base_price*usdhuilv:
                    if price_gap<0.001 and self.h in self.up_hours:
                        self.product.margin=m+ self.product.inner_price*n
                    else:
                        self.product.margin=-0.01
                else:
                    self.product.reference=self.product.inner_price
                    self.product.margin=0
            else:
                self.product.reference=self.product.inner_price
                if self.product.inner_price<self.monopoly_max:
                    self.product.margin=random.randrange(20,500)/10.0
                else:
                    self.product.margin=random.randrange(-20,20)
            self.product.margin=self.product.margin*usdhuilv
        elif self.product.source_price==None:
            if self.product.inner_price!=None:
                self.product.reference=self.product.inner_price
                self.product.margin=self.product.inner_price*self.up_percent+random.randrange(10,500)/5.0
            else:
                self.product.reference=500+random.randrange(-200,200)/3.0
                self.product.margin=0
            if self.is_ajax_requantity==True:
                self.product.quantity=0
        if is_number(self.product.retail_price):
            self.product.retail_price=float(str('%.2f' % self.product.retail_price))
    def set_retail_price(self):
        if is_number(self.product.reference) and is_number(self.product.margin):
            self.product.retail_price=self.product.reference+self.product.margin
            self.product.retail_price+=0.0005
            if is_number(self.base_price) and self.product.retail_price<self.base_price:
                self.product.retail_price=self.base_price+random.randrange(0,50)/20.0
        elif is_number(self.product.inner_price):
            self.product.retail_price=self.product.inner_price
        if is_number(self.product.source_price):
            if self.product.source_price==1.0:
                self.product.source_price=random.randrange(10,200)
            t,p= self.source_monopoly_points
            if is_number(self.product.retail_price):
                if (self.product.retail_price > (self.source_profit_times+3)*self.product.source_price+25) and (self.product.retail_price-self.product.source_price>40):
                    self.product.retail_price=max(self.product.source_price*(self.source_profit_times+t)+p,self.product.source_price*(self.source_profit_times+1)+15,self.product.retail_price*0.7)
                elif self.product.retail_price <self.product.source_price*1.17+1.35+self.source_min_profit:
                    self.product.retail_price=max(self.product.source_price*2+15,self.product.source_price*(self.source_profit_times+2)+5)
            else:
                self.product.retail_price=self.product.source_price*t+p
                if type(self.product.inner_price)==type(0.1):
                    if self.product.retail_price<self.product.inner_price:
                        self.product.retail_price=max(self.product.inner_price*0.7,self.product.retail_price)
                else:
                    self.retail_price=self.monopoly_max+random.randrange(-10,10)
            if is_number(self.product.shipping_fee):
                self.product.retail_price+=self.product.shipping_fee*1.2
        elif is_number(self.product.inner_price):
            if self.product.isbn!=None and self.getprice_method=='api':
                if self.workingasins_dic.get(self.product.asin,False):
                    if self.product.inner_price<self.monopoly_max:
                        self.product.retail_price=self.product.inner_price+random.randrange(500,1000)
                    else:
                        self.product.retail_price=self.product.inner_price+random.randrange(-20,20)
                    if self.is_source_requantity==True:
                        self.product.quantity=0
                else:
                    if is_number(self.product.outer_price):
                        self.product.retail_price=(1000/self.product.outer_price)+self.product.outer_price*1.2
                    elif is_number(self.product.inner_price):
                        self.product.retail_price=(1000/self.product.inner_price)+self.product.inner_price*1.2
                    else:
                        self.product.retail_price=self.monopoly_max
        if is_number(self.product.retail_price):
            self.product.retail_price=float(str('%.2f' % self.product.retail_price))
        # if self.category=='product':
        #     pass
    def get_retail_product(self,**kwargs):
        usdhuilv=kwargs.get('usdhuilv',1.0)
        option=kwargs.get('option','normal')
        if option=='normal':
            if self.getprice_method=='ajax':
                self.set_ajax_retail_option(usdhuilv)
            else:
                self.set_retail_option(usdhuilv)
        elif option=='sourceonly':
            pass
        self.set_retail_price()
        return self.product
    def get_ajax_retail_product(self,product):
        pass
class SourceAnalysis(Analysis):
    pass
def get_products_from_invenfile(product_class,restskuasinfile_path,innerpricefile_path,outerpricefile_path,isbn2asins_dic,sourcepricefile_path,**kwargs):
    products={}
    rest_products={}
    valid_asins={}
    workingasins_dic=kwargs.get('workingasins_dic',{})
    for line in open(outerpricefile_path).readlines():
        valid_asins[line.strip('\n').split('\t')[0]]=True
    for line in open(sourcepricefile_path).readlines():
        valid_asins[isbn2asins_dic.get(line.strip('\n').split('\t')[0],'notaasin')]=True
    for asin in workingasins_dic:
        valid_asins[asin]=True
    has_outerprice=kwargs.get('has_outerprice',True)
    for line in open(restskuasinfile_path).readlines()[1:]:
        sku,asin=line.strip('\n').split('\t')[:2]
        if valid_asins.get(asin,False):
            p=product_class(sku,asin)
            products[asin]=p
    for line in open(innerpricefile_path).readlines()[1:]:
        asin,price=line.strip('\n').split('\t')
        if valid_asins.get(asin,False):
            try:
                # print(products[asin])
                products[asin].set_inner_price(price)
            except:
                pass
                # print(products[asin].outer_price)
    if has_outerprice:
        for line in open(outerpricefile_path).readlines()[1:]:
            asin,price,competitor_on_bottom=(line.strip('\n').split('\t')+['0'])[:3]
            try:
                products[asin].set_outer_price(price)
                products[asin].set_competitor_on_bottom(competitor_on_bottom)
                # print(products[asin].outer_price)
            except:
                pass
    for isbn in isbn2asins_dic:
        if valid_asins.get(isbn2asins_dic[isbn],False):
            try:
                products[isbn2asins_dic[isbn]].set_isbn(isbn)
            except:
                pass
    for line in open(sourcepricefile_path).read().splitlines()[1:]:
        isbn,price=(line.split('\t')+['',''])[:2]
        try:
            products[isbn2asins_dic[isbn]].set_isbn(isbn)
        except:
            pass
        try:
            products[isbn2asins_dic[isbn]].set_source_price(price)
        except:
            pass
    return products
def get_ajaxproducts_from_invenfile(product_class,restskuasinfile_path,innerpricefile_path,outerpricefile_path):
    products={}
    rest_products={}
    for line in open(restskuasinfile_path).read().splitlines()[1:]:
        sku,asin=line.split('\t')[:2]
        p=product_class(sku,asin)
        products[asin]=p
    for line in open(innerpricefile_path).read().splitlines()[1:]:
        asin,price=line.split('\t')
        try:
            # print(products[asin])
            products[asin].set_inner_price(price)
        except:
            pass
    for line in open(outerpricefile_path).read().splitlines()[1:]:
        asin,price,competitor_on_bottom=(line.split('\t')+['0'])[:3]
        try:
            products[asin].set_outer_price(price)
            products[asin].set_competitor_on_bottom(competitor_on_bottom)
            # print(products[asin].outer_price)
        except:
            pass
    return products
