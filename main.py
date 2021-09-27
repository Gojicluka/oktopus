#External modules
from PyQt5 import QtWidgets;
import asyncio;

#Internal modulesmodules
from MainWindow import MainWindow

'''
#todo
'''

async def main():
    #mandatory stuff pyqt needs
    import sys;
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow();
    mainWindow.show();
    config = mainWindow.config;
    

    sys.exit(app.exec_()); 
    

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main());
