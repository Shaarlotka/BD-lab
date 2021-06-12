import psycopg2
from psycopg2 import sql
import json

class DataBase:
    def __init__(self):
        super().__init__()
        self.host = "host"
        self.user = "user"
        self.password = "pass"
        self.name = "name"
        self.connectDB()

    def connectDB(self):
        self.con = pymysql.connect(self.host, self.user, self.password, self.name)
        self.cursor = self.conn.cursor()

    def addCard(self, name, set_):
    	self.cursor.callproc("add_card", (name, set_))
        
    def addShop(self, shop, set_, cost):
    	self.cursor.callproc("add_shop", (name, set_, cost))

    def clearCards(self):
    	self.cursor.callproc("clear_cards")

    def clearShops(self):
    	self.cursor.callproc("clear_shops")

    def clearAll(self):
    	self.cursor.callproc("clear_all")

    def search(self, key):
    	self.cursor.callproc("search", (key))
    	return self.cursor.fetchone()[0]

    def getCards(self):
    	self.cursor.callproc("get_cards")
    	return self.cursor.fetchone()[0]

    def getShops(self):
    	self.cursor.callproc("get_shops")
    	return self.cursor.fetchone()[0]

    def updateName(self, id, name):
    	self.cursor.callproc("update_name", (id, name))

    def updateCardSet(self, id, set_):
    	self.cursor.callproc("update_card_name", (id, set_))

    def updateShop(self, id, shop):
    	self.cursor.callproc("update_shop", (id, shop))

    def updateShopSet(self, id, set_):
    	self.cursor.callproc("update_shop_set", (id, set_))

    def updateCost(self, id, cost):
    	self.cursor.callproc("update_cost", (id, cost))

    def deleteCardByName(self, name):
    	self.cursor.callproc("delete_card_by_name", (name))

    def deleteShopByName(self, shop):
    	self.cursor.callproc("delete_shop_by_name", (shop))

    def deleteCard(self, id):
    	self.cursor.callproc("delete_card", (id))

    def deleteShop(self, id):
    	self.cursor.callproc("delete_shop", (id))

    def deteteBD(self):
        self.conn.close()
        self.con = pymysql.connect(self.host, self.user, self.password, self.name)
        cursor = con.cursor()
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(self.name)))
        conn.close()
        del self