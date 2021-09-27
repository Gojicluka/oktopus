from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore;
from PyQt5 import QtWidgets,QtGui,QtCore;
import asyncio

from binance import client;


#update
class PortfolioThread(QThread):
    output = pyqtSignal(object,object,float,int);
    tableOutput = pyqtSignal(object,str,int,object);
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent);

    def setup(self,config):
        self.start();
        self.config = config;
    def __del__(self):    
        self.wait()
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop) 
        asyncio.get_event_loop().run_until_complete(PortfolioThread.portfolioFetching(self,self.config))
    '''
    Fetch the value of the current selected symbols and calculate btc value of them
    '''
    async def portfolioFetching(self,config):
        while True:
            for clientIndex,client in enumerate(config.clients):
                symbol1AvalibleCrossMargin = 0;
                symbol2AvalibleCrossMargin = 0;
                symbol1AvalibleIsolatedMargin = 0;
                symbol2AvalibleIsolatedMargin = 0;
                balances = client.get_account()['balances'];
                config.weight +=10;
                spotTrimmedList = [];
                for i,item in enumerate(balances):
                    if config.currentSymbol1 == item['asset']:symbol1AvalibleSpot = float(item['free']);
                    if config.currentSymbol2 == item['asset']:symbol2AvalibleSpot = float(item['free']);
                    if float(item['free']) != 0: 
                        spotTrimmedList.append(item)
                        
                #calculate btc from spot account since there is no function for doing that
                gettotalbtc = PortfolioThread.getTotalBtc(client,config,spotTrimmedList);
                totalBtc = gettotalbtc[0];
                pairPrices = gettotalbtc[1];

                #Updating the weight of the requests (10 for the get_account call and 2 for the get_symbol_ticker() in the totalBtc section)
                config.weight +=2;
                #updating SPOT 
                self.tableOutput.emit(spotTrimmedList,"Spot",clientIndex,pairPrices)

                crossMarginList = client.get_margin_account();
                config.weight +=10;
                totalBtc += float(crossMarginList['totalNetAssetOfBtc'])
                crossMarginTrimmedList = [];
                for item in crossMarginList['userAssets']:
                    if float(item['free']) != 0 or float(item['locked']) != 0 or float(item['borrowed']) != 0 or float(item['interest']) != 0 or float(item['netAsset']) != 0:
                        crossMarginTrimmedList.append(item);
                        if item['asset'] == config.currentSymbol1:symbol1AvalibleCrossMargin=float(item['free']);
                        if item['asset'] == config.currentSymbol2:symbol2AvalibleCrossMargin=float(item['free']);
                    pass;
                self.tableOutput.emit(crossMarginTrimmedList,"crossmargin",clientIndex,pairPrices)

                isolatedMarginList = client.get_isolated_margin_account();
                config.weight +=10;
                totalBtc += float(isolatedMarginList['totalNetAssetOfBtc'])
                isolatedMarginTrimmedList = [];                
                for asset in isolatedMarginList['assets']:
                    item = asset['baseAsset'];
                    if float(item['free']) != 0 or float(item['locked']) != 0 or float(item['borrowed']) != 0 or float(item['interest']) != 0 or float(item['netAsset']) != 0:
                        isolatedMarginTrimmedList.append(item);
                        if item['asset'] == config.currentSymbol1:symbol1AvalibleIsolatedMargin=float(item['free']);
                        if item['asset'] == config.currentSymbol2:symbol2AvalibleIsolatedMargin=float(item['free']);
                    pass;
                self.tableOutput.emit(isolatedMarginTrimmedList,"isolatedmargin",clientIndex,pairPrices)
                
                #print(f" Cross:{float(crossMarginList['totalNetAssetOfBtc'])} Isolated:{float(isolatedMarginList['totalAssetOfBtc'])}")
                
                config.clientSpotPortfolios[clientIndex] = spotTrimmedList;     
                config.clientCrossMarginPortfolios[clientIndex] = crossMarginTrimmedList; 
                config.clientIsolatedMarginPortfolios[clientIndex] = isolatedMarginTrimmedList; 

                #print ( f"{float(crossMarginList['totalAssetOfBtc'])} {float(isolatedMarginList['totalAssetOfBtc'])}")
                #if(config.clientsymbol1AvalibleSpot[clientIndex] != float(symbol1AvalibleSpot) or config.symbol2AvalibleSpot != float(symbol2AvalibleSpot)):
                symbol1Avalible = [symbol1AvalibleSpot,symbol1AvalibleCrossMargin,symbol1AvalibleIsolatedMargin]
                symbol2Avalible = [symbol2AvalibleSpot,symbol2AvalibleCrossMargin,symbol2AvalibleIsolatedMargin]
                self.output.emit(symbol1Avalible,symbol2Avalible,totalBtc,clientIndex);
            await asyncio.sleep(5);
            
    '''
    Function for calculating total BTC value 

    @params
        -client = client whose portfolio is being calculated
        -config = main config class instance
        -list = list of all symbols which need to be calculated into the btc value
    @returns
        [0] = totalBtc of the spot account
        [1] = btc value of pairs for further calculation
    '''
    def getTotalBtc(client,config,list):
        totalBtc = 0.0;
        prices = client.get_symbol_ticker()
        valuesInBtc = {};
        for asset in list:
            symbol = asset['asset'];
            completePair = f"{symbol}BTC";
            #There is no btcusdt pair so we need to improvise and inverse the usdtbtc
            if completePair != "USDTBTC":
                pairPrice = prices[PortfolioThread.findDictionaryValue(prices,'symbol',completePair)]['price'];   
            else :
                pairPrice = 1/float(prices[PortfolioThread.findDictionaryValue(prices,'symbol',"BTCUSDT")]['price']);
            totalBtc += float(pairPrice) * float(asset['free']);
            valuesInBtc[symbol] = float(pairPrice) * float(asset['free']);
            pass;
        return [totalBtc,prices];
         #float(client.get_margin_account()['totalAssetOfBtc'])

    def findDictionaryValue(list, key, value):
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1

#makes portfolio scroll area which contains all the prices
class portfolioScrollArea():
    def __init__(self,ui,config) -> None:
        self.ui = ui;
        self.config = config;

        widget = QtWidgets.QWidget();
        vbox = QtWidgets.QVBoxLayout();
        vbox.setSpacing(0);
        vbox.setContentsMargins(0,0,0,0)

        naslov = QtWidgets.QLabel("Portolios");
        font = QtGui.QFont()
        font.setPointSize(32)
        naslov.setFont(font);
        vbox.addWidget(naslov);
        
        self.symbol1Labels = [];
        self.symbol1CrossMargin = [];
        self.symbol1IsolatedMargin = []
        self.symbol2Labels = [];
        self.symbol2CrossMargin = [];
        self.symbol2IsolatedMargin = []
        self.totalBtcLabels = [];
        #len(config.clients)
        for i in range(0,1):
            font.setPointSize(16)
            keyNameLabel = QtWidgets.QLabel(config.keyNames[0])
            keyNameLabel.setFont(font);
            keyNameLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(keyNameLabel);
            
            font.setPointSize(12)

            self.symbol1Labels.append(QtWidgets.QLabel("{} Avalible: loading"));
            self.symbol1Labels[i].setFont(font);
            self.symbol1Labels[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.symbol1Labels[i]);

            self.symbol1CrossMargin.append(QtWidgets.QLabel("Cross Margin: "));
            self.symbol1CrossMargin[i].setFont(font);
            self.symbol1CrossMargin[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.symbol1CrossMargin[i]);

            self.symbol1IsolatedMargin.append(QtWidgets.QLabel("Isolated Margin:"));
            self.symbol1IsolatedMargin[i].setFont(font);
            self.symbol1IsolatedMargin[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.symbol1IsolatedMargin[i]);

            self.symbol2Labels.append(QtWidgets.QLabel("{} Avalible: loading"));
            self.symbol2Labels[i].setFont(font);
            self.symbol2Labels[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.symbol2Labels[i]);

            self.symbol2CrossMargin.append(QtWidgets.QLabel("Cross Margin: "));
            self.symbol2CrossMargin[i].setFont(font);
            self.symbol2CrossMargin[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.symbol2CrossMargin[i]);

            self.symbol2IsolatedMargin.append(QtWidgets.QLabel("Isolated Margin:"));
            self.symbol2IsolatedMargin[i].setFont(font);
            self.symbol2IsolatedMargin[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.symbol2IsolatedMargin[i]);


            self.totalBtcLabels.append(QtWidgets.QLabel("Total BTC: loading"));
            self.totalBtcLabels[i].setFont(font);
            self.totalBtcLabels[i].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            vbox.addWidget(self.totalBtcLabels[i]);

        #prazan label koji lepo alignuje stvari
        vbox.addWidget(QtWidgets.QLabel(""),120)
        widget.setLayout(vbox);
        
        self.ui.scrollAreaPotrfolios.setWidget(widget)
    
    @staticmethod
    def updateItems(symbol1price,symbol2price,totalBtc,clientIndex,config):
        #print("xdddd");
        config.clientSymbol1Avalible[clientIndex] = symbol1price[0];
        config.clientSymbol2Avalible[clientIndex] = symbol2price[0];
        config.portfolioScrollArea.symbol1Labels[clientIndex].setText(f"{config.currentSymbol1} Avalible {symbol1price[0]}");
        config.portfolioScrollArea.symbol2Labels[clientIndex].setText(f"{config.currentSymbol2} Avalible {symbol2price[0]}");
        config.portfolioScrollArea.symbol1CrossMargin[clientIndex].setText(f"Cross Margin: {symbol1price[1]}");
        config.portfolioScrollArea.symbol2CrossMargin[clientIndex].setText(f"Cross Margin: {symbol2price[1]}");
        config.portfolioScrollArea.symbol1IsolatedMargin[clientIndex].setText(f"Isolated Margin: {symbol1price[2]}");
        config.portfolioScrollArea.symbol2IsolatedMargin[clientIndex].setText(f"Isolated Margin: {symbol2price[2]}");
        config.portfolioScrollArea.totalBtcLabels[clientIndex].setText(f"Total BTC {totalBtc}");
        pass;