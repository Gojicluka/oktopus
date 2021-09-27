
from buySellTextBoxes import BuySellTextBoxes
from portfolio import PortfolioThread, portfolioScrollArea
from PyQt5.QtWidgets import QLabel, QMainWindow;
from PyQt5 import QtGui, QtWidgets;
from PyQt5 import QtCore;
from PyQt5.QtGui import QDoubleValidator
from datetime import datetime;

#Custom modules
from ui import Ui_MainWindow;
from openOrders import openOrders;
from openOrders import openOrdersThread;
from config import Config;
from PairSymbolList import PairSymbolList;
from buySell import BuySell
from fetchPrice import  fetchPriceAlt;

from portfolioTable import portfolioTab
from buySellTextBoxes import BuySellTextBoxes;
'''
Class for the main window which initiates the whole application
'''
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.ui = Ui_MainWindow();
        self.ui.setupUi(self);
        self.config = Config(self.ui);
        self.setWindowTitle('Binance trading app');        
        
        self.buySellTextBoxes = BuySellTextBoxes(self.ui,self.config);
        self.declareMessageBox();
        
        BuySell.setup(self.ui,self.config);
        portfolioTab.createTables(self.ui,self.config);
        openOrders.createTables(self.ui,self.config);
        self.signalsInit();
        self.threadInit();
    
    '''
    Initiates all the threads which are needed for this application
    
    @Threads
        -openOrdersThread = fetches all the open orders for all the clients
        -fetchPriceThread = fetches the prices via web socket
    '''
    def threadInit(self):
        #open order thread setup
        self.openOrdersThread = openOrdersThread();
        self.openOrdersThread.setup(self.config);
        self.openOrdersThread.output[object,int].connect(lambda podaci,tableIndex: openOrders.processOpenOrders(self.ui,self.config,podaci,tableIndex));
        self.openOrdersThread.deleteRow[object,int].connect(lambda podatak,tableIndex: openOrders.deleteRow(self.ui,self.config,podatak,tableIndex));
        self.openOrdersThread.filledChanged[object,int].connect(lambda podaci,tableIndex: openOrders.filledChanged(self.ui,self.config,podaci,tableIndex));
        #fetch price thread setup
        self.fetchPriceThread = fetchPriceAlt();
        self.fetchPriceThread.setup(self.config);
        self.fetchPriceThread.output[str].connect(lambda podaci: self.updatePairPrice(podaci));

        self.portfolioThread = PortfolioThread();
        self.portfolioThread.setup(self.config);
        self.portfolioThread.output[object,object,float,int].connect(
            lambda symbol1price,symbol2price,totalBtc,clientIndex:
                 portfolioScrollArea.updateItems(symbol1price,symbol2price,totalBtc,clientIndex,self.config));
        self.portfolioThread.tableOutput[object,str,int,object].connect(
            lambda lista,whichTable,clientIndex,pairPrices:
                 portfolioTab.updateTable(lista,whichTable,clientIndex,self.config,pairPrices));
                
    def updatePairPrice(self,podaci):
        self.ui.labelPairPrice.setText(podaci)
        BuySellTextBoxes.updateBuySellTextBoxes(self.buySellTextBoxes,self.ui,self.config);
        pass;
    #Initialises all the signals needed
    def signalsInit(self):
        self.ui.buttonPairList.clicked.connect(lambda:self.createPairListForm());
        #self.ui.buttonSymbolList.clicked.connect(lambda:self.createSymbolListForm());
        self.ui.comboBoxMode.currentIndexChanged.connect(self.updateMode);

    '''
    Updates which mode is displayed 

    @Modes:
        -Limit
        -Market
        -Stop Limit
    '''
    def updateMode(self):
        self.ui.labelModeLimit.setText(self.ui.comboBoxMode.currentText())
        self.ui.labelModeMarket.setText(self.ui.comboBoxMode.currentText())
        self.ui.LabelModeStopLimit.setText(self.ui.comboBoxMode.currentText())

    #Creating the new form
    def createPairListForm(self):
        self.pairListForm = PairSymbolList(self.config,self.ui,"pair");
    def createSymbolListForm(self):
        self.symbolListForm = PairSymbolList(self.config,self.ui,"symbol");
    def declareMessageBox(self):
        self.ui.messageBox = QtWidgets.QMessageBox()
        self.ui.messageBox .setIcon(QtWidgets.QMessageBox.Critical)
        self.ui.messageBox .setText("")
        self.ui.messageBox .setInformativeText("")
        self.ui.messageBox .setWindowTitle("Error")
        #self.ui.messageBox .setDetailedText("The details are as follows:")
        self.ui.messageBox .setStandardButtons(QtWidgets.QMessageBox.Ok)
        #self.ui.messageBox .buttonClicked.connect(self.ui.messageBox btn)
    def createErrorBox(ui,text,info):
        ui.messageBox.setText(text)
        ui.messageBox.setInformativeText(info)
        ui.messageBox.show();
    