import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel("Head Test")
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        self.label = label
        layout.addWidget(label)
        layout.addStretch(1)
        
        #thread set
        #thLCD = threading.Thread(target=swLCD.runLCDdisplay)
        #thLCD.start()
        #thLCD.stop()
        
        #1-CAMERA
        btnCAM = QPushButton("CAMERA")
        btnCAM.clicked.connect(self.onBtnCamClicked)
        
        # progress bar
        self.bar = QProgressBar(self)
        self.bar.setValue(10)
        
        layout.addWidget(btnCAM)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def onBtnCamClicked(self):
       self.bar.setValue(20)

    
   
    def show(self):
        super().show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    print("hi")