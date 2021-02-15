import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from SubWindow import SubWindow
#from lib.SubWindow import SubWindow
#import lib.swLCD
from lib.swLCD import swLCD
from lib.swSpeaker import swSpeaker
from lib.swCamera import swCamera
from lib.swMIC import swMIC
from lib.swMotor import swMotor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        
        #
        label = QLabel("Head Test")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addStretch(1)
        
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        self.label = label
        
        #
        lbCAM = QLabel("CAMERA")
        layout.addWidget(lbCAM)
        self.lbCAM = lbCAM

        #
        lbMIC = QLabel("MIC")
        layout.addWidget(lbMIC)
        self.lbMIC = lbMIC
        
        #
        lbLCD = QLabel("LCD")
        layout.addWidget(lbLCD)
        self.lbLCD = lbLCD

        #
        lbSPK = QLabel("SPEAKER")
        layout.addWidget(lbSPK)
        self.lbSPK = lbSPK

        #
        lbMO_HRoll = QLabel("HEAD13(roll)")
        layout.addWidget(lbMO_HRoll)
        self.lbMO_HRoll = lbMO_HRoll
        
        #
        lbMO_HPitch = QLabel("HEAD14(pitch)")
        layout.addWidget(lbMO_HPitch)
        self.lbMO_HPitch = lbMO_HPitch
        
        #thread set
        #thLCD = threading.Thread(target=swLCD.runLCDdisplay)
        #thLCD.start()
        #thLCD.stop()
       
        #start
        btnStart = QPushButton("START")
        btnStart.clicked.connect(self.onBtnStartClicked)
        layout.addWidget(btnStart)
        
        #OK
        btnOK = QPushButton("OK")
        btnOK.clicked.connect(self.onBtnOKClicked)
        layout.addWidget(btnOK)

        #NG
        btnNOK = QPushButton("NOK")
        btnNOK.clicked.connect(self.onBtnNOKClicked)
        layout.addWidget(btnNOK)
        
        #1-CAMERA
        #btnCAM = QPushButton("CAMERA")
        #btnCAM.clicked.connect(self.onBtnCamClicked)
        #layout.addWidget(btnCAM)
        
        #2-MIC_REC
        #btnMIC = QPushButton("MIC_REC")
        #btnMIC.clicked.connect(self.onBtnMicClicked)
        #layout.addWidget(btnMIC)
        
        #3-LCD
        #btnLCD = QPushButton("LCD")
        #btnLCD.clicked.connect(self.onBtnLcdClicked)
        #layout.addWidget(btnLCD)
        
        #4-Speaker
        #btnSpeaker = QPushButton("Speaker")
        #btnSpeaker.clicked.connect(self.onBtnSpeakerClicked)
        #layout.addWidget(btnSpeaker)
     
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def initLabel(self):
        pass
 
    def onBtnStartClicked(self):
        
        texttmp=""
        texttmp = self.lbCAM.text()
        self.lbCAM.setText(texttmp+">>>>> Processing")
        self.lbCAM.repaint()
        
        #cam test
        self.onBtnCamClicked()
        
        texttmp=""
        texttmp = self.lbCAM.text()
        self.lbCAM.setText(texttmp+">>>>> Pass")
        self.lbCAM.setStyleSheet("Color:green")
        self.lbCAM.repaint()

        #mic start, label display
        texttmp=""
        texttmp = self.lbMIC.text()
        self.lbMIC.setText(texttmp+">>>>> Processing")
        self.lbMIC.repaint()
        
        #mic test run
        micTestResult = 0
        iMIC = swMIC()
        iMIC.start()
        micTestResult = iMIC.join()
        print("test result:",str(micTestResult))
        
        if micTestResult == "11":
            self.lbMIC.setText("mic result success")
            self.lbMIC.setStyleSheet("Color:green")
        else:
            self.lbMIC.setText("mic result fail")
            self.lbMIC.setStyleSheet("Color:red")

        #LCD start, label display
        texttmp=""
        texttmp = self.lbLCD.text()
        self.lbLCD.setText(texttmp+">>>>> Processing")
        self.lbLCD.repaint()
        
        LTResult = None
        #LCD test run
        LTResult = self.onBtnLcdClicked()
        
        #LCD finish
        if LTResult == "11":
            self.lbLCD.setText("LCD result success")
            self.lbLCD.setStyleSheet("Color:green")
        else:
            self.lbLCD.setText("LCD Device not connected")
            self.lbLCD.setStyleSheet("Color:red")
            
        #refresh LCD text
        self.lbLCD.repaint()
        
        #Speaker start, label display
        texttmp=""
        texttmp = self.lbSPK.text()
        self.lbSPK.setText(texttmp+">>>>>> Processing")
        self.lbSPK.repaint()
        
        #SPK test run
        STResult = None
        STResult = self.onBtnSpeakerClicked()
        
        #SPK finish
        if STResult == "11":
            self.lbSPK.setText("Speaker result success")
            self.lbSPK.setStyleSheet("Color:green")
        else:
            self.lbSPK.setText("Speaker Device not connected")
            self.lbSPK.setStyleSheet("Color:red")
        self.lbSPK.repaint()
        
        #motor
        MTResult = None
        MTResult = self.onBtnMotorClicked()
        
        if MTResult == "11":
            self.lbMO_HRoll.setText("Motor(13) result success")
            self.lbMO_HRoll.setStyleSheet("Color:green")
            self.lbMO_HPitch.setText("Motor(14) result success")
            self.lbMO_HPitch.setStyleSheet("Color:green")
        else:
            self.lbMO_HRoll.setText("Motor(13) is not response")
            self.lbMO_HRoll.setStyleSheet("Color:red")
            self.lbMO_HPitch.setText("Motor(14) is not response")
            self.lbMO_HPitch.setStyleSheet("Color:red")
           
        
    def onBtnOKClicked(self):
        pass
    
    def onBtnNOKClicked(self):
        pass
    
    def onBtnCamClicked(self):
        thCAM = threading.Thread(target=swCamera.run)
        thCAM.start()
        thCAM.join()
    
    def onBtnMicClicked(self):
        pass
        
    def onBtnLcdClicked(self):
        #swLCD.runLCDdisplay()
        #t = threading.Thread(target=swLCD.runLCDdisplay)
        #t.start()
        thLCD = threading.Thread(target=swLCD.run)
        LCDTestResult = None
        
        if not thLCD.is_alive():
            thLCD.start()
            LCDTestResult = thLCD.join()
        else:
            thLCD.kill()
            thLCD.start()
            LCDTestResult = thLCD.join()
        
        print("test result:",str(LCDTestResult))
        return LCDTestResult

    def onBtnMotorClicked(self):
        motorTestResult = None
        motor = swMotor()
        motor.start()
        motorTestResult = motor.join()
        return motorTestResult

    def onBtnSpeakerClicked(self):
        speakerTestResult = None
        sout = swSpeaker()
        sout.start()
        speakerTestResult = sout.join()
        print(speakerTestResult)
        return speakerTestResult
        
   
    def show(self):
        super().show()
        
if __name__ == '__main__':
    print("use external call")