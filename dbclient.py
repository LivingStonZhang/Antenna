"""
Database client
"""
import time
import os
from itertools import islice
import random
import sqlite3
import pymysql
CONNECT_ERROR = 'can not connect to %s'
CONNECT_SUCCESS = 'connect to %s successfully'
CREATE_TABLE_MSG = 'created table %s'
class SqliteDbClient(object):
    """
    sqlite db client
    """
    def __init__(
            self,
            db_path=None,
            table_name=None,
    ):
        self.db_path = db_path
        self.table_name = table_name
        self.conn = None
    def connect_db(self,):
        """
        connect to database
        """
        try:
            self.conn = sqlite3.connect(self.db_path, timeout=1)
            query3 = "pragma temp_store=2;"
            query4 = "pragma journal_mode=OFF;"
            query5 = "pragma synchronous=OFF;"
            query6 = "vacuum;"
            list(map(self.conn.executescript, (query3, query4, query5, query6)))
        except:
            raise CONNECT_ERROR % self.db_path
    def close_db(self,):
        """
        close db
        """
        try:
            self.conn.close()
        except:
            pass
    def create_table_of_inventory(self,):
        """
        create table for inventory
        sku, asin, price
        asin is index
        """
        query1 = """create table %s\
        (sku varchar(30) not null unique,\
        asin varchar(10) not null unique,\
        price varchar(20) not null,\
        min_price varchar(20) not null,\
        max_price varchar(20) not null,\
        quantity int(2))""" % self.table_name
        query2 = """create index %s_sku on %s(sku)""" % (self.table_name, self.table_name)
        query3 = " pragma temp_store=2;"
        query4 = "pragma auto_vacuum=1;"
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.execute(query3)
        self.conn.execute(query4)
        self.conn.commit()
        print(CREATE_TABLE_MSG % self.table_name)
    def create_table_of_allowed_price(self,):
        """
        create table for allowed price
        sku, asin, min_price, max_price
        asin is index
        """
        query1 = """create table %s\
        (sku varchar(30) not null unique,\
        asin varchar(10) not null unique,\
        min_price varchar(20) not null,\
        max_price varchar(20) not null)""" % self.table_name
        self.conn.execute(query1)
        self.conn.commit()
    def create_table_of_zhendianbiao(self):
        """
        create table for zhendianbiao
        asin, isbn
        asin is index
        """
        query1 = """create table %s\
        (asin varchar(10) not null unique,\
        isbn varchar(10) not null,) """ % self.table_name
        query2 = """create index %s_asin on %s(asin)""" % (self.table_name, self.table_name)
        query3 = " pragma temp_store=2;"
        query4 = "pragma auto_vacuum=1;"
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.execute(query3)
        self.conn.execute(query4)
        self.conn.commit()
        print(CREATE_TABLE_MSG % self.table_name)
    def create_table_of_outer_asin_price(self):
        """
        create table for asin price
        asin, price, lowest_price, competitor_on_bottom, record_time
        asin is index
        """
        query1 = """create table %s\
        (asin varchar(10) not null unique,\
        price varchar(20) not null,\
        lowest_price varchar(20) not null,\
        competitor_on_bottom BOOLEAN(1),\
        record_time DATETIME)\
        """ % self.table_name
        query2 = """create index %s_asin on %s(asin)""" % (self.table_name, self.table_name)
        query3 = " pragma temp_store=2;"
        query4 = "pragma auto_vacuum=1;"
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.execute(query3)
        self.conn.execute(query4)
        self.conn.commit()
        print(CREATE_TABLE_MSG % self.table_name)
    def create_table_of_inner_asin_price(self):
        """
        create table for asin price
        asin, price
        """
        query1 = """create table %s\
        (asin varchar(10) not null unique,\
        price varchar(20) not null)""" % self.table_name
        query2 = """create index %s_asin on %s(asin)""" % (self.table_name, self.table_name)
        query3 = " pragma temp_store=2;"
        query4 = "pragma auto_vacuum=1;"
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.execute(query3)
        self.conn.execute(query4)
        self.conn.commit()
    def create_table_of_asin_buyboxprice(self):
        """
        create table for asin buybox_price
        isbn,price,record_time
        """
        query1 = """create table %s\
        (asin varchar(10) not null unique,\
        price varchar(20) not null,\
        record_time DATETIME)""" % self.table_name
        query2 = """create index %s_asin on %s(asin)""" % (self.table_name, self.table_name)
        query3 = " pragma temp_store=2;"
        query4 = "pragma auto_vacuum=1;"
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.execute(query3)
        self.conn.execute(query4)
        self.conn.commit()
    def create_table_of_isbn_price(self):
        """
        create table for isbn price
        isbn,price,record_time
        """
        query1 = """create table %s\
        (isbn varchar(10) not null unique,\
        price varchar(20) not null,\
        record_time DATETIME)""" % self.table_name
        query2 = """create index %s_isbn on %s(isbn)""" % (self.table_name, self.table_name)
        query3 = " pragma temp_store=2;"
        query4 = "pragma auto_vacuum=1;"
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.execute(query3)
        self.conn.execute(query4)
        self.conn.commit()
    def table_exists(self):
        """ check table exists or not"""
        query = """select name from sqlite_master \
        where type='table' and name='%s' """ % self.table_name
        result = self.conn.execute(query)
        return result.fetchone() != None
    def drop_table(self):
        """
        drop a table
        """
        query = """drop table if exists %s""" % self.table_name
        result = self.conn.executescript(query)
        return result
    def remove_price_record_by_time(self, record_time):
        """
        remove old record
        """
        delete_query = "delete from %s where record_time < '%s'" % (self.table_name, record_time)
        result = self.conn.executescript(delete_query)
        return result
    def put_sku_asin_price(self, file_path):
        """
        store sku, asin, price into table
        """
        query = """insert or replace into %s (sku,asin,price) values %s"""
        cursor = self.conn.cursor()
        with open(file_path) as sku_asin_price_file:
            sku_asin_price_file.readline()
            while True:
                next_n_lines = tuple(islice(sku_asin_price_file, 500))
                if not next_n_lines:
                    break
                sku_asin_price_data = []
                for line in next_n_lines:
                    items = line.strip('\n').split('\t')
                    if len(items) == 3:
                        sku_asin_price_data.append(str(tuple(items)))
                cursor.execute(
                    query % (
                        self.table_name,
                        ','.join(sku_asin_price_data)
                    )
                )
            self.conn.commit()
    def renew_price(self, asin_price_dic):
        """
        update price
        """
        cursor = self.conn.cursor()
        query = """replace into %s (sku,asin,price) values %s"""
        count = 1
        data = []
        for asin in asin_price_dic:
            price = asin_price_dic[asin]['price']
            sku = asin_price_dic[asin]['sku']
            try:
                price = '%.2f' % float(price)
                data.append(
                    str(
                        tuple(
                            (sku, asin, price)
                        )
                    )
                )
                count += 1
            except:
                pass
            if count % 500 == 0 and count != 0:
                cursor.execute(
                    query % (
                        self.table_name,
                        ','.join(data)
                    )
                )
                data = []
            if count % 10000 == 0:
                self.conn.commit()
                count = 0
            if count % 50000 == 0:
                self.close_db()
                self.connect_db()
        if data != []:
            cursor.execute(
                query % (
                    self.table_name,
                    ','.join(data)
                )
            )
        self.conn.commit()
    def records(self, columns):
        """
        get records of table
        """
        cursor = self.conn.cursor()
        query = "select %s from %s" % (','.join(columns), self.table_name)
        cursor.execute(query)
        return cursor
    def update_data(self, column, new_value, key, key_value):
        """
        update data by where =
        """
        query = """update %s set %s='%s' where %s = '%s'""" % (
            self.table_name,
            column,
            new_value,
            key,
            key_value,
        )
        self.conn.execute(query)
    def put_data_from_values(self, columns, values):
        """
        put data to sqlite from values
        """
        query_parts = []
        query_parts.append("""insert or replace into %s (""" % self.table_name)
        query_parts.append(','.join(columns))
        query_parts.append(') values %s')
        query = ''.join(query_parts)
        self.conn.execute(query % values)
        self.conn.commit()
    def put_data_from_io(self, columns, stringio):
        """
        put data to sqlite from stringio
        """
        query = ''.join(
            (
                "insert or replace into %s (" % self.table_name,
                ",".join(columns),
                ") values %s",
            )
        )
        title = stringio.readline()
        if '\t' in title:
            splitter = '\t'
        else:
            splitter = ','
        count = 0
        while True:
            next_n_lines = tuple(islice(stringio, 500))
            if not next_n_lines:
                break
            data = []
            for line in next_n_lines:
                items = line.strip('\n').split(splitter)
                data.append(
                    str(tuple(items))
                )
                count += 1
            self.conn.execute(query % (','.join(data)))
            if count >= 20000:
                self.conn.commit()
                self.close_db()
                self.connect_db()
                count = 0
        self.conn.commit()
    def put_data_from_tuple_generator(self, columns, gen):
        """
        put data to db from tuple generator
        """
        query = ''.join(
            (
                "insert or replace into %s (" % self.table_name,
                ",".join(columns),
                ") values %s",
            )
        )
        count = 0
        while True:
            next_n_lines = tuple(islice(gen, 500))
            if not next_n_lines:
                break
            data = []
            for line in next_n_lines:
                print(type(line), line)
                data.append(str(line))
                count += 1
            self.conn.execute(query % (','.join(data)))
            if count >= 20000:
                self.conn.commit()
                self.close_db()
                self.connect_db()
                count = 0
        self.conn.commit()
    def put_data_from_file(self, columns, file_path):
        """
        put data to sqlite from file
        """
        if os.path.isfile(file_path):
            with open(file_path) as myfile:
                self.put_data_from_io(columns, myfile)
    def init_inventory(self, columns, file_path, rate=1):
        """
        set allowed price
        """
        query = ''.join(
            (
                "insert or replace into %s (" % self.table_name,
                ",".join(columns),
                ") values %s",
            )
        )
        count = 0
        the_file = open(file_path, 'r')
        while True:
            next_n_lines = islice(the_file, 500)
            data = []
            for line in next_n_lines:
                sku, asin, price = line.strip().split('\t')
                float_price = float(price)
                min_price = "%.2f" % (3 + float_price % rate)
                max_price = "%.2f" % (float_price * 5 + 1000 * rate)
                data.append('("{0}","{1}", "{2}","{3}", "{4}")'.format(
                    sku, asin, price, min_price, max_price))
                count += 1
            if data != []:
                self.conn.execute(query % (','.join(data)))
            else:
                break
            if count >= 20000:
                self.conn.commit()
                self.close_db()
                self.connect_db()
                count = 0
        self.conn.commit()
        the_file.close()
    def put_outer_asin_price_from_file(self, price_file_path):
        """
        put asin, price, lowest_price, competitor_on_bottom, record_time
        """
        columns = ('asin', 'price', 'lowest_price', 'competitor_on_bottom', 'record_time')
        self.put_data_from_file(columns, price_file_path)
    def put_outer_asin_price_from_io(self, stringio):
        """
        put asin, price, lowest_price, competitor_on_bottom, record_time
        """
        columns = ('asin', 'price', 'lowest_price', 'competitor_on_bottom', 'record_time')
        self.put_data_from_io(columns, stringio)
    def put_asin_buyboxprice_from_file(self, price_file_path):
        """
        put asin, price, record_time
        """
        columns = ('asin', 'price', 'record_time')
        self.put_data_from_file(columns, price_file_path)
    def put_asin_buyboxprice_from_io(self, stringio):
        """
        put asin, price, record_time
        """
        columns = ('asin', 'price', 'record_time')
        self.put_data_from_io(columns, stringio)
    def put_isbn_price_from_file(self, price_file_path):
        """
        put isbn, price, record_time
        """
        columns = ('isbn', 'price', 'record_time')
        self.put_data_from_file(columns, price_file_path)
    def put_isbn_price_from_io(self, stringio):
        """
        put isbn, price, record_time
        """
        columns = ('isbn', 'price', 'record_time')
        self.put_data_from_io(columns, stringio)
    def latest_record_time(
            self,
            max_time=None,
    ):
        """
        get latest record time of price
        """
        if max_time is None:
            max_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        query = """select max(record_time) from %s \
        where record_time < '%s'""" % (self.table_name, max_time)
        cursor = self.conn.cursor()
        result = cursor.execute(query)
        if result:
            lrt = result.fetchone()
            if lrt and lrt[0] is not None:
                return lrt[0]
            else:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()-1200))
    def get_outer_asin_price(self, record_time):
        """
        get asin, price after a time from table
        """
        query1 = """select asin, price, lowest_price, competitor_on_bottom from %s \
        where record_time>'%s' """ % (self.table_name, record_time)
        cursor = self.conn.cursor()
        result = cursor.execute(query1)
        if result:
            return cursor.fetchall()
        return []
    def get_buybox_asin_price(self, record_time):
        """
        get asin, price after a time
        """
        query = """select asin, price from %s where record_time > '%s'""" % (
            self.table_name,
            record_time,
        )
        cursor = self.conn.cursor()
        result = cursor.execute(query)
        if result:
            return cursor.fetchall()
        else:
            return []
    def get_source_isbn_price(self, record_time):
        """
        get isbn, price after a time
        """
        query = """select isbn, price from %s \
        where record_time > '%s'""" % (self.table_name, record_time)
        cursor = self.conn.cursor()
        result = cursor.execute(query)
        if result:
            return cursor.fetchall()
        else:
            return []
    def get_source_isbn_price_by_isbns(self, isbns):
        """
        get isbn, price from table
        """
        isbn_prices = []
        query1 = """select price from %s where isbn = ?""" % self.table_name
        cursor = self.conn.cursor()
        for isbn in isbns:
            price = cursor.execute(query1, (isbn,)).fetchone()
            if price:
                isbn_prices.append((isbn, price[0]))
        return isbn_prices
    def get_sku_asin_price(self):
        """
        get sku, asin, price from inventory table
        """
        cursor = self.conn.cursor()
        query = """select sku, asin, price from %s""" % self.table_name
        result = cursor.execute(query)
        if result:
            return cursor.fetchall()
        else:
            return []
    def get_isbn_by_asin(self, asin):
        """
        get isbn from asin_isbn table
        """
        query = "select isbn from %s where asin = ?" % self.table_name
        isbn = self.conn.execute(query, (asin,)).fetchone()
        if len(isbn) == 1:
            return isbn
        else:
            return None
    def get_isbn_by_asins(self, asins):
        """
        get isbns from asin_isbn table
        """
        isbns = []
        query = "select isbn from %s where asin = ?" % self.table_name
        for asin in asins:
            isbn = self.conn.execute(query, asin).fetchone()
            if len(isbn) == 1:
                isbns.append(isbn)
        return isbns
class RegisterDbClient(SqliteDbClient):
    """
    store file_path, status
    help to manage conflict when two process need the same file
    """
    def __init__(
            self,
            db_path=None,
            table_name=None,
            visit_clock=None,
    ):
        super(RegisterDbClient, self).__init__(
            db_path=db_path,
            table_name=table_name,
        )
        self.visit_clock = visit_clock

    def create_table_of_register(self):
        """
        create table for register
        file_path, status
        file_path is index
        """
        while int(time.time() * 10) % 10 != self.visit_clock:
            pass
        query1 = """create table %s\
        (file_path varchar(250) not null unique,\
        status int(2))""" % self.table_name
        query2 = """create index %s_file_path on %s(file_path)""" % (
            self.table_name,
            self.table_name,
        )
        self.conn.execute(query1)
        self.conn.execute(query2)
    def register_file_path(self, file_path=None):
        """
        register file_path to database
        """
        while int(time.time() * 10) % 10 != self.visit_clock:
            pass
        end_time = time.time() + 5
        select_query = "select * from %s where file_path = '%s' and status > 0 " % (
            self.table_name,
            file_path,
        )
        insert_query = "insert or replace into %s (file_path, status) values ('%s', %d)" % (
            self.table_name,
            file_path,
            1,
        )
        cursor = self.conn.cursor()
        while time.time() < end_time:
            try:
                cursor.execute(select_query)
                break
            except:
                time.sleep(random.randrange(10)/10.0)
        result = cursor.fetchone()
        end_time = time.time() + 5
        if result is None:
            while time.time() < end_time:
                try:
                    cursor.execute(insert_query)
                    self.conn.commit()
                    print("registered %s" % file_path)
                    return True
                except:
                    time.sleep(random.randrange(10)/10.0)
            return False
        else:
            return False
    def deregister_file_path(self, file_path=None):
        """
        deregister file_path from database
        """
        while int(time.time() * 10) % 10 != self.visit_clock:
            pass
        select_query = "select * from %s where file_path = '%s' and status > 0" % (
            self.table_name,
            file_path,
        )
        update_query = "update %s set status = status -1 where file_path = '%s'" % (
            self.table_name,
            file_path,
        )
        cursor = self.conn.cursor()
        while True:
            try:
                cursor.execute(select_query)
                break
            except:
                time.sleep(random.randrange(10)/10.0)
        result = cursor.fetchone()
        if result is not None:
            while True:
                try:
                    cursor.execute(update_query)
                    self.conn.commit()
                    break
                except:
                    time.sleep(random.randrange(10)/10.0)
        print("deregistered %s" % file_path)
        return True
    def init_status(self):
        """
        init status 0
        """
        update_query = 'update %s set status = 0' % self.table_name
        cursor = self.conn.cursor()
        cursor.execute(update_query)
        self.conn.commit()
        return True
class RequestDbClient(SqliteDbClient):
    """
    store requestid
    help to download report
    """
    def create_table_of_request(self,):
        """
        create table for request_id
        """
        query1 = """create table %s\
        (request_id varchar(50) not null unique,\
        time_stamp int(11))
        """ % self.table_name
        self.conn.execute(query1)
        self.conn.commit()
    def put_request_id(self, request_id):
        """
        store request_id in database
        """
        insert_query = "insert or replace into %s (request_id, time_stamp) values('%s', %d)" % (
            self.table_name, request_id, time.time()
        )
        self.conn.execute(insert_query)
        self.conn.commit()
    def remove_old_request_id(self, keep_time):
        """
        remove old request_id from database
        """
        allow_time_stamp = time.time() - keep_time
        delete_query = "delete from %s where time_stamp < %d" % (
            self.table_name, allow_time_stamp)
        self.conn.execute(delete_query)
        self.conn.commit()
    def get_latest_request_ids(self,):
        """
        get latest request_ids
        """
        request_ids = []
        select_query = "select request_id from %s\
        where time_stamp < %d order by time_stamp desc limit 2" % (
            self.table_name, time.time() - 1200)
        cursor = self.conn.cursor()
        result = cursor.execute(select_query)
        if result:
            for record in cursor.fetchall():
                request_ids.append(record[0])
        return tuple(request_ids)
class InventoryDbClient(SqliteDbClient):
    """
    store sku, asin, hebing_status
    help to xiajia hebingdian
    """
    def create_table_of_inventory(self):
        """
        sku, asin, hebing_status
        """
        query1 = "create table %s\
        (sku varchar(50) not null unique,\
        asin varchar(10) not null,\
        hebing_status int(1) default 0)" % self.table_name
        query2 = "create index %s_sku on %s(sku)" % (
            self.table_name, self.table_name)
        self.conn.execute(query1)
        self.conn.execute(query2)
        self.conn.commit()
    def mark_hebingdian(self, sku, asin):
        """
        if asin changed, mark hebing_status 1
        """
        update_query = "update %s set hebing_status = 1\
        where sku ='%s' and asin != '%s'" % (
            self.table_name, sku, asin)
        self.conn.execute(update_query)
    def get_hebingdian_skus(self,):
        """
        get all hebingdian skus
        """
        select_query = "select sku from %s where hebing_status = 1" % self.table_name
        cursor = self.conn.cursor()
        result = cursor.execute(select_query)
        skus = []
        if result:
            for row in cursor.fetchall():
                skus.append(row[0])
        return skus
    def remove_hebingdian_skus(self, skus):
        """
        remove hebingdian skus
        """
        delete_query = "delete from %s where sku = ?" % self.table_name
        for sku in skus:
            self.conn.execute(delete_query, (sku,))
        self.conn.commit()
    def remove_xiajia_skus(self, skus):
        """
        remove xiajia skus
        """
        self.remove_hebingdian_skus(skus)
class SkuQuantityDbClient(SqliteDbClient):
    """
    store out of stock skus
    help to decide requantity or not.
    """
    def create_table_of_sku_quantity(self):
        """
        sku, quantity
        """
        query1 = "create table %s\
        (sku varchar(50) not null unique,\
        quantity int(1))" % self.table_name
        query2 = "create index %s_sku on %s(sku)" % (self.table_name, self.table_name)
        self.conn.execute(query1)
        self.conn.execute(query2)
    def put_skus(self, skus, quantity=0):
        """
        record sku and quantity
        """
        query = "insert or replace into %s (sku, quantity) values %s"
        sku_iter = iter(skus)
        cursor = self.conn.cursor()
        while True:
            next_n_skus = tuple(islice(sku_iter, 500))
            if not next_n_skus:
                break
            sku_quantity_data = []
            for sku in next_n_skus:
                sku_quantity_data.append(str((sku, quantity)))
            cursor.execute(
                query % (
                    self.table_name,
                    ','.join(sku_quantity_data),
                )
            )
        self.conn.commit()
    def remove_skus(self, skus):
        """
        if you have change the sku quantity in reprice file
        delete this record by sku
        """
        delete_query = ''.join(
            ("delete from %s where sku = " % self.table_name, "'%s'")
        )
        for sku in skus:
            self.conn.execute(delete_query % sku)
        self.conn.commit()
    def get_out_of_stock_skus(self):
        """
        get out of stock skus from db
        """
        skus = []
        select_query = "select sku from %s where quantity = 0" % self.table_name
        cursor = self.conn.cursor()
        result = cursor.execute(select_query)
        if result:
            for record in cursor.fetchall():
                skus.append(record[0])
        return skus
class MysqlDbClient(object):
    """
    mysql db client
    """
    def __init__(self, host=None, user=None, password=None, db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = None
    def connect_db(self):
        """
        connect to database
        """
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db_name,
                charset='utf8'
            )
        except:
            raise CONNECT_ERROR
    def create_table_of_inventory(self, table_name):
        """
        create table for inventory
        sku, asin, price
        asin is index
        """
        query1 = """create table %s\
        (sku varchar(30) not null primary key,\
        asin varchar(10) not null unique,\
        price varchar(20) not null,\
        quantity int(2))\
        """ % table_name
        cursor = self.conn.cursor()
        cursor.execute(query1)
        self.conn.commit()
    def create_table_of_price(self, table_name):
        """
        create table for price
        asin, price
        asin is index
        """
        query1 = """create table %s \
        (asin varchar(10) not null primary key,\
        price varchar(20) not null,\
        is_duishou bool not null,\
        record_time datetime not null)\
        """ % table_name
        cursor = self.conn.cursor()
        cursor.execute(query1)
        self.conn.commit()
    def table_exists(self, table_name):
        """ check table exists or not """
        query1 = """select * from \
        information_schema.tables \
        where table_name='%s' """ % table_name
        cursor = self.conn.cursor()
        result = cursor.execute(query1)
        if result:
            return cursor.fetchone() != None
    def put_price(self, table_name, price_file_path):
        """
        store price into table with record_time
        asin, price
        """
        record_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        query1_part1 = """replace into %s \
        (asin,price,is_duishou,record_time) values """ % table_name
        cursor = self.conn.cursor()
        with open(price_file_path) as price_file:
            price_file.readline()
            while True:
                next_n_lines = tuple(islice(price_file, 5000))
                if not next_n_lines:
                    break
                price_data = []
                for line in next_n_lines:
                    items = line.strip('\n').split('\t')
                    if len(items) == 3:
                        items.append(record_time)
                        price_data.append(str(tuple(items)))
                    if len(items) == 4:
                        price_data.append(str(tuple(items)))
                query1_part2 = ','.join(price_data)
                cursor.execute(''.join((query1_part1, query1_part2)))
            self.conn.commit()
    def get_outer_price(self, table_name, record_time):
        """
        get price after a time from table
        asin, price, is_duishou
        """
        query1 = """select asin,price,is_duishou from %s \
        where record_time > '%s' """ % (table_name, record_time)
        cursor = self.conn.cursor()
        result = cursor.execute(query1)
        if result:
            return cursor.fetchall()
        return []
    def get_source_price(self, table_name, record_time):
        """
        get all price from source table
        asin, price, is_duishou
        """
        query1 = """select asin, price, is_duishou from %s \
        where (record_time > '%s' and price='None') \
        or price != 'None' """ % (table_name, record_time)
        cursor = self.conn.cursor()
        result = cursor.execute(query1)
        if result:
            return cursor.fetchall()
        return []
