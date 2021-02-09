import sys
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QLabel,QProgressBar,QApplication,QPushButton,QWidget
from PyQt5.QtCore import *
import pyaudio
import numpy as np

#CHUNK = 4*10   #all zero, no response
CHUNK = 4**5
#CHUNK = 2**16
RATE = 44100

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


        #1-stop
        self.btn = QPushButton("User Button")
        self.btn.clicked.connect(self.doAction)
        
        # progress bar
        self.bar1 = QProgressBar(self)
        self.bar2 = QProgressBar(self)
        self.bar3 = QProgressBar(self)
        self.bar4 = QProgressBar(self)
        
        self.bar1.setValue(0)
        self.bar2.setValue(2)

        #timer
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(100,self)
        
        #add layout
        layout.addWidget(label)
        layout.addWidget(self.bar1)
        layout.addWidget(self.bar2)
        layout.addWidget(self.bar3)
        layout.addWidget(self.bar4)
        layout.addWidget(self.btn)
        layout.addStretch(1)      
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        
        #audio init
        self.audio_step = 0 
        p=pyaudio.PyAudio()
        self.stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,
                      input=True,frames_per_buffer=CHUNK)
    
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
        #data = np.fromstring(self.stream.read(CHUNK),dtype=np.int16)
        data = np.frombuffer(self.stream.read(CHUNK),dtype=np.int16)
        dataMIC1 = data[0::4]
        dataMIC2 = data[1::4]
        dataMIC3 = data[2::4]
        dataMIC4 = data[3::4]
        
        peakMIC1 =np.average(np.abs(dataMIC1))*2
        peakMIC2 =np.average(np.abs(dataMIC2))*2
        peakMIC3 =np.average(np.abs(dataMIC3))*2
        peakMIC4 =np.average(np.abs(dataMIC4))*2
        
        bars1=int(50*peakMIC1/2**16)
        bars2=int(50*peakMIC2/2**16)
        bars3=int(50*peakMIC3/2**16)
        bars4=int(50*peakMIC4/2**16)
        
        #print("%d,%d,%d,%d %s"%(bars1,bars2,bars3,bars4,self.audio_step))
        #self.audio_step = self.audio_step + 1
        
        #bar update
        self.bar1.setValue(bars1)
        self.bar2.setValue(bars2)
        self.bar3.setValue(bars3)
        self.bar4.setValue(bars4)
   
    def micRead(self):
        pass
   
    def show(self):
        super().show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    print("hi")