from configparser import ConfigParser
import os,codecs
import platform
from datetime import datetime
from DB.sqliteDB import DButil
from app.myutil.calculateCore import calculateCore as cc
import shutil

def get_path(root_dir,directory_list):
    print('root_dir----'+root_dir)
    print('directory_list-----'+str(directory_list))
    if platform.system() == 'Windows':
        print('windows')
        dir = root_dir.rstrip('/')+'/'+'/'.join(directory_list)+'/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir
    else:
        print('Linux')
        dir = root_dir.rstrip('/')+'/'+'/'.join(directory_list)+'/'
        return dir

def get_config_value(root_path,section_name,key):
    config_dir=get_path(root_path,['app','config'])
    config_path=config_dir+'config.ini'
    config=ConfigParser()
    config.read(config_path)
    return config.get(section_name,key)

def set_config_value(root_path,section_name,key,value):
    config_dir=get_path(root_path,['app','config'])
    config_path=config_dir+'config.ini'
    config=ConfigParser()
    config.read(config_path)
    config.set(section_name,key,value)
    config.write(open(config_path,'w'))

def get_source_asins_from_asindir(asindir):
    source_asins = {}
    for f in (codecs.open(asindir+i,encoding='iso-8859-1') for i in os.listdir(asindir) if '.txt' in i):
        asins=f.read().splitlines()
        for asin in asins:
            if asin:
                source_asins[asin] = True
    return source_asins

def get_asins_from_asindir(asindir):
    asins_list = []
    for f in (codecs.open(asindir+i,encoding='iso-8859-1') for i in os.listdir(asindir) if '.txt' in i):
        asins=f.read().splitlines()
        for asin in asins:
            if asin:
                asins_list.append(asin)
    asins_list.sort()
    return asins_list

def write_to_file(file_path,content):
    f_out = codecs.open(file_path,'a',encoding='utf-8')
    f_out.write(content+'\n')
    f_out.close()

def get_filter_asins_from_filter_asindir(filter_asindir):
    asinsdic={}
    for f in (codecs.open(filter_asindir+i,encoding='iso-8859-1') for i in os.listdir(filter_asindir) if '.txt' in i):
        asins=f.read().splitlines()
        for asin in asins:
            if asin:
                asinsdic[asin]=True
    return asinsdic
def get_filter_asins_from_filter_invendir(filter_invendir):
    asinsdic={}
    for f in (codecs.open(filter_invendir+i,encoding='iso-8859-1') for i in os.listdir(filter_invendir) if '.txt' in i):
        lines=f.read().splitlines()
        for line in lines:
            try:
                asin=line.split('\t')[1]
            except:
                continue
            asinsdic[asin]=True
    return asinsdic
def get_keep_asins_from_keep_asindir(keep_asindir):
    asinsdic={}
    for f in (codecs.open(keep_asindir+i,encoding='iso-8859-1') for i in os.listdir(keep_asindir) if '.txt' in i):
        asins=f.read().splitlines()
        for asin in asins:
            asinsdic[asin]=True
    return asinsdic
def get_keep_asins_from_inven_dir(keep_invendir):
    asinsdic={}
    for f in (codecs.open(keep_invendir+i,encoding='iso-8859-1') for i in os.listdir(keep_invendir) if '.txt' in i):
        lines=f.read().splitlines()
        for line in lines:
            try:
                asin=line.split('\t')[1]
            except:
                continue
            asinsdic[asin]=True
    return asinsdic
def get_products(inven_file,used_signs,filter_asins):
    products={}
    first_line=inven_file.readline()
    lines=inven_file.read().splitlines()
    for line in lines:
        sku,asin,price,quantity=line.split('\t')[:4]
        if filter_asins.get(asin,False):
            continue
        if products.get(asin,None)==None:
            products[asin]={}
        if is_used(sku,used_signs):
            products[asin]['used_price']=price
        else:
            products[asin]['new_price']=price
    return products


def get_asins(source_asins,filter_asins,type):
    asinsdic = {}
    for asin in source_asins:
        if filter_asins.get(asin,False):
            continue
        if asinsdic.get(asin)==None and type=='book' and 'B' not in asin:
            asinsdic[asin]=True
        elif asinsdic.get(asin)==None:
            asinsdic[asin]=True
    return [k for k in asinsdic.keys()]


def write_to_asinfile(file_name,asin_path,asins):
    file_name = file_name+'_'+datetime.strftime(datetime.now(),'%Y%m%d')
    file_number = 1
    count = 0
    file_path = asin_path+str(file_name)+'_'+str(file_number)+'.txt'
    print(file_path)
    f_out = open(file_path,'w')
    for asin in asins:
        if asin and 'B' not in asin:
            print(asin)
            count +=1
            f_out.write(asin+'\n')
        if count%300000==0:
            f_out.close()
            file_number +=1
            file_path = asin_path+str(file_name)+'_'+str(file_number)+'.txt'
            f_out = open(file_path,'w')
    f_out.close()


def convert_isbn(isbn):
    if len(isbn)<10:
        return (10-len(isbn))*'0'+isbn
    else:
        return isbn


# get asin from price_unit depend on speedlevel
# NEED TO CHECK EVERY TIME ! If there is no new asin need to grab. Then get the asins from price_unit table .
# Generate another txt file for grab
def DBtoFile():
    db = DButil()
    resultFromDB = db.selectPriceUnit()
    deleteFile("src/source_asins/US/")
    file = open("src/source_asins/US/source_asin.txt","w")
    resultAsin = cc.getAsinByCalculate(resultFromDB)
    for item in resultAsin:
        file.write(item+'\n')

# delete file in the folder
def deleteFile(folderName):
    shutil.rmtree(folderName)
    os.mkdir(folderName)

# check is there any ASIN in remote Database still need to grab
# return TRUE or FALSE
def checkRemoteAsinLeft():
    pass

# get new asin to grab from remote database
def getAsinRemote():
        pass
