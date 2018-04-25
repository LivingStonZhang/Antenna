__author__ = 'can'
import os,time,re,random
import numpy as np
import threading

class Getprice(object):
    def __init__(self,product_client,market_place_id,asins,n_outerpricefile_path,u_outerpricefile_path,d_seller_ratings,**kwargs):
        self.product_client=product_client
        self.market_place_id=market_place_id
        self.all_asins=asins
        self.n_outerpricefile_path=n_outerpricefile_path
        self.u_outerpricefile_path=u_outerpricefile_path
        self.d_seller_ratings=d_seller_ratings
        self.try_limit=kwargs.get('try_limit',3)
        self.wait_limit=kwargs.get('wait_limit',4)
        self.thread_capicity=kwargs.get('thread_capicity',3)
        self.getnew=kwargs.get('getnew',True)
        self.getprice_option=kwargs.get('getprice_option','both')
        self.min_feedback_count=kwargs.get('min_feedback_count',100)
        self.min_rating=kwargs.get('min_rating',89)
        self.max_ships_days=kwargs.get('max_ships_days',7)
        self.only_domestic=kwargs.get('only_domestic',False)
        self.price_kind=kwargs.get('price_kind','listing_price')
        self.record=0
        self.noprice_asins=asins
        self.n_prices={}
        self.u_prices={}
        self.need_getnewprice_asins=[]
    def get_value_from_dic(self,d,l):
        for k in l:
            try:
                d=d[k]
            except:
                return None
        return d
    def is_duishou(self,feedback,d_seller_ratings):
        if any(feedback):
            feedback_count,rating=feedback
        else:
            return False
        for d_seller in d_seller_ratings:
            if rating == d_seller['rating'] and abs(feedback_count-d_seller['feedback_count'])<80:
                return True
        return False
    def get_sellers(self,lowestproducts):
        condition2value={'New':0,'Mint':1,'VeryGood':2,'Good':3,'Acceptable':4}
        n_sellers=[]
        u_sellers=[]
        better_n_sellers=[]
        better_u_sellers=[]
        if type(lowestproducts)!=type(list()):
            lowestproducts=[lowestproducts,]
        for p in lowestproducts:
            try:
                subcondition=condition2value[p['Qualifiers']['ItemSubcondition']['value']]
            except:
                continue
            if self.price_kind=='landed_price':
                price=self.get_value_from_dic(p,['Price','LandedPrice','Amount','value'])
            elif self.price_kind=='listing_price':
                price=self.get_value_from_dic(p,['Price','ListingPrice','Amount','value'])
            else:
                price=self.get_value_from_dic(p,['Price','ListingPrice','Amount','value'])
            try:
                feedback_count=int(self.get_value_from_dic(p,['SellerFeedbackCount','value']))
                rating=int(self.get_value_from_dic(p,['Qualifiers','SellerPositiveFeedbackRating','value']).split('-')[0])
            except:
                feedback_count=0
                rating=0
            ships_domestically=self.get_value_from_dic(p,['Qualifiers','ShipsDomestically','value']).lower()
            ships_time=self.get_value_from_dic(p,['Qualifiers','ShippingTime','Max','value']).lower()
            if 'days' in ships_time:
                ships_days=ships_time.split('days')[0].strip()
                ships_days=int(re.sub('[^\d]','',ships_days.split('-')[-1]))
            elif 'day' in ships_time:
                ships_days=1
            elif 'hours' in ships_time:
                ships_days=2
            else:
                ships_days=30
            if int(rating)>self.min_rating and int(feedback_count)>self.min_feedback_count:
                if self.only_domestic==True and ships_domestically=='false':
                    continue
                if ships_days>self.max_ships_days:
                    continue
                if subcondition==0:
                    n_sellers.append([price,feedback_count,rating])
                elif subcondition!=4:
                    u_sellers.append([price,feedback_count,rating])
            if int(rating)>94 and int(feedback_count)>self.min_feedback_count:
                if self.only_domestic==True and ships_domestically=='false':
                    continue
                if ships_days>self.max_ships_days:
                    continue
                if subcondition==0:
                    better_n_sellers.append([price,feedback_count,rating])
                elif subcondition!=4:
                    better_u_sellers.append([price,feedback_count,rating])
            if len(better_n_sellers)>2 or (len(n_sellers)-len(better_n_sellers)<2 and len(better_n_sellers)>0):
                n_sellers=better_n_sellers
            if len(better_u_sellers)>2 or (len(u_sellers)-len(better_u_sellers)<2 and len(better_u_sellers)>0):
                u_sellers=better_u_sellers
        return {'n_sellers':n_sellers,'u_sellers':u_sellers}
    def get_likely_sellers(self,sellers):
        sellers=np.array(sellers,float)
        if len(sellers)<3:
            return sellers
        else:
            if len(sellers)==3:
                mean=sum(sellers[0:-1,0])/len(sellers[0:-1,0])
            elif len(sellers)==4:
                mean=sum(sellers[0:3,0])/len(sellers[0:3,0])
            else:
                mean=sum(sellers[1:4,0])/len(sellers[1:4,0])
            tmp_sellers=[sellers[i] for i in range(len(sellers)) if abs(sellers[i][0]/mean - 1.1)<0.5]
            if len(tmp_sellers)!=0:
                sellers=np.array(tmp_sellers)
            # sellers_total=len(sellers)
            # if sellers_total>2:
            #     kl=sellers[-1,0]-sellers[0,0]+0.00001
            #     print(kl)
            #     k=[(sellers[i,0] - sellers[i-1,0])/kl for i in range(1,sellers_total)]
            #     if max(k)>0.9:
            #         position=0
            #         for i in k:
            #             if i>0.9:
            #                 break
            #             position+=1
            #         if 2*position+3>sellers_total:
            #             if sellers[position+1]-sellers[position]<2 or sellers[position+1]/sellers[position]<1.2:
            #                 sellers=sellers[0:position+2]
            #             else:
            #                 sellers=sellers[0:position+1]
            #         else:
            #             if sellers[position+1]-sellers[position]<2 or sellers[position+1]/sellers[position]<1.2:
            #                 sellers=sellers[position:]
            #             else:
            #                 sellers=sellers[position+1:]
            return sellers
    def get_likely_seller(self,sellers):
        if len(sellers):
            sellers=np.array(sellers,float)
            j=0
            current_price=sellers[0,0]
            for i in range(len(sellers)):
                if sellers[i,0]-0.01*j>=current_price:
                    current_price=sellers[i,0]-0.01*j
                    sellers[i,0]=current_price
                    j+=1
            minprice=min(sellers[:,0])
            meanprice=np.mean(sellers[:,0])
            if minprice/meanprice >0.995:
                return sellers[0]
            else:
                return [meanprice,0,0]
        else:
            return []
    def chunks(self,l,n):
        for i in range(0, len(l), n):
            yield l[i:i+n]
    def waitthread(self,threads):
        while True:
            hasthread=0
            for t in threads:
                if t.isAlive()!=False:
                    hasthread=1
                    break
            if hasthread!=0:
                time.sleep(0.1)
            else:
                break
    def get_results_by_asins(self,asins,**kwargs):
        condition=kwargs.get('condition','Any')
        res=[]
        results=[]
        try_times=0
        wait_time=0.5
        while try_times<self.try_limit:
            wait_time+=try_times*0.5
            try:
                res=self.product_client.get_lowest_offer_listings_for_asin(self.market_place_id,asins,condition)
                results=res.parsed
                print(len(results))
                break
            except:
                time.sleep(wait_time)
                try_times+=1
        try:
            if len(results)==0:
                # print('add to noprice_asins',asins)
                self.noprice_asins+=asins
        except:
            self.noprice_asins+=asins
        return results
    def get_prices_from_results(self,results):
        for result in results:
            self.record+=1
            try:
                asin=result['ASIN']['value']
                lowestproducts=result['Product']['LowestOfferListings']['LowestOfferListing']
            except:
                continue
            all_sellers=self.get_sellers(lowestproducts)
            n_sellers=all_sellers['n_sellers']
            u_sellers=all_sellers['u_sellers']
            if len(n_sellers)==0 and any(u_sellers):
                self.need_getnewprice_asins.append(asin)
            n_sellers,u_sellers=self.get_likely_sellers(n_sellers),self.get_likely_sellers(u_sellers)
            n_seller,u_seller=self.get_likely_seller(n_sellers),self.get_likely_seller(u_sellers)
            if any(n_seller):
                self.n_prices[asin]=[n_seller[0],self.is_duishou(n_seller[1:],self.d_seller_ratings)]
            if any(u_seller):
                self.u_prices[asin]=[u_seller[0],self.is_duishou(u_seller[1:],self.d_seller_ratings)]
    def get_prices_by_asins(self,asins,**kwargs):
        results=self.get_results_by_asins(asins,**kwargs)
        self.get_prices_from_results(results)
    def get_all_prices(self):
        threads=[]
        thread_count=0
        btry_times=0
        line_count=len(self.noprice_asins)
        self.wait_limit+=int(line_count/1000)
        if self.getprice_option=='both':
            condition='Any'
        elif self.getprice_option=='new':
            condition='New'
        while len(self.noprice_asins)>0 and btry_times<10:
            if len(self.noprice_asins)<100:
                btry_times+=1
            asins_list=self.chunks(list(set(self.noprice_asins)),20)
            self.noprice_asins=[]
            for asins in asins_list:
                thread_count+=1
                t=threading.Thread(target=self.get_prices_by_asins,args=(asins,),kwargs={'condition':condition})
                threads.append(t)
                try:
                    t.start()
                except:
                    threads.pop()
                if thread_count%self.thread_capicity==0:
                    time.sleep(0.5)
                if thread_count%50==0:
                    time.sleep(10)
            self.waitthread(threads)
            print('there are %d asins left' % len(self.noprice_asins))
        if any(self.need_getnewprice_asins) and self.getnew==True:
            line_count+=len(self.need_getnewprice_asins)
            print('I am going to get new prices!!!')
            self.noprice_asins=self.need_getnewprice_asins
            condition='New'
            btry_times=0
            while len(self.noprice_asins)>0 and btry_times<10:
                if len(self.noprice_asins)<100:
                    btry_times+=1
                asins_list=self.chunks(list(set(self.noprice_asins)),20)
                self.noprice_asins=[]
                for asins in asins_list:
                    thread_count+=1
                    t=threading.Thread(target=self.get_prices_by_asins,args=(asins,),kwargs={'condition':condition})
                    threads.append(t)
                    try:
                        t.start()
                    except:
                        threads.pop()
                    if thread_count%self.thread_capicity==0:
                        time.sleep(0.5)
                    if thread_count%50==0:
                        time.sleep(10)
                self.waitthread(threads)
                print('there are %d new asins left' % len(self.noprice_asins))
        s=[]
        while True:
            s.append(self.record)
            print(self.record)
            time.sleep(1)
            if line_count==self.record:
                break
            if len(s)>self.wait_limit:
                if s[-1]==s[0-self.wait_limit]:
                    break
                else:
                    print(line_count,self.record)
        print('end')
        time.sleep(3)
        with open(self.n_outerpricefile_path,'w') as f:
            f.write('asin\tprice\tduishouzhandi\n')
            for asin in self.n_prices:
                if self.n_prices[asin][1]==True:
                    duishouzhandi='1'
                else:
                    duishouzhandi='0'
                if self.n_prices[asin][0]!=1.0:
                    f.write("%s\t%.2f\t%s\n" % (asin,self.n_prices[asin][0],duishouzhandi))
                else:
                    f.write("%s\t%.2f\t%s\n" % (asin,random.randrange(5,200),duishouzhandi))
        with open(self.u_outerpricefile_path,'w') as f:
            f.write("asin\tprice\tduishouzhandi\n")
            u_prices=self.n_prices
            u_prices.update(self.u_prices)
            for asin in u_prices:
                if u_prices[asin][1]==True:
                    duishouzhandi='1'
                else:
                    duishouzhandi='0'
                if u_prices[asin][0]!=1.0:
                    f.write("%s\t%.2f\t%s\n" % (asin,u_prices[asin][0],duishouzhandi))
                else:
                    f.write("%s\t%.2f\t%s\n" % (asin,random.randrange(5,200),duishouzhandi))
                    
