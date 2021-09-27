import configparser;
from PyQt5 import QtWidgets

from forms.pairsymbollist import Ui_Form as pairListForm
import buySell;


class PairSymbolList():
    '''
    @params
        -self
        -config = main instance of the config class
        -mainWindowUi = ui of the main window
        -action = checks whether to make this form for pairs or symbols
    '''
    def __init__(self,config,mainWindowUi,action) -> None:
        self.mainWindowUi = mainWindowUi
        self.config = config;
        self.app = QtWidgets.QWidget();
        self.ui = pairListForm();
        self.ui.setupUi(self.app);
        self.app.show();
        self.action = action;

        self.ui.pushButton.clicked.connect(self.submit)
        if self.action == "pair":
            self.ui.textEdit.setText(str("\n".join(self.config.pairs)));
        else:
            self.ui.textEdit.setText(str("\n".join(self.config.selectedSymbols)));
            self.ui.label.setText( "Symbol list");
    
    def submit(self):
        try: 
            #Updating the config file
            with open('config.ini') as fp:
                config = configparser.ConfigParser();
                config.read_file(fp);
                config.set("pairs","pairs" if self.action == "pair" else "selectedSymbols",str(self.ui.textEdit.toPlainText().splitlines()).replace('\'','"'));
                with open('config.ini',"w") as fp2:
                    config.write(fp2);
            #updating confing in memory
            if self.action == "pair":
                self.config.pairs = self.ui.textEdit.toPlainText().splitlines()
                self.updateElementsPair();
            else:
                self.config.selectedSymbols = self.ui.textEdit.toPlainText().splitlines()
                self.updateElementsSymbol();

            
            self.app.close();
        except Exception as ex:
            self.mainWindowUi.console.append(f"Exception thrown at OpenOrders.createTables() : \n{ex}")

    def updateElementsPair(self):
        buySell.BuySell.comboBoxSetup(self.mainWindowUi,self.config);

    def updateElementsSymbol(self):
        #buySell.BuySell.comboBoxSetup(self.mainWindowUi,self.config);
        pass;
