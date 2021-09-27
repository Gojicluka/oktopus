from PyQt5.QtGui import QDoubleValidator

'''
Methods for the textBoxes for buy sell methods
'''
class BuySellTextBoxes():
    def __init__(self,ui,config) :
        self.writeLock = False;
        self.setValidators(ui);
        self.setupBuySellTextBoxesEvents(ui,config);
    #Enabling only doubles to be written in lineEdits
    def setValidators(self,ui):
        ui.lineEditLimitPrice.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditLimitPrice));
        ui.lineEditLimitAmount.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditLimitAmount));
        ui.lineEditLimitTotal.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditLimitTotal));

        ui.lineEditMarketAmountBuy.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditMarketAmountBuy));
        ui.lineEditMarketAmountSell.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditMarketAmountSell));
        ui.lineEditMarketAmountBuyTotal.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditMarketAmountBuyTotal));
        ui.lineEditMarketAmountSellTotal.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditMarketAmountSellTotal));

        ui.lineEditStopLimitLimit.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditStopLimitLimit));
        ui.lineEditStopLimitAmount.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditStopLimitAmount));
        ui.lineEditStopLimitStop.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditStopLimitStop));
        ui.lineEditStopLimitTotal.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditStopLimitTotal));

        ui.lineEditLimitSlider.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditLimitSlider));
        ui.lineEditMarketBuySlider.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditMarketBuySlider));
        ui.lineEditMarketSellSlider.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditMarketSellSlider));
        ui.lineEditStopLimitSlider.setValidator(QDoubleValidator(0, 100, 30, ui.lineEditStopLimitSlider));
    
    #Setup events for textBoxes
    def setupBuySellTextBoxesEvents(self,ui,config):

        ui.lineEditMarketAmountBuy.textChanged.connect(
            lambda:self.marketTextChanged(ui.lineEditMarketAmountBuyTotal,ui.lineEditMarketAmountBuy,config,"amountBuy"));
        ui.lineEditMarketAmountBuyTotal.textChanged.connect(
            lambda:self.marketTextChanged(ui.lineEditMarketAmountBuyTotal,ui.lineEditMarketAmountBuy,config,"totalBuy"));
        ui.lineEditMarketAmountSell.textChanged.connect(
            lambda:self.marketTextChanged(ui.lineEditMarketAmountSellTotal,ui.lineEditMarketAmountSell,config,"amountSell"));
        ui.lineEditMarketAmountSellTotal.textChanged.connect(
            lambda:self.marketTextChanged(ui.lineEditMarketAmountSellTotal,ui.lineEditMarketAmountSell,config,"totalSell"));

        ui.lineEditLimitPrice.textChanged.connect(lambda: self.updateElement(ui,config,"limitPrice"));
        ui.lineEditLimitAmount.textChanged.connect(lambda: self.updateElement(ui,config,"limitAmount"));
        ui.lineEditLimitTotal.textChanged.connect(lambda: self.updateElement(ui,config,"limitTotal"));

        ui.lineEditStopLimitLimit.textChanged.connect(lambda: self.updateElement(ui,config,"stopLimitLimit"));
        ui.lineEditStopLimitAmount.textChanged.connect(lambda: self.updateElement(ui,config,"stopLimitAmount"));
        ui.lineEditStopLimitTotal.textChanged.connect(lambda: self.updateElement(ui,config,"stopLimitTotal"))
    
    def marketTextChanged(self,textBoxTotal,textBoxAmount,config,type):
        if (type ==  "amountBuy" or type == "amountSell") and self.writeLock!=True:
            self.writeLock = True;
            textBoxTotal.setText(str(
                    (float(textBoxAmount.text()) if textBoxAmount.text() !="" else 0)*float(config.currentPairPrice)))
            self.writeLock = False;
            if type == "amountBuy": config.marketBuyMode = "amount";
            if type == "amountSell": config.marketSellMode = "amount";
        
        if (type ==  "totalBuy" or type=="totalSell") and self.writeLock != True:
            self.writeLock = True;
            if textBoxTotal.text() !="":  
                textBoxAmount.setText(str(
                    (float(textBoxTotal.text()))/(float(config.currentPairPrice))))
            else: textBoxAmount.setText(str(0));
            self.writeLock = False;
            if type == "totalBuy": config.marketBuyMode = "total";
            if type == "totalSell": config.marketSellMode = "total";
    
    def updateElement(self,ui,config,action):
        #There is no switch in python soooo we need to do it like this
        if self.writeLock==False:
            self.writeLock= True;
            if action == "limitTotal":           
                ui.lineEditLimitAmount.setText(str((float(ui.lineEditLimitTotal.text())/float(ui.lineEditLimitPrice.text()))
                    if  ui.lineEditLimitPrice.text()!= "" and ui.lineEditLimitPrice.text()!=0 else ""))               
            elif action == "limitAmount":          
                ui.lineEditLimitTotal.setText(str(
                    (float(ui.lineEditLimitPrice.text()) if ui.lineEditLimitPrice.text() != "" else 0) *
                    float(ui.lineEditLimitAmount.text()) if ui.lineEditLimitAmount.text() !="" else 0));          
            elif action == "limitPrice":   
                ui.lineEditLimitTotal.setText(str(
                    (float(ui.lineEditLimitPrice.text()) if ui.lineEditLimitPrice.text() != "" else 0) *
                    float(ui.lineEditLimitAmount.text()) if ui.lineEditLimitAmount.text() !="" else 0)); 
            elif action == "stopLimitLimit":
                ui.lineEditStopLimitTotal.setText(str(
                    (float(ui.lineEditStopLimitLimit.text()) if ui.lineEditStopLimitLimit.text() != "" else 0)*
                    (float(ui.lineEditStopLimitAmount.text()) if ui.lineEditStopLimitAmount.text() != "" else 0)))
            elif action == "stopLimitAmount":
                ui.lineEditStopLimitTotal.setText(str(
                    (float(ui.lineEditStopLimitLimit.text()) if ui.lineEditStopLimitLimit.text() != "" else 0)*
                    (float(ui.lineEditStopLimitAmount.text()) if ui.lineEditStopLimitAmount.text() != "" else 0)))
            elif action == "stopLimitTotal":
                ui.lineEditStopLimitAmount.setText(str((float(ui.lineEditStopLimitTotal.text())/float(ui.lineEditStopLimitLimit.text()))
                    if  ui.lineEditStopLimitLimit.text()!= "" and ui.lineEditStopLimitLimit.text()!=0 else ""))
            self.writeLock= False;
        pass;
    #Updating the total text box
    def updateBuySellTextBoxes(self,ui,config):
        self.writeLock= True;
        if ui.lineEditMarketAmountBuy.text() != "" and float(ui.lineEditMarketAmountBuy.text()) != 0 and config.marketBuyMode=="amount":       
            ui.lineEditMarketAmountBuyTotal.setText(str(float(ui.lineEditMarketAmountBuy.text())*config.currentPairPrice)) 
        elif ui.lineEditMarketAmountBuyTotal.text() != "" and float(ui.lineEditMarketAmountBuyTotal.text()) != 0 and config.marketBuyMode=="total":
            ui.lineEditMarketAmountBuy.setText(str(
                (float(ui.lineEditMarketAmountBuyTotal.text()) )/config.currentPairPrice))
        elif config.marketBuyMode=="slider":
            if ui.comboBoxAccountMode.currentText()== "Spot":   symbolAvalible = config.clientSymbol2Avalible[0]
            elif ui.comboBoxAccountMode.currentText()== "Cross":
                #From the portfolio we need to find the assset which needs to be used
                index = BuySellTextBoxes.findDictionaryValue(config.clientCrossMarginPortfolios[0],"asset",config.currentSymbol2);
                if index == -1: symbolAvalible = 0;
                else: symbolAvalible = config.clientCrossMarginPortfolios[0][index]['free'];     
            elif ui.comboBoxAccountMode.currentText()== "Isolated":
                index = BuySellTextBoxes.findDictionaryValue(config.clientIsolatedMarginPortfolios[0],"asset",config.currentSymbol2);
                if index == -1: symbolAvalible = 0;
                else: symbolAvalible = config.clientIsolatedMarginPortfolios[0][index]['free'];

            ui.lineEditMarketAmountBuyTotal.setText(str(
                (float(symbolAvalible) /100)* float(ui.lineEditMarketBuySlider.text())) if symbolAvalible != 0 else "0")
            ui.lineEditMarketAmountBuy.setText(str(
                (float(ui.lineEditMarketAmountBuyTotal.text())/float(config.currentPairPrice))))


        
        if ui.lineEditMarketAmountSell.text() != "" and float(ui.lineEditMarketAmountSell.text()) != 0 and config.marketSellMode=="amount":
            ui.lineEditMarketAmountSellTotal.setText(str(float(ui.lineEditMarketAmountSell.text())*(config.currentPairPrice)))
        elif ui.lineEditMarketAmountSellTotal.text() != "" and float(ui.lineEditMarketAmountSellTotal.text()) != 0 and config.marketSellMode=="total":
            ui.lineEditMarketAmountSell.setText(str(
                (float(ui.lineEditMarketAmountSellTotal.text()) )/config.currentPairPrice))
        elif config.marketSellMode=="slider":
            if ui.comboBoxAccountMode.currentText()== "Spot":   symbolAvalible = config.clientSymbol1Avalible[0]
            elif ui.comboBoxAccountMode.currentText()== "Cross":
                #From the portfolio we need to find the assset which needs to be used
                index = BuySellTextBoxes.findDictionaryValue(config.clientCrossMarginPortfolios[0],"asset",config.currentSymbol1);
                if index == -1: symbolAvalible = 0;
                else: symbolAvalible = config.clientCrossMarginPortfolios[0][index]['free'];     
            elif ui.comboBoxAccountMode.currentText()== "Isolated":
                index = BuySellTextBoxes.findDictionaryValue(config.clientIsolatedMarginPortfolios[0],"asset",config.currentSymbol1);
                if index == -1: symbolAvalible = 0;
                else: symbolAvalible = config.clientIsolatedMarginPortfolios[0][index]['free'];
     
            ui.lineEditMarketAmountSell.setText(str(
                (float(symbolAvalible) /100)* float(ui.lineEditMarketSellSlider.text())) if symbolAvalible != 0 else "0")
            ui.lineEditMarketAmountSellTotal.setText(str(
                (float(ui.lineEditMarketAmountSell.text())*float(config.currentPairPrice))))
            
        self.writeLock= False;
        
    def findDictionaryValue(list, key, value):
        for i, dic in enumerate(list):
            if dic[key] == value:
                return i
        return -1