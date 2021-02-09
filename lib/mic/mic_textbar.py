import sys
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QLabel,QApplication,QPushButton,QWidget
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
        
        #timer
        #win10-period 10ms is live 
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(50,self)

        #mic display ctrl
        self.turnonmic = 0
        
        #add label(graph)
        self.lbMIC1 = QLabel("mic1")
        self.lbMIC2 = QLabel("mic2")
        self.lbMIC3 = QLabel("mic3")
        self.lbMIC4 = QLabel("mic4")
        
        #add layout
        layout.addWidget(label)
        layout.addWidget(self.btn)
        layout.addWidget(self.lbMIC1)
        layout.addWidget(self.lbMIC2)
        layout.addWidget(self.lbMIC3)
        layout.addWidget(self.lbMIC4)
        layout.addStretch(1)      
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        
        #audio init
        self.audio_step = 0 
        p=pyaudio.PyAudio()

        #find audio device 
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0,numdevices):
            if(p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        #linux
        #self.stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,
        #              input=True,input_device_index = 2,frames_per_buffer=CHUNK)
        self.stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,
                           input=True,frames_per_buffer=CHUNK)
    
    
    def doAction(self):
        if(self.turnonmic == 1):
            self.turnonmic = 0
        else:
            self.turnonmic = 1

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
        
        if(self.turnonmic == 1):
            bars1="#"*int(50*(peakMIC1/2**15))
            bars2="#"*int(50*(peakMIC2/2**15))
            bars3="#"*int(50*(peakMIC3/2**15))
            bars4="#"*int(50*(peakMIC4/2**15))
            #bars2=int(100*(peakMIC2/2**15))
            #bars3=int(100*(peakMIC3/2**15))
            #bars4=int(100*(peakMIC4/2**15))

            #bars1=int(100*(peakMIC1/2**15))
            #bars2=int(100*(peakMIC2/2**15))
            #bars3=int(100*(peakMIC3/2**15))
            #bars4=int(100*(peakMIC4/2**15))
            
            #print("%d,%d,%d,%d %s"%(bars1,bars2,bars3,bars4,self.audio_step))
            #self.audio_step = self.audio_step + 1

            self.lbMIC1.setText(bars1)
            self.lbMIC2.setText(bars2)
            self.lbMIC3.setText(bars3)
            self.lbMIC4.setText(bars4)
        
   
    def micRead(self):
        pass
   
    def show(self):
        super().show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
