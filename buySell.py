import MainWindow;
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QWindow;
from PyQt5.QtWidgets import QApplication,QMainWindow;
from binance.client import Client;
import configparser;
import json;
from PyQt5.QtGui import QDoubleValidator
#Custom modules
from ui import Ui_MainWindow;
from forms.window2 import Ui_Form as window2;
from binance.enums import *

'''
Main class for the functionality of the buy selling methods
'''
class BuySell():
    '''
    Initializses all the methods needed
    '''
    @staticmethod
    def setup(ui,config):
        BuySell.comboBoxSetup(ui,config);
        BuySell.updateSymbols(ui,config)
        config.currentPair = ui.comboBoxPair.currentText();
        ui.comboBoxPair.currentIndexChanged.connect(lambda : BuySell.updateSymbols(ui,config))
        BuySell.sliderSetup(ui,config);

        Limit.setup(ui,config);
        Market.setup(ui,config);
        StopLimit.setup(ui,config);
    #Initialises combobox
    def comboBoxSetup(ui,config):
        ui.comboBoxPair.clear();
        lista = config.pairs;
        ui.comboBoxPair.addItems(lista);
    
   

    #Updates symbols when combobox selected item is changed or the new pair is added
    def updateSymbols(ui,config):
        try: 
            pair = ui.comboBoxPair.currentText();
            #find the matching symbols in a pair
            matchingSymbols = [s for s in config.symbols if s in pair];  
            #change the order of the mathing pairs for displaying
            if len(matchingSymbols)>1:
                if pair.find(matchingSymbols[0]) != 0:
                    pom = matchingSymbols[0]
                    matchingSymbols[0] = matchingSymbols[1];
                    matchingSymbols[1] = pom;    
                config.currentSymbol1 = matchingSymbols[0];
                config.currentSymbol2 = matchingSymbols[1];
                config.currentPair = ui.comboBoxPair.currentText();
                BuySell.updateSymbolLabels(ui,matchingSymbols[0],matchingSymbols[1],config);
            else:
                MainWindow.MainWindow.createErrorBox(ui,"The pair doesn't exist","Please delete the pair.")
        except Exception as ex:
            ui.console.append(f"Exception thrown at BuySell.updateSymbols() : \n{ex}")
    
    #initialises functions for the sliders
    def sliderSetup(ui,config):
        #change the % of the slider
        ui.horizontalSliderLimit.valueChanged.connect(
            lambda: BuySell.sliderLimitUpdate(ui,config))
        ui.horizontalSliderMarketBuy.valueChanged.connect(
            lambda: BuySell.sliderUpdate(ui.lineEditMarketBuySlider,ui.horizontalSliderMarketBuy,"marketBuy",config))
        ui.horizontalSliderMarketSell.valueChanged.connect(
            lambda: BuySell.sliderUpdate(ui.lineEditMarketSellSlider,ui.horizontalSliderMarketSell,"marketSell",config))
        ui.horizontalSliderStopLimit.valueChanged.connect(
            lambda: BuySell.sliderStopLimitUpdate(ui,config))
        
        #change the slider value based on textBox
        ui.lineEditMarketBuySlider.textChanged.connect(lambda: 
            ui.horizontalSliderMarketBuy.setValue(int(ui.lineEditMarketBuySlider.text())) 
            if 0<=(int(ui.lineEditMarketBuySlider.text()) if ui.lineEditMarketBuySlider.text()!="" else -1)<=100 else 0)
        ui.lineEditMarketSellSlider.textChanged.connect(lambda: 
            ui.horizontalSliderMarketSell.setValue(int(ui.lineEditMarketSellSlider.text())) 
            if 0<=(int(ui.lineEditMarketSellSlider.text())if ui.lineEditMarketSellSlider.text()!="" else -1)<=100 else 0)

        ui.lineEditLimitSlider.textChanged.connect(lambda: 
            ui.horizontalSliderLimit.setValue(int(ui.lineEditLimitSlider.text())) 
            if 0<=(int(ui.lineEditLimitSlider.text())if ui.lineEditLimitSlider.text()!="" else -1)<=100 else 0)
        ui.lineEditLimitSlider.textChanged.connect(lambda: 
            ui.horizontalSliderLimit.setValue(int(ui.lineEditLimitSlider.text())) 
            if 0<=(int(ui.lineEditLimitSlider.text())if ui.lineEditLimitSlider.text()!="" else -1)<=100 else 0)
    def sliderLimitUpdate(ui,config):
        ui.lineEditLimitSlider.setText(str(ui.horizontalSliderLimit.value()))
        if ui.lineEditLimitPrice.text() != "0" and ui.lineEditLimitPrice.text() != "" and ui.horizontalSliderLimit.value() != "0":
             ui.lineEditLimitAmount.setText(str(
                 ((float(ui.horizontalSliderLimit.value())/100)*config.clientSymbol2Avalible[0])/float(ui.lineEditLimitPrice.text())))

    def sliderStopLimitUpdate(ui,config):
        ui.lineEditStopLimitSlider.setText(str(ui.horizontalSliderStopLimit.value()))
        if ui.lineEditStopLimitLimit.text() != "0" and ui.lineEditStopLimitLimit.text() != "" and ui.horizontalSliderStopLimit.value() != "0":
             ui.lineEditStopLimitAmount.setText(str(
                 ((float(ui.horizontalSliderStopLimit.value())/100)*config.clientSymbol2Avalible[0])/float(ui.lineEditStopLimitLimit.text())))

    
    #update the mode of the slider
    def sliderUpdate(textBox,slider,mode,config):
        textBox.setText(str(slider.value()));

        #unfortunately python doesnt support pointers to a string so we need to do this this way
        if mode == "marketBuy":config.marketBuyMode="slider";
        elif mode=="marketSell":config.marketSellMode = "slider";

    #change the symbol name after the updating of the combobox
    def updateSymbolLabels(ui,symbol1,symbol2,config):
        ui.labelLimitPriceSymbol.setText(symbol2)
        ui.labelLimitAmountSymbol.setText(symbol1)
        ui.labelLimitTotalSymbol.setText(symbol2);
        ui.labelMarketAmountSymbolBuy1.setText(symbol1);
        ui.labelMarketAmountSymbolBuy2.setText(symbol2);
        ui.labelMarketAmountSymbolSell1.setText(symbol1);
        ui.labelMarketAmountSymbolSell2.setText(symbol2);
        ui.labelStopLimitStopSymbol.setText(symbol2);
        ui.labelStopLimitPriceSymbol.setText(symbol2);
        ui.labelStopLimitAmountSymbol.setText(symbol1);
        ui.labelStopLimitTotalSymbol.setText(symbol2);

        for i in range(0,len(config.portfolioScrollArea.symbol1Labels)):
            config.portfolioScrollArea.symbol1Labels[i].setText(f"{symbol1} Avalible: loading");
            config.portfolioScrollArea.symbol2Labels[i].setText(f"{symbol2} Avalible: loading");
    
    def findDictionaryValue(list, key, value):
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1
    
    def calculateBuy(ui,config,clientIndex,percent,finalPrice,amount):   
        try:
            amountBeingSpent=0;
            if ui.comboBoxAccountMode.currentText()== "Spot":
                if float(config.clientSymbol2Avalible[clientIndex]) != 0:
                    if clientIndex == 0:percent = (finalPrice/float(config.clientSymbol2Avalible[clientIndex]))*100; 
                    else: 
                        amountBeingSpent = ((float(config.clientSymbol2Avalible[clientIndex])/100)*percent);
                        amount = amountBeingSpent/config.currentPairPrice;
                else: 
                    if clientIndex == 0: percent = 0;
                    else: amountBeingSpent = 0;

            elif ui.comboBoxAccountMode.currentText()== "Cross":
                indexOfAsset = BuySell.findDictionaryValue(config.clientCrossMarginPortfolios[clientIndex],"asset",config.currentSymbol2);
                if indexOfAsset == -1: 
                    if clientIndex == 0: percent = 0;
                    else: amountBeingSpent = 0;
                else: 
                    if clientIndex == 0: 
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0 and finalPrice!=0:
                            percent = (finalPrice/float(config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free']))*100;
                        else : percent = 0;
                    else:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0:
                            amountBeingSpent = ((float(config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'])/100)*percent);
                            amount = amountBeingSpent/config.currentPairPrice;
                        else: 
                            amountBeingSpent = 0
                            amount = 0

            elif ui.comboBoxAccountMode.currentText()== "Isolated":
                indexOfAsset = BuySell.findDictionaryValue(config.clientIsolatedMarginPortfolios[clientIndex],"asset",config.currentSymbol2);
                if indexOfAsset == -1: 
                    if clientIndex == 0: percent = 0;
                    else: amountBeingSpent = 0;
                else: 
                    if clientIndex == 0:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0 and finalPrice!=0:
                            percent = (finalPrice/float(config.clientIsolatedMarginPortfolios[clientIndex][indexOfAsset]['free']))*100;
                        else:
                            percent = 0;
                    else:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0:
                            amountBeingSpent = ((float(config.clientIsolatedMarginPortfolios[clientIndex][indexOfAsset]['free'])/100)*percent);
                            amount = amountBeingSpent/config.currentPairPrice;
                        else:
                            amountBeingSpent = 0
                            amount = 0
            
            return [percent,amountBeingSpent,amount];
        except Exception as ex:
            ui.console.append(f"Exception thrown at BuySell.calculateBuy() : \n{ex}")
            return ["error","error","error"]

    def calculateSell(ui,config,clientIndex,percent,finalPrice,amount):
        try:
            amountBeingSold =0;
            if ui.comboBoxAccountMode.currentText()== "Spot":
                if float(config.clientSymbol1Avalible[clientIndex]) != 0:
                    if clientIndex == 0:percent = (amount/float(config.clientSymbol1Avalible[clientIndex]))*100;
                    else: amountBeingSold = (float(config.clientSymbol1Avalible[clientIndex])/100)*percent;
                else: 
                    if clientIndex == 0: percent = 0;
                    else: amountBeingSold = 0;

                
            elif ui.comboBoxAccountMode.currentText()== "Cross":
                indexOfAsset = BuySell.findDictionaryValue(config.clientCrossMarginPortfolios[clientIndex],"asset",config.currentSymbol1);
                if indexOfAsset == -1: 
                    if clientIndex == 0: percent = 0;
                    else: amountBeingSold = 0;
                else: 
                    if clientIndex == 0:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0 and amount!=0:
                            percent = (amount/float(config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free']))*100;
                        else: percent  = 0;
                    else:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0:
                            amountBeingSold = (float(config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'])/100)*percent;
                        else: 
                            amountBeingSold = 0;
            elif ui.comboBoxAccountMode.currentText()== "Isolated":
                indexOfAsset = BuySell.findDictionaryValue(config.clientIsolatedMarginPortfolios[clientIndex],"asset",config.currentSymbol1);
                if indexOfAsset == -1: 
                    if clientIndex == 0: percent = 0;
                    else: amountBeingSold = 0;
                else: 
                    if clientIndex == 0:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0 and amount !=0:
                            percent = (amount/float(config.clientIsolatedMarginPortfolios[clientIndex][indexOfAsset]['free']))*100;
                        else: 
                            percent = 0;
                    else:
                        if config.clientCrossMarginPortfolios[clientIndex][indexOfAsset]['free'] != 0: 
                            amountBeingSold = (float(config.clientIsolatedMarginPortfolios[clientIndex][indexOfAsset]['free'])/100)*percent;
                        else: amountBeingSold = 0;
            
            return [percent,amountBeingSold];
        except Exception as ex:
            ui.console.append(f"Exception thrown at BuySell.calculateSell() : \n{ex}")
            return ["error","error"]
#Class for items from tab widgets
class Limit():
    def setup(ui,config):
        ui.buttonLimitBuy.clicked.connect(lambda:Limit.order(ui,config,"buy"));
        ui.buttonLimitSell.clicked.connect(lambda:Limit.order(ui,config,"sell"));

    def order(ui,config,action):
        try: 
            percent = 0;
            price = float(ui.lineEditLimitPrice.text());
            amount = float(ui.lineEditLimitAmount.text());
            finalPrice = price * amount;
            for clientIndex,client in  enumerate(config.clients):
                if config.userAccountsScrollArea.checkBoxes[clientIndex].isChecked() == True:
                    if action == "buy":
                        #percent = (finalPrice/float(config.clientSymbol2Avalible[0]))*100
                        calculateBuy = BuySell.calculateBuy(ui,config,clientIndex,percent,finalPrice,amount)
                        if calculateBuy[0] != "error":
                            percent = calculateBuy[0];
                            amountBeingSpent = calculateBuy[1];
                            amount = calculateBuy[2];
                            
                            if clientIndex ==0: amount = float(ui.lineEditLimitAmount.text())

                            if 0<percent<=100:  
                                params = {"symbol":config.currentPair,"side": SIDE_BUY,"type":ORDER_TYPE_LIMIT,"timeInForce":TIME_IN_FORCE_GTC,
                                    "quantity":amount,"price":price};

                                if  ui.comboBoxAccountMode.currentText()== "Isolated":
                                    params['isIsolated'] = "TRUE";

                                if False:
                                    if  ui.comboBoxAccountMode.currentText()== "Spot":order = client.create_order(**params)
                                    elif  ui.comboBoxAccountMode.currentText()== "Cross" or ui.comboBoxAccountMode.currentText()== "Isolated":
                                            order = client.create_margin_order(**params)
                                    if "clientOrderId" in order:
                                        ui.console.append("Succesfull order");
                                    else:
                                        ui.console.append("Error i think?");
                            else:
                                MainWindow.MainWindow.createErrorBox(ui,"An error has occured",f"You don't have enough {config.currentSymbol2}")
                                break; 
                    if action == "sell":
                        #percent = (finalPrice/float(config.clientSymbol2Avalible[0]))*100
                        calculateSell = BuySell.calculateSell(ui,config,clientIndex,percent,finalPrice,amount)
                        if calculateSell[0] !="error":
                            percent = calculateSell[0];
                            amountBeingSold = calculateSell[1];
                            
                            if clientIndex ==0: amountBeingSold = float(ui.lineEditLimitAmount.text())

                            if 0<percent<=100:  
                                params = {"symbol":config.currentPair,"side": SIDE_SELL,"type":ORDER_TYPE_LIMIT,"timeInForce":TIME_IN_FORCE_GTC,
                                    "quantity":amount,"price":price};
                                if  ui.comboBoxAccountMode.currentText()== "Isolated":
                                    params['isIsolated'] = "TRUE";
                                if False:
                                    if  ui.comboBoxAccountMode.currentText()== "Spot":order = client.create_order(**params)
                                    elif  ui.comboBoxAccountMode.currentText()== "Cross" or ui.comboBoxAccountMode.currentText()== "Isolated":
                                        order = client.create_margin_order(**params)
                                    
                                    if "clientOrderId" in order:
                                        ui.console.append("Succesfull order");
                                    else:
                                        ui.console.append("Error i think?");
                            else:
                                MainWindow.MainWindow.createErrorBox(ui,"An error has occured",f"You don't have enough {config.currentSymbol2}")
                                break; 
        except Exception as ex:
            ui.console.append(f"Exception thrown at Limit.order() : \n{ex}")


class Market():
    def setup(ui,config):
        ui.buttonMarketBuy.clicked.connect(lambda:Market.order(ui,config,"buy"));
        ui.buttonMarketSell.clicked.connect(lambda:Market.order(ui,config,"sell"));

    def order(ui,config,action):
        try:
            percent = 0;
        
            for clientIndex,client in  enumerate(config.clients):
                if config.userAccountsScrollArea.checkBoxes[clientIndex].isChecked() == True:
                    if action == "buy":
                        if ui.lineEditMarketAmountBuy.text() =="" or ui.lineEditMarketAmountBuyTotal.text()=="":
                            MainWindow.MainWindow.createErrorBox(ui,"Empty fields!","")
                        else:
                            amount = float(ui.lineEditMarketAmountBuy.text());
                            finalPrice = float(config.currentPairPrice)*amount;
                            
                            calculateBuy = BuySell.calculateBuy(ui,config,clientIndex,percent,finalPrice,amount)
                            if calculateBuy[0]!="error":
                                percent = calculateBuy[0];
                                amountBeingSpent = calculateBuy[1];
                                amount = calculateBuy[2];

                                if clientIndex ==0: amountBeingSpent = float(ui.lineEditMarketAmountBuyTotal.text())
                                print(percent);
                                #check if the percentage is good
                                if 0<percent<=100:  
                                    if  ui.comboBoxAccountMode.currentText()== "Spot":params = {"symbol":config.currentPair};
                                    elif  ui.comboBoxAccountMode.currentText()== "Cross":
                                        params = {"symbol":config.currentPair,"side":SIDE_BUY,"type":ORDER_TYPE_MARKET}
                                    elif  ui.comboBoxAccountMode.currentText()== "Isolated":
                                        params = {"symbol":config.currentPair,"side":SIDE_BUY,"type":ORDER_TYPE_MARKET,"isIsolated":"TRUE"}                
                                    # if config.marketBuyMode =="total":
                                    # else: params['quantity']=amount;
                                    params['quoteOrderQty']=amountBeingSpent;
                                    if False:
                                        if  ui.comboBoxAccountMode.currentText()== "Spot":order = client.order_market_buy(**params)
                                        elif  ui.comboBoxAccountMode.currentText()== "Cross" or ui.comboBoxAccountMode.currentText()== "Isolated":
                                            order = client.create_margin_order(**params)
                                        if "clientOrderId" in order:
                                            ui.console.append("Succesfull order");
                                        else:
                                            ui.console.append("Error i think?");
                                else:
                                    MainWindow.MainWindow.createErrorBox(ui,"An error has occured",f"You don't have enough {config.currentSymbol2}")
                                    break;  
        
                    if action == "sell":
                        if ui.lineEditMarketAmountSell.text() =="" or ui.lineEditMarketAmountSellTotal.text()=="":
                            MainWindow.MainWindow.createErrorBox(ui,"Empty fields!","")
                        else:
                            amount = float(ui.lineEditMarketAmountSell.text());
                            finalPrice = float(config.currentPairPrice)*amount;
                            
                            calculateSell = BuySell.calculateSell(ui,config,clientIndex,percent,finalPrice,amount)
                            if calculateSell[0] != "error":
                                percent = calculateSell[0];
                                amountBeingSold = calculateSell[1];


                                if clientIndex ==0: amountBeingSold = float(ui.lineEditMarketAmountSell.text())

                                if 0<percent<=100:
                                    if False:
                                        if  ui.comboBoxAccountMode.currentText()== "Spot":
                                            params = {"symbol":config.currentPair,"quantity":amountBeingSold};
                                            order = client.order_market_sell(**params)
                                        elif  ui.comboBoxAccountMode.currentText()== "Cross": 
                                            params = {"symbol":config.currentPair,"side":SIDE_SELL,"type":ORDER_TYPE_MARKET,"quantity":amountBeingSold};
                                            order = client.create_margin_order(**params)
                                        elif  ui.comboBoxAccountMode.currentText()== "Isolated": 
                                            params = {"symbol":config.currentPair,"side":SIDE_SELL,"type":ORDER_TYPE_MARKET,"quantity":amountBeingSold,"isIsolated":"True"};
                                            order = client.create_margin_order(**params)

                                        if "clientOrderId" in order:
                                            ui.console.append("Succesfull order");
                                        else:
                                            ui.console.append("Error i think?");
                                else:
                                    MainWindow.MainWindow.createErrorBox(ui,"An error has occured",f"You don't have enough {config.currentSymbol1}")
                                    break;
        except Exception as ex:
            ui.console.append(f"Exception thrown at Market.order() : \n{ex}")
        

class StopLimit():
    def setup(ui,config):
        ui.buttonStopLimitBuy.clicked.connect(lambda:StopLimit.order(ui,config,"buy"));
        ui.buttonStopLimitSell.clicked.connect(lambda:StopLimit.order(ui,config,"sell"));

    def order(ui,config,action):
        try:
            percent = 0;
            stop = float(ui.lineEditStopLimitStop.text())
            price = float(ui.lineEditStopLimitPrice.text());
            amount = float(ui.lineEditStopLimitAmount.text());
            finalPrice = price * amount;
            for clientIndex,client in  enumerate(config.clients):
                if config.userAccountsScrollArea.checkBoxes[clientIndex].isChecked() == True:
                    if action == "buy":
                        #percent = (finalPrice/float(config.clientSymbol2Avalible[0]))*100
                        calculateBuy = BuySell.calculateBuy(ui,config,clientIndex,percent,finalPrice,amount)
                        if calculateBuy[0] == "error":
                            percent = calculateBuy[0];
                            amountBeingSpent = calculateBuy[1];
                            amount = calculateBuy[2];
                            
                            if clientIndex ==0: amount = float(ui.lineEditStopLimitAmount.text())

                            if 0<percent<=100:  
                                params = {"symbol":config.currentPair,"side": SIDE_BUY,"type":ORDER_TYPE_STOP_LOSS_LIMIT,"timeInForce":TIME_IN_FORCE_GTC,
                                    "quantity":amount,"price":price,"stopPrice":stop};

                                if  ui.comboBoxAccountMode.currentText()== "Isolated":
                                    params['isIsolated'] = "TRUE";

                                if False:
                                    if  ui.comboBoxAccountMode.currentText()== "Spot":order = client.create_order(**params)
                                    elif  ui.comboBoxAccountMode.currentText()== "Cross" or ui.comboBoxAccountMode.currentText()== "Isolated":
                                            order = client.create_margin_order(**params)
                                    if "clientOrderId" in order:
                                        ui.console.append("Succesfull order");
                                    else:
                                        ui.console.append("Error i think?");
                            else:
                                MainWindow.MainWindow.createErrorBox(ui,"An error has occured",f"You don't have enough {config.currentSymbol2}")
                                break; 
                    if action == "sell":
                        #percent = (finalPrice/float(config.clientSymbol2Avalible[0]))*100
                        calculateSell = BuySell.calculateSell(ui,config,clientIndex,percent,finalPrice,amount)
                        if calculateSell != "error":
                            percent = calculateSell[0];
                            amountBeingSold = calculateSell[1];
                            
                            if clientIndex ==0: amountBeingSold = float(ui.lineEditStopLimitAmount.text())

                            if 0<percent<=100:  
                                params = {"symbol":config.currentPair,"side": SIDE_SELL,"type":ORDER_TYPE_STOP_LOSS_LIMIT,"timeInForce":TIME_IN_FORCE_GTC,
                                    "quantity":amount,"price":price,"stopPrice":stop};

                                if  ui.comboBoxAccountMode.currentText()== "Isolated":
                                    params['isIsolated'] = "TRUE";
                                if False:
                                    if  ui.comboBoxAccountMode.currentText()== "Spot":order = client.create_order(**params)
                                    elif  ui.comboBoxAccountMode.currentText()== "Cross" or ui.comboBoxAccountMode.currentText()== "Isolated":
                                            order = client.create_margin_order(**params)
                                    
                                    if "clientOrderId" in order:
                                        ui.console.append("Succesfull order");
                                    else:
                                        ui.console.append("Error i think?");
                            else:
                                MainWindow.MainWindow.createErrorBox(ui,"An error has occured",f"You don't have enough {config.currentSymbol2}")
                                break; 
        except Exception as ex:
            ui.console.append(f"Exception thrown at StopLimit.order() : \n{ex}")
