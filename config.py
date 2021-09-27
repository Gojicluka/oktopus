import configparser
import json;
from binance import Client;


from portfolio import portfolioScrollArea
from userAccounts import userAccountsScrollArea

#config class for loading settings from config.ini
class Config():
    def __init__(self,ui) -> None:
        try:
            self.currentPair = "AAAAAAAAAAAAAAAAAA";
            self.mode = "Normal";
            self.isolatedCross = "Isolated";
            self.currentSymbol1 = "";
            self.currentSymbol2 = "";
            self.currentPairPrice = -1;

            self.weight = 0;
            
            self.marketBuyMode = "amount";
            self.marketSellMode = "amount";

            with open('config.ini') as fp:
                config = configparser.ConfigParser();
                config.read_file(fp);
                self.keyNames = json.loads(config.get("binance","keyNames"));
                self.apiKeys = json.loads(config.get("binance","apiKeys"));
                self.secretKeys = json.loads(config.get("binance","secretKeys"));
                self.symbols = json.loads(config.get("pairs","symbols"));
                self.pairs = json.loads(config.get("pairs","pairs"));
                self.selectedSymbols = json.loads(config.get("pairs","selectedSymbols"));
            
            self.clients = [];
            self.clientSpotPortfolios = [];
            self.clientCrossMarginPortfolios = [];
            self.clientIsolatedMarginPortfolios = [];
            self.clientSymbol1Avalible = [];
            self.clientSymbol2Avalible = [];
            

            for i in range(0,len(self.apiKeys)):
                self.clients.append(Client(self.apiKeys[i],self.secretKeys[i]))
                self.clientSpotPortfolios.append([]);
                self.clientCrossMarginPortfolios.append([]);
                self.clientIsolatedMarginPortfolios.append([]);
                self.clientSymbol1Avalible.append(-1);
                self.clientSymbol2Avalible.append(-1);
            
            self.openOrdersTables = [];
            self.portfolioTab = [];
            
            self.portfolioScrollArea = portfolioScrollArea(ui,self);
            self.userAccountsScrollArea = userAccountsScrollArea(ui,self);
        except Exception as ex:
            ui.console.append(f"Exception thrown at Config.__init__() : \n{ex}")
