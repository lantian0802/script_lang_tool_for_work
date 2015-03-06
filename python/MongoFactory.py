__author__ = 'steven'
import pymongo

class MongoFactory:

    conn = None
    servers = "mongodb://ip:port"

    def connect(self):
        self.conn = pymongo.Connection(self.servers)

    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn