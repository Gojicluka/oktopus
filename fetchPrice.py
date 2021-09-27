import threading;
import asyncio
from PyQt5 import QtCore;
from PyQt5.QtCore import QThread;
from binance import BinanceSocketManager;
from binance import AsyncClient;

#Thread for fetching the prices of the pairs via websockets
class fetchPriceAlt(QThread):
    output = QtCore.pyqtSignal(str)
    
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
        asyncio.get_event_loop().run_until_complete(fetchPriceAlt.fetchPairPrice(self,self.config))
    '''
    Fetches the price of the current pair via web socket

    @params
        -self
        -config = pointer to the class that stores all the data that is needed
    '''
    async def fetchPairPrice(self,config):
        #self.output.emit(podaci);
        client = await AsyncClient.create()
        bsm  = BinanceSocketManager(client);
        try:
            while True:
                currentThreadPair = config.currentPair;
                socket = bsm.symbol_ticker_socket(config.currentPair);
                async with socket as tscm:
                    #While pair isn't switched fetch prices from binance webscoket
                    while currentThreadPair == config.currentPair:
                        #await tscm.__aenter__();
                        res = await tscm.recv()
                        formated_price = "{:.2f}".format(float(res['c']))
                        config.currentPairPrice = float(res['c']);
                        self.output.emit(str(res['c']));

        except Exception as ex:
            print(ex);
            print("exception")

