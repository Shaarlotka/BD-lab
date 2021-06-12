import psycopg2
from psycopg2 import sql
import json
from PyQt5.QtWidgets import *
import interface

class DataBase(QtWidgets.QMainWindow, interface.AppWindow):
    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.user = "user666"
        self.password = "pas..s"
        self.name = "tytylik"
        self.connectDB()
        self.connectAction.clicked.connect(self.connect)
        self.dropAction.clicked.connect(self.drop)
        self.deleteStringAction.clicked.connect(self.deleteString)
        self.deleteTableAction.clicked.connect(self.deleteTable)
        self.deleteAllAction.clicked.connect(self.deleteTables)
        self.cardsTab.itemChanged.connect(self.updateCards)
        self.shopsTab.itemChanged.connect(self.updateShops)
        self.addButton.clicked.connect(self.addDataToCards)
        self.deleteButton.clicked.connect(self.delCardByName)
        self.searchButton.clicked.connect(self.searchCard)
        self.addButton_.clicked.connect(self.addDataToShops)
        self.deleteButton_.clicked.connect(self.delShopByName)
        self.searchButton_.clicked.connect(self.searchShop)

    def connect(self):
        self.setDataToTable(self.cardsTab, self.getCards())
        self.setDataToTable(self.shopsTab, self.getShops())

    def drop(self):
        self.deteteBD()
        self.setDataToTable(self.cardsTab, None)
        self.setDataToTable(self.shopsTab, None)

    def deleteTable(self):
        if self.tabs.currentIndex() == 0:
                self.clearCards()()
                self.setDataToTable(self.cardsTab, None)
        else:
            self.clearShops()()
            self.tabledataOrders = self.db.getOrders()
            self.setDataToTable(self.shopsTab, None)

    def deleteTables(self):
        self.clearAll()
        self.setDataToTable(self.cardsTab, None)
        self.setDataToTable(self.shopsTab, None)

    def addDataToCards(self):
        if (len(self.nameEdit.text()) == 0 or len(self.setEdit.text()) == 0):
            return
        self.addCard(self.nameEdit.text(), self.setEdit.text())
        self.setDataToTable(self.cardsTab, self.getCards())

    def addDataToShops(self):
        if (len(self.setEdit_.text()) == 0 or len(self.shopEdit.text()) == 0
               or len(self.costEdit.text()) == 0):
            return
        self.addShop(self.shopEdit.text(), self.setEdit_.text(), self.costEdit.text())
        self.setDataToTable(self.shopsTab, self.getShops())

    def searchCard(self):
        if not self.keyEdit.text():
            self.setDataToTable(self.cardsTab, None)
            return
        self.setDataToTable(self.cardsTab, self.search1(self.keyEdit.text()))

    def searchShop(self):
        if not self.keyEdit_.text():
            self.setDataToTable(self.shopsTab, None)
            return
        self.setDataToTable(self.shopsTab, self.search2(self.keyEdit_.text()))

    def delCardByName(self):
        if not self.keyEdit.text():
            return
        self.deleteCardByName()
        self.setDataToTable(self.cardsTab, self.getCards())

    def delShopByName(self):
        if not self.keyEdit_.text():
            return
        self.deleteShopByName()
        self.setDataToTable(self.shopsTab, self.getShops())

    def updateCards(self, tmp):
        data = self.getCards()
        if tmp.column() == 1:
            self.updateName(data[tmp.row()]['id'], tmp.text())
        if tmp.column() == 2:
            self.updateCardSet(data[tmp.row()]['id'], tmp.text())

    def updateShops(self, tmp):
        data = self.getShops()()
        if tmp.column() == 1:
            self.updateCardSet(data[tmp.row()]['id'], tmp.text())
        if tmp.column() == 2:
            self.updateShop(data[tmp.row()]['id'], tmp.text())
        if tmp.column() == 3:
            self.updateCost(data[tmp.row()]['id'], tmp.text())

    def setData(self, table, data):
        if data is None or len(data) == 0:
            table.setRowCount(0)
            return
        table.setRowCount(len(data))
        for rownum in enumerate(data):
            table.setItem(rownum, QTableWidgetItem(str(row)))


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

    def search1(self, key):
    	self.cursor.callproc("search", (key))
    	return self.cursor.fetchone()[0]

    def search2(self, key):
    	self.cursor.callproc("searchlnShop", (key))
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
        
