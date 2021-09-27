
from PyQt5.QtWidgets import QTabWidget, QTableWidget
from PyQt5 import QtWidgets,QtCore,QtGui

class portfolioTab():
    def createTables(ui,config):
        for i in range(0,len(config.clients)):
            config.portfolioTab.append(portfolioTabSelection());
            ui.tabWidgetPortfolio.addTab(config.portfolioTab[i],config.keyNames[i]);

        
    def updateTable(data,whichTable,clientIndex,config,pairPrices):
        if whichTable.lower() == "spot":table = config.portfolioTab[clientIndex].tableSpot;
        elif whichTable.lower() == "crossmargin":table = config.portfolioTab[clientIndex].tableCrossMargin;
        elif whichTable.lower() == "isolatedmargin":table = config.portfolioTab[clientIndex].tableIsolatedMargin;

    
        for item in data:
            symbol = item['asset'];
            completePair = f"{symbol}BTC"; 
            rowIndex = portfolioTab.checkIfInTable(table,symbol);
            if completePair != "USDTBTC":
                pairPrice = pairPrices[portfolioTab.findDictionaryValue(pairPrices,'symbol',completePair)]['price'];   
            else :
                pairPrice = 1/float(pairPrices[portfolioTab.findDictionaryValue(pairPrices,'symbol',"BTCUSDT")]['price']);

            #-1 means it is not in table
            if portfolioTab.checkIfInTable(table,symbol)== -1:
                table.insertRow(table.rowCount())
                
               
                if whichTable.lower()=="spot":
                    table.setItem(table.rowCount()-1,0,QtWidgets.QTableWidgetItem(symbol));
                    table.setItem(table.rowCount()-1,1,QtWidgets.QTableWidgetItem(str(item['free'])));
                    table.setItem(table.rowCount()-1,2,QtWidgets.QTableWidgetItem(str(item['locked'])));
                    table.setItem(table.rowCount()-1,3,QtWidgets.QTableWidgetItem(str(float(pairPrice) * float(item['free']))));
                elif whichTable.lower()  == "crossmargin" or whichTable.lower()  == "isolatedmargin":
                    table.setItem(table.rowCount()-1,0,QtWidgets.QTableWidgetItem(symbol));
                    table.setItem(table.rowCount()-1,1,QtWidgets.QTableWidgetItem(str(item['netAsset'])));
                    table.setItem(table.rowCount()-1,2,QtWidgets.QTableWidgetItem(str(item['free'])));
                    table.setItem(table.rowCount()-1,3,QtWidgets.QTableWidgetItem(str(item['locked'])));
                    table.setItem(table.rowCount()-1,4,QtWidgets.QTableWidgetItem(str(item['borrowed'])));
                    table.setItem(table.rowCount()-1,5,QtWidgets.QTableWidgetItem(str(item['interest'])));
                    table.setItem(table.rowCount()-1,6,QtWidgets.QTableWidgetItem(str(float(pairPrice) * float(item['free']))));
            else:
                if whichTable.lower()=="spot":
                    table.item(rowIndex,1).setText(str(item['free']))
                    table.item(rowIndex,2).setText(str(item['locked']))
                    table.item(rowIndex,3).setText(str(float(pairPrice) * float(item['free'])))
                elif whichTable.lower()  == "crossmargin" or whichTable.lower()  == "isolatedmargin":
                    table.item(rowIndex,1).setText(str(item['netAsset']))
                    table.item(rowIndex,2).setText(str(item['free']))
                    table.item(rowIndex,3).setText(str(item['locked']))
                    table.item(rowIndex,4).setText(str(item['borrowed']))
                    table.item(rowIndex,5).setText(str(item['interest']))
                    table.item(rowIndex,6).setText(str(float(pairPrice) * float(item['free'])))
            
        pass;
    def checkIfInTable(table,symbol):
        for rowIndex in range(0,table.rowCount()):
            if table.item(rowIndex,0).text() == symbol:
                return rowIndex;
        return -1;
    
    def findDictionaryValue(list, key, value):
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1


class portfolioTabStorage():
    def __init__(self,tabWidget,spotTable,crossMarginTable,isolatedMarginTable):
        self.tabWidget = tabWidget;
        self.spotTable = spotTable;
        self.crossMarginTable = crossMarginTable;
        self.isolatedMarginTable = isolatedMarginTable;

class portfolioTabSelection(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.setGeometry(QtCore.QRect(0, 20, 931, 541))
        self.setObjectName("tabWidgetPortfolioSelection")
        self.tableSpot = portfolioTable("spot")
        self.tableSpot.setObjectName("tableSpot")
        self.addTab(self.tableSpot, "")
        self.tableCrossMargin = portfolioTable("margin")
        self.tableCrossMargin.setObjectName("tableCrossMargin")
        self.addTab(self.tableCrossMargin, "")
        self.tableIsolatedMargin = portfolioTable("margin")
        self.tableIsolatedMargin.setObjectName("tableIsolatedMargin")
        self.addTab(self.tableIsolatedMargin, "")

        self.setCurrentIndex(0)

        self.setTabText(self.indexOf(self.tableSpot),  "Spot")
        self.setTabText(self.indexOf(self.tableCrossMargin), "Cross Margin")
        self.setTabText(self.indexOf(self.tableIsolatedMargin), "Isolated margin")


class portfolioTable(QTableWidget):
    def __init__(self,type):
        QTableWidget.__init__(self);
        self.setGeometry(QtCore.QRect(0, 170, 931, 521))
        self.setObjectName("tablePortfolio")
        
        self.setRowCount(0)
       
        #self.setHorizontalHeaderItem(2,  QtWidgets.QTableWidgetItem())
        #float(item['free']) != 0 or float(item['locked']) != 0 or float(item['borrowed']) != 0 or float(item['interest']) != 0 or float(item['netAsset']) != 0:
        if type == "spot":
            self.setColumnCount(4)
            for i in range(0,self.columnCount()):
                self.setHorizontalHeaderItem(i,  QtWidgets.QTableWidgetItem());
            self.horizontalHeaderItem(0).setText("Symbol")
            self.horizontalHeaderItem(1).setText("Free")
            self.horizontalHeaderItem(2).setText("Locked")
            self.horizontalHeaderItem(3).setText("Total BTC")
            self.setColumnWidth(3,140);
        if type == "margin":
            self.setColumnCount(7)
            for i in range(0,self.columnCount()):
                self.setHorizontalHeaderItem(i,  QtWidgets.QTableWidgetItem());
            self.horizontalHeaderItem(0).setText("Symbol")
            self.horizontalHeaderItem(1).setText("netAsset")
            self.horizontalHeaderItem(2).setText("Free")
            self.horizontalHeaderItem(3).setText("Locked")
           
            self.horizontalHeaderItem(4).setText("Borrowed")
            self.horizontalHeaderItem(5).setText("Interest")
            self.horizontalHeaderItem(6).setText("Total BTC")

            self.setColumnWidth(6,140);
           
        