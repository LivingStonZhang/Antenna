__author__ = 'Frank Zhang'
import sqlite3
from itertools import islice
import time;

class DButil(object):
    """docstring for DButil"""

    def __init__(self, dbPath=None, tableName=None):
        super(DButil, self).__init__()
        self.conn = None
        self.dbPath = None
        self.tableName = None

    # connect to database productDetail.db. There are two table (detail and priceLevel)
    def __connectDB(self):
        try:
            self.conn = sqlite3.connect('productDetail.db')
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise

    # disconnect database
    def __disconnectDB(self):
        self.cursor.close()
        self.conn.close()

    # create Table
    def createDBTable(self):
        print('123')
        self.__connectDB()
        print(self.conn)
        try:
            self.conn.execute('''CREATE TABLE if not exists details(
				productid text, 
				title text, 
				brand text, 
				rank text, 
				product_group text,
				availability text,
				new_sellers text,
				has_reviews text,
				cankao_price text)''')
            self.conn.execute('''CREATE TABLE if not exists price_unit(
				productid text primary key,
				currentprice text,
				speedlevel text,
				lastchanged text,
				pricegap text,
				daygap text)''')
        except Exception as e:
            raise
        print('111111')
        self.__disconnectDB()

    # insert data into table details
    def insertDetails(self, details_data_file):
        self.createDBTable()
        self.__connectDB()
        with open(details_data_file) as file:
            file.readline()
            while True:
                next_n_lines = tuple(islice(file, 500))
                print("---==---" + str(next_n_lines))
                if not next_n_lines:
                    break
                data = []
                for line in next_n_lines:
                    print("-=-=-=-=-=-=-=-=-")
                    items = line.strip('\n').split('\t')
                    data.append(tuple(items))
                print('------' + str(data))
                try:
                    self.cursor.executemany('INSERT INTO details VALUES (?,?,?,?,?,?,?,?,?)', data)
                except Exception as e:
                    raise e
        self.conn.commit()
        self.__disconnectDB()
        return self.cursor.rowcount

    # insert data into table price_unit
    def insertPrice_unit(self, price_unit_data):
        self.createDBTable()
        self.__connectDB()
        with open (price_unit_data) as file:
            file.readline()
            while True:
                next_n_lines = tuple(islice(file, 500))
                print("---==---" + str(next_n_lines))
                if not next_n_lines:
                    break
                data = []
                for line in next_n_lines:
                    items = line.strip('\n').split('\t')
                    tmp_item = [items[0],items[8],'A',time.time(),'0','0']
                    data.append(tuple(tmp_item))
                try:
                    self.cursor.executemany('INSERT INTO price_unit VALUES (?,?,?,?,?,?)', data)
                except Exception as e:
                    raise e
        self.conn.commit()
        self.__disconnectDB()
        return self.cursor.rowcount

    # update TABLE details
    def updateDetails(self, details_data):
        pass

    # delete table
    def dropTable(self):
        self.__connectDB()
        try:
            self.conn.execute('''DROP TABLE details''')
            self.conn.execute('''DROP TABLE price_unit''')
        except Exception as e:
            raise e
        self.__disconnectDB()

    # get all rows from Details
    def selectDetails(self):
        self.__connectDB()
        self.cursor.execute("""SELECT * FROM details""")
        result = self.cursor.fetchall()
        return result
        self.__disconnectDB()

    # get all rows from price_unit
    def selectPriceUnit(self):
        self.__connectDB()
        self.cursor.execute("""SELECT * FROM price_unit""")
        result = self.cursor.fetchall()
        return result
        self.__disconnectDB()