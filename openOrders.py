from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QTableWidget;
import json;
import asyncio;
from datetime import datetime;


'''
Static called mainly being called by the mainWindow class, which contains methods for manipulating the open orders tables
'''
class openOrders():
    '''
    Creates table for every client that is logged in at the moment

    @params
        -ui = pointer to the main ui 
        -config = pointer to the class that stores all the data that is needed 
    '''
    def createTables(ui,config):
        try:
            for i in range(0,len(config.clients)):
                config.openOrdersTables.append(openOrdersTable());
                ui.tabWidgetOpenOrders.addTab(config.openOrdersTables[i],config.keyNames[i]);
                #create signal for each time cell is changed (for cancelign the orders)
                config.openOrdersTables[i].cellChanged.connect(lambda row,column:openOrders.cellChanged(row,column,ui,config,i));
        except Exception as ex:
            ui.console.append(f"Exception thrown at OpenOrders.createTables() : \n{ex}")
    '''
    Proccessing the data from orders in to the table that are sent by the thread to this function

    @params 
        -ui = pointer to the main ui 
        -config = pointer to the class that stores all the data that is needed
        -podaci = data being sent from the thread that needs to be placed in to the table
        -tableIndex = index of the table which current iteration of the thread is checking
    '''
    def processOpenOrders(ui,config,podaci,tableIndex,accountType):
        
        table = config.openOrdersTables[tableIndex];
        for podatak in podaci:
            try:
                table.insertRow(table.rowCount())
                #Moguca promena, na drugaciji nacin da se postavljaju podaci
                table.setItem(table.rowCount()-1,0,QtWidgets.QTableWidgetItem(podatak['symbol']));
                table.setItem(table.rowCount()-1,1,QtWidgets.QTableWidgetItem(podatak['type']));
                table.setItem(table.rowCount()-1,2,QtWidgets.QTableWidgetItem(podatak['price']));
                table.setItem(table.rowCount()-1,3,QtWidgets.QTableWidgetItem(podatak['origQty']));
                filled = float(podatak['executedQty'])/(float(podatak['origQty'])/100) if float(podatak['executedQty']) else 0;
                table.setItem(table.rowCount()-1,4,QtWidgets.QTableWidgetItem(f"{filled} %"));
                table.setItem(table.rowCount()-1,5,QtWidgets.QTableWidgetItem(str(float(podatak['price'])*float(podatak['origQty']))));
                table.setItem(table.rowCount()-1,6,QtWidgets.QTableWidgetItem("" if float(podatak['stopPrice'])==0 else podatak['stopPrice']));
                table.setItem(table.rowCount()-1,7,
                QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(int(float(podatak['time'])/1000)))));
                table.setItem(table.rowCount()-1,8,QtWidgets.QTableWidgetItem("0"));
                table.setItem(table.rowCount()-1,9,QtWidgets.QTableWidgetItem(str(podatak['orderId'])));
                table.setItem(table.rowCount()-1,10,QtWidgets.QTableWidgetItem(str(accountType)));
                if accountType == "spot":
                    color = QtGui.QColor(77, 210, 219)
                if accountType == "margin":
                    if podatak['isIsolated'] == "TRUE":
                        color = QtGui.QColor(217, 201, 28)
                    else:
                        color = QtGui.QColor(73, 184, 48)
                else:
                    color = QtGui.QColor(77, 210, 219)
                openOrders.setColortoRow(table,table.rowCount()-1,color,ui)
            except Exception as ex:
                ui.console.append(f"Exception thrown at OpenOrders.proccessOpenOrders() : \n{ex}")
    '''
    Function being called by the pyqt singla when ExecutedQty of the order is changed

    @details
        Function for each data given finds the table row index which contains it and when it does it updates the filled %
        in the table

    @params
        -ui = pointer to the main ui 
        -config = pointer to the class that stores all the data that is needed
        -podaci = data being sent from the thread that needs to be updated
        -tableIndex = index of the table which current iteration of the thread is checking
    '''
    def filledChanged(ui,config,podaci,tableIndex):
        try:
            table = config.openOrdersTables[tableIndex];
            for i in range(0,len(podaci)):
                rowIndexFound = -1;
                for j in range(table.rowCount()):
                    if table.item(j,9).text() == str(podaci[i]['orderId']):
                        rowIndexFound = j;
                        break;
                if rowIndexFound!=-1:
                    filled = float(podaci[i]['executedQty'])/(float(podaci[i]['origQty'])/100) if float(podaci[i]['executedQty']) else 0;
                    table.item(rowIndexFound,4).setText(f"{filled} %")
                    ui.console.append(f"updated filled for {podaci[i]['orderId']}")
        except Exception as ex:
            ui.console.append(f"Exception thrown at OpenOrders.filledChanged() : \n{ex}")
    '''
    Function being called by the pyqt singla when the order is no longer present(that means executed or canceled)

    @params
        -ui = pointer to the main ui 
        -config = pointer to the class that stores all the data that is needed
        -podatak = data being sent from the thread that needs to be deleted from the table
        -tableIndex = index of the table which current iteration of the thread is checking
    '''
    def deleteRow(ui,config,podatak,tableIndex):
        try:
            table = config.openOrdersTables[tableIndex];
            #moramo manuelno da proveravamo
            for i in range(0,table.rowCount()):
                if str(podatak['orderId']) == table.item(i,9).text():
                    table.removeRow(i);
                    ui.console.append(f"{podatak['orderId']} obrisan :)");
                    break;
        except Exception as ex:
            ui.console.append(f"Exception thrown at OpenOrders.deleteRow() : \n{ex}")
    '''
    Coloring the given row of the table

    @params
        -table = the table which needs the row colored
        -rowIndex 
        -color
    '''
    def setColortoRow(table, rowIndex, color,ui):
        try:
            for j in range(table.columnCount()):
                table.item(rowIndex, j).setBackground(color)
        except Exception as ex:
            ui.console.append(f"Exception thrown at OpenOrders.setColorRow() : \n{ex}")

    '''
    Function being called by the pyqt singla when the cell is changed that checks whether the user canceled the order

    @params
        -row = table row
        -column = table column
        -ui = pointer to the main ui 
        -config = pointer to the class that stores all the data that is needed
        -tableIndex = index of the table which current iteration of the thread is checking
    '''
    def cellChanged(row,column,ui,config,tableIndex):
        try:
            table = config.openOrdersTables[tableIndex];
            if column == 8 and table.item(row,column).text() =="1":
                print("ORDER CANCELED");
                if table.item(row,10).text() == "spot":
                    result = config.clients[tableIndex].cancel_order(
                        symbol=table.item(row,0).text(),
                        orderId=table.item(row,9).text())
                elif table.item(row,10).text() == "margin":
                    result = config.clients[tableIndex].cancel_margin_order(
                        symbol=table.item(row,0).text(),
                        orderId=table.item(row,9).text())
                ui.console.append("Order cancel request send, confirmation message should be there soon")
        except Exception as ex:
            ui.console.append(f"Exception thrown at OpenOrders.cellChanged() : \n{ex}")

'''
Thread for continuously fetching open orders from binance api
'''
class openOrdersThread(QtCore.QThread):
    output = QtCore.pyqtSignal(object,int,str);
    deleteRow = QtCore.pyqtSignal(object,int)
    filledChanged = QtCore.pyqtSignal(object,int);

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent);
    
    def setup(self,config,ui):
        self.start();
        self.config = config;
        self.ui = ui;
    def __del__(self):    
        self.wait()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(openOrdersThread.openOrdersFetching(self))
    '''
    Asynchronous fetching of the orders of all clients from binance

    @params 
        -self
    '''
    async def openOrdersFetching(self):
        trenutnaTabela=[];
        while True:
            try: 
                for tableIndex in range(0,len(self.config.clients)):
                    for pair in self.config.pairs:
                        #ovde se kao loaduje par
                        # with open('openOrdersExample.json') as f:
                        #     podaci = json.load(f)
                        # podaci = [podatak for podatak in podaci if podatak['symbol'] == pair]
                        podaci = self.config.clients[tableIndex].get_open_orders(symbol=pair)
                        self.orderProccesing(trenutnaTabela,tableIndex,podaci,pair,"spot");
                        self.config.weight+=3;
                        await asyncio.sleep(1);
                    marginOrders = self.config.clients[tableIndex].get_open_margin_orders();
                    self.orderProccesing(trenutnaTabela,tableIndex,marginOrders,pair,"margin");
                    self.config.weight+=10;
                    await asyncio.sleep(1);
            except Exception as ex:
                self.ui.console.append(f"Exception thrown at OpenOrdersThread.openOrdersFetching() : \n{ex}")
                
    def orderProccesing(self,trenutnaTabela,tableIndex,podaci,pair,type):
        try:
            self.checkForExecutedData(trenutnaTabela,tableIndex,podaci,pair);
            self.checkForFilledChanges(trenutnaTabela,tableIndex,podaci);
            #Checking if the data that is displayed is changed
            podaci = [podatak for podatak in podaci if not any(d['orderId'] == podatak['orderId'] for d in trenutnaTabela)]
            #Adding new data to the table
            if len(podaci)>0:
                trenutnaTabela+=podaci;
                self.output.emit(podaci,tableIndex,type)
        except Exception as ex:
            self.ui.console.append(f"Exception thrown at OpenOrdersThread.orderProccesing() : \n{ex}")

    '''
    Checking if an order has been canceled or executed

    @params
        -self
        -trenutnaTabela = the current list of all the data present
        -tableIndex = index of the table which current iteration is checking
        -podaci = data that we retrieved in the current iteration
    '''
    def checkForExecutedData(self,trenutnaTabela,tableIndex,podaci,pair):
        try: 
            for vecPostojaciPodatak in trenutnaTabela:
                if vecPostojaciPodatak["symbol"] == pair:
                    if not any(podatak['orderId'] == vecPostojaciPodatak['orderId'] for podatak in podaci):
                        trenutnaTabela.remove(vecPostojaciPodatak);
                        self.deleteRow.emit(vecPostojaciPodatak,tableIndex);
                        self.ui.console.append(f"Order canceled or executed {vecPostojaciPodatak['symbol']} {vecPostojaciPodatak['orderId']} at {datetime.now()}")
        except Exception as ex:
            self.ui.console.append(f"Exception thrown at OpenOrdersThread.checkForExecutedData() : \n{ex}")
    '''
    Checking if the executed quantity is changed in data

    @params
        -self
        -trenutnaTabela = the current list of all the data present
        -tableIndex = index of the table which current iteration is checking
        -podaci = data that we retrieved in the current iteration
    '''
    def checkForFilledChanges(self,trenutnaTabela,tableIndex,podaci):
        #Making the list of all the data that has its ExecutedQty changed
        try:
            filledChangedList = [podatak for podatak in podaci 
                if any(podatakIzTrenutneTabele['orderId'] == podatak['orderId'] and 
                podatakIzTrenutneTabele['executedQty'] != podatak['executedQty'] for podatakIzTrenutneTabele in trenutnaTabela)] 
            
            if any(filledChangedList):
                #Changing the executed quantity in the current list of the table in the memory
                for filledChangedPodatak in filledChangedList:
                    foundIndex = openOrdersThread.findDictionaryValue(trenutnaTabela,'orderId',filledChangedPodatak['orderId']);
                    trenutnaTabela[foundIndex]['executedQty'] = filledChangedPodatak['executedQty'];
                #Emiting the signal to change the table
                self.filledChanged.emit(filledChangedList,tableIndex);
        except Exception as ex:
            self.ui.console.append(f"Exception thrown at OpenOrdersThread.checkForFilledChanges() : \n{ex}")
    '''
    Finds the key of the value from the dictionary

    @params 
        -list = the list of dictionaries
        -key = key which we are looking for 
        -value = value which we are looking for
    @returns
        -int index of the value we are lookign for 
        -int (-1) if we don't find the value
    '''
    def findDictionaryValue(list, key, value):
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1

#qt table for tailor made for open orders
class openOrdersTable(QTableWidget):
    def __init__(self, parent = None):
        QTableWidget.__init__(self, parent);
        self.setGeometry(QtCore.QRect(30, -10, 931, 551))
        self.setObjectName("openOrdersTable")
        self.setColumnCount(11)
        self.setRowCount(0)
        for i in range(0,self.columnCount()):
            self.setHorizontalHeaderItem(i,  QtWidgets.QTableWidgetItem());
        self.horizontalHeaderItem(0).setText("Pair")
        self.horizontalHeaderItem(1).setText("Type")
        self.horizontalHeaderItem(2).setText("Price")
        self.horizontalHeaderItem(3).setText("Amount")
        self.horizontalHeaderItem(4).setText("Filled (%)")
        self.horizontalHeaderItem(5).setText("Total")
        self.horizontalHeaderItem(6).setText("Trigger conditions")
        self.horizontalHeaderItem(7).setText("Date")
        self.horizontalHeaderItem(8).setText("Cancel")
        self.horizontalHeaderItem(9).setText("orderId")
        self.horizontalHeaderItem(10).setText("accountType")

        self.setColumnWidth(7,120);
        self.setColumnWidth(5,140);