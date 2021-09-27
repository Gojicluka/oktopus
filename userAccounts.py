from PyQt5 import QtWidgets,QtGui;

class userAccountsScrollArea():
    def __init__(self,ui,config) -> None:
        self.ui = ui;
        self.config = config;
        #create group box
        font = QtGui.QFont()

        self.groupBoxes = [];
        self.checkBoxes = [];
        self.sliders = [];
        self.textBoxes = [];
        
        font.setPointSize(12);
        for i in range(0,len(config.clients)):  
            hbox = QtWidgets.QHBoxLayout();
            self.groupBoxes.append(QtWidgets.QGroupBox());

            #create checkBox    
            self.checkBoxes.append(QtWidgets.QCheckBox(config.keyNames[i]));
            self.checkBoxes[i].setFont(font);
            self.checkBoxes[i].setChecked(True);
            hbox.addWidget(self.checkBoxes[i]);
            

            # self.sliders.append(QtWidgets.QSlider(QtCore.Qt.Horizontal));
            # self.sliders[i].setMaximum(100)
            # self.sliders[i].setValue(100);
            # hbox.addWidget(self.sliders[i]);

            # self.textBoxes.append(QtWidgets.QLineEdit("100"));
            # self.textBoxes[i].setFont(font);
            # self.textBoxes[i].setAlignment(QtCore.Qt.AlignRight)
            # self.textBoxes[i].setFixedWidth(40)
            # hbox.addWidget(self.textBoxes[i]);

            # label = QtWidgets.QLabel("%");
            # label.setFont(font);
            # hbox.addWidget(label);
            #self.groupBoxes[i].setStyleSheet("border:none;");
            self.groupBoxes[i].setLayout(hbox);
        
        scrollAreawidget = QtWidgets.QWidget();
        vbox = QtWidgets.QVBoxLayout();
        vbox.setSpacing(0);
        vbox.setContentsMargins(0,0,0,0)

        naslov = QtWidgets.QLabel("User accounts");
        font.setPointSize(28)
        naslov.setFont(font);
        vbox.addWidget(naslov);

        
        for i in range(0,len(self.sliders)):
            self.sliders[i].valueChanged.connect( lambda: self.textBoxes[i].setText(str(self.sliders[i].value())))

        for groupBox in self.groupBoxes:
            vbox.addWidget(groupBox);
        
        vbox.addWidget(QtWidgets.QLabel(""),120)
        scrollAreawidget.setLayout(vbox);
        self.ui.scrollAreaUserAccounts.setWidget(scrollAreawidget);
