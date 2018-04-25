__author__ = 'Joseph'
from mws import mws
import datetime,time
class Orders:
    def __init__(self,mws_access_key,mws_secret_key,mws_seller_id,region):
        marketplaceid = {"CA" : "A2EUQ1WTGCTBG2","US" : "ATVPDKIKX0DER","DE" : "A1PA6795UKMFR9","ES" : "A1RKKUPIHCS9HS","FR" : "A13V1IB3VIYZZH",\
                         "IN" : "A21TJRUUN4KGV","IT" : "APJ6JRA9NG5V4","UK" : "A1F83G8C2ARO7P","JP" : "A1VC38T7YXB528","CN" : "AAHKV2X7AFYLW"}
        self.mws_access_key = mws_access_key
        self.mws_secret_key = mws_secret_key
        self.mws_seller_id = mws_seller_id
        self.region = region
        self.marketplaceid = marketplaceid[self.region.upper()]
        self.order_client=mws.Orders(access_key=self.mws_access_key, secret_key=self.mws_secret_key, account_id=self.mws_seller_id)

    def get_orderids(self,created_after,created_before):
        orderids = []
        res = self.order_client.list_orders([self.marketplaceid],created_after,created_before,orderstatus=("Unshipped","PartiallyShipped"))
        orders = res.parsed
        order_list = self.get_value_from_dic(orders,['Orders','Order'])
        if order_list:
            for order in order_list:
                print(order)
                orderid = self.get_value_from_dic(order,['AmazonOrderId','value'])
                orderids.append(orderid)
                purchase_date = self.get_value_from_dic(order,['PurchaseDate','value'])
                print(purchase_date)
        return orderids
    def get_order(self,orderids):
        res = self.order_client.get_order(orderids)
        order = res.parsed
        return order
    def get_order_asin(self,orderid):
        res = self.order_client.list_order_items(orderid)
        item = res.parsed
        asin =  self.get_value_from_dic(item,['OrderItems','OrderItem','ASIN','value'])
        return asin
    def get_value_from_dic(self,d,l):
        for k in l:
            try:
                d=d[k]
            except:
                return None
        return d

