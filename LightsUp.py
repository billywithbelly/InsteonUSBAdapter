'''
    * @file     LightsUp.py
    * @brief    Create user interface and send commands
    * @author   Billy Chen
    * @bug      No known bugs
'''
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QMessageBox, QListWidget)
from PyQt5.QtCore import *

import time
import sys
import serial
import binascii

APPNAME = "LightsUp"
INSTRUCTION = 'This tool can help us control devices under the protocol of Inteon'

s = serial.Serial('YOUR_OWN_PORT', YOUR_OWN_BAUDRATE, timeout=2)

commands = {}
commands['link'] = '02640301'
commands['on1'] = '0262'
commands['on2'] = '0F11FF'
commands['on3'] = '0262'
commands['on4'] = '0f110f'
commands['off1'] = '0262'
commands['off2'] = '0F1300'
commands['reset'] = '0267'

listOfDevice = list()

class Dialog(QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.TARGETDEVICE = 'N/A'

        def on_click():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(APPNAME)
            msg.setText("About")
            labelFont = QMessageBox().font()
            labelFont.setPointSize(15)
            labelFont.setBold(True)
            labelFont.setFamily('System')
            msg.setFont(labelFont)
            msg.setInformativeText(INSTRUCTION)
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        def scanForDevices():
            state = 'ha'
            s.write(binascii.unhexlify('0269'))
            response = s.read(1024)
            hexResponse = binascii.hexlify(response)
            if (len(hexResponse) >  20):
                lightID = str(hexResponse[len(hexResponse)-12:len(hexResponse)-6], 'ascii')
                print(lightID)
                if lightID not in listOfDevice:
                    listOfDevice.append(lightID)
                    listwidget.addItem(lightID)
                listOfDevice.append(lightID)
                while (state == 'ha'):
                    s.write(binascii.unhexlify('026a'))
                    response = s.read(1024)
                    if (len(binascii.hexlify(response))<10):
                        state = 'he'
                    else:
                        hexResponse = binascii.hexlify(response)
                        lightID = str(hexResponse[len(hexResponse)-12:len(hexResponse)-6], 'ascii')
                        print(lightID)
                        if lightID not in listOfDevice:
                            listOfDevice.append(lightID)
                            listwidget.addItem(lightID)

        def quit_app(self):
            sys.exit(app.exec_())

        def start_function():     
            print ("Run function!")
            CommandDescription.setText("Update")

        def connect_function():     
            print ("Connect function!")
            s.write(binascii.unhexlify('02640301'))
            response = s.read(1024)
            print(binascii.hexlify(response))
            print('-------')
            scanForDevices()

        def max_function():     
            print ("Max function!")
            if (len(self.TARGETDEVICE) < 4):
                print('Please select target!')
            else:
                print(commands['on1'] + self.TARGETDEVICE + commands['on2'])
                s.write(binascii.unhexlify(commands['on1'] + self.TARGETDEVICE + commands['on2']))
                response = s.read(1024)
                print('-------')

        def lit_function():     
            print ("Lit function!")
            if (len(self.TARGETDEVICE) < 4):
                print('Please select target!')
            else:
                print(commands['on3'] + self.TARGETDEVICE + commands['on4'])
                s.write(binascii.unhexlify(commands['on3'] + self.TARGETDEVICE + commands['on4']))
                response = s.read(1024)
                print('-------')

        def dim_funtion():     
            print ("Dim function!")
            if (len(self.TARGETDEVICE) < 4):
                print('Please select target!')
            else:
                print(commands['off1'] + self.TARGETDEVICE + commands['off2'])
                s.write(binascii.unhexlify(commands['off1'] + self.TARGETDEVICE + commands['off2']))
                response = s.read(1024)
                print('-------')

        def reset_funtion():     
            print ("Reset function!")
            s.write(binascii.unhexlify(commands['reset']))
            self.TARGETDEVICE = 'N/A'
            listwidget.clear()
            listOfDevice.clear()
            print('-------')

        def selectionChanged(item):
            self.TARGETDEVICE = str(item.text())
            targetDeviceDescription.setText(self.TARGETDEVICE)
            print("Selected items:", item.text())


        CommandDescription = QLabel('Target Device:')
        targetDeviceDescription = QLabel(self.TARGETDEVICE)

        exitButton=QPushButton("Exit")
        exitButton.clicked.connect(quit_app)
        
        instructionButton=QPushButton('About')
        instructionButton.clicked.connect(on_click)

        connectButton=QPushButton("Connect")
        connectButton.clicked.connect(connect_function)

        maxBrightness=QPushButton("Max")
        maxBrightness.clicked.connect(max_function)

        LitButton=QPushButton("HalfLid")
        LitButton.clicked.connect(lit_function)

        DimButton=QPushButton("Dim")
        DimButton.clicked.connect(dim_funtion)

        resetButton=QPushButton("Reset")
        resetButton.clicked.connect(reset_funtion)

        listwidget = QListWidget()
        scanForDevices()
        #for i in range (0, len(listOfDevice)):
        #    listwidget.insertItem(i, listOfDevice[i])
        listwidget.itemClicked.connect(selectionChanged)

        leftLayout = QVBoxLayout()
        leftLayout.setAlignment(Qt.AlignTop)
        leftLayout.addWidget(targetDeviceDescription)
        leftLayout.addWidget(connectButton)
        leftLayout.addWidget(maxBrightness)
        leftLayout.addWidget(LitButton)
        leftLayout.addWidget(DimButton)
        leftLayout.addWidget(resetButton)


        mainLayout = QGridLayout()
        mainLayout.addWidget(CommandDescription, 0, 0, 1, 2)
        mainLayout.addLayout(leftLayout, 1, 0, 3, 2)
        mainLayout.addWidget(listwidget, 0, 2, 3, 2)
        mainLayout.addWidget(instructionButton, 4, 0, 1, 2)
        mainLayout.addWidget(exitButton, 4, 2, 1, 2)

        self.setLayout(mainLayout)
        self.setGeometry(150, 150, 300, 400)
        self.setWindowTitle(APPNAME)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
sys.exit(dialog.exec_())
