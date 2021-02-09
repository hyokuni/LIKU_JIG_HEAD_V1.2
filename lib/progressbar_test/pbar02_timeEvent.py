import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('ProgressBar Example')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel("MIC Test(Pbar)")
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        self.label = label
        layout.addWidget(label)
        layout.addStretch(1)
        
  
        #1-stop
        self.btn = QPushButton("User Button")
        self.btn.clicked.connect(self.doAction)
        
        # progress bar
        self.bar = QProgressBar(self)
        self.bar.setValue(0)

        #timer
        self.timer = QBasicTimer()
        self.step = 0

        layout.addWidget(self.btn)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def onBtnCamClicked(self):
       self.bar.setValue(20)
       
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100,self)
            self.btn.setText('Stop')

    def timerEvent(self,e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return
        
        self.step = self.step + 1
        self.bar.setValue(self.step)
   
    def show(self):
        super().show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    print("hi")