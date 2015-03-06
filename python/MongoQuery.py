__author__ = 'jianying.wcj'
#coding=utf8
import MongoFactory
import thread

def process():
    dbConn = MongoFactory.MongoFactory()
    dbConn.connect()
    conn = dbConn.getConn()
    collection = conn.tag_per_data.tag_data
    readTags(collection,1)
    ##for i in range(1,10):
    ##    thread.start_new_thread(readTags,(collection,i))
    ##while(True):
    ##    print("tick di da...")

def readTags(collection,index):
    file = open("")
    while True:
        line = file.readline()
        if not line:
            break
        strArr = line.split("\t")[8].split(" ")
        for index in range(len(strArr)):
            queryTag = strArr[index]
            print(collection.find_one({"taglist":{ "$all":[queryTag] } }))
            #print(collection.find_one())
process()



