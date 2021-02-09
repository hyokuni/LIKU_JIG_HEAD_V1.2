import pyaudio
import numpy as np
import threading
from threading import Thread

class swMIC(Thread):

    def __init__(self,group=None,target=None,name=None,
                 args=(),kwargs={}):
        Thread.__init__(self,group,target,name,args)
        
        self.initMIC()

        self._return = None
        self.count = 0
        self.flagRun = 0
        #self.run()
        
    def initMIC(self):
        pass
    
    def startTimer(self):
        #global count
        #print("timer",str(count))
        
        timer = threading.Timer(1, self.startTimer) # n sec
        
        self.count = self.count + 1
        if(self.count <= 5):
            timer.start()
        else:
            timer.cancel()
            #print("timer stop")
            #off condition
            #global flagRun
            self.flagRun = 1

    #return Array over threshold number
    def thdArray(self,thdNum,array):
        newArr = []
        for tmp in array:
            if(tmp > thdNum):
                newArr.append(tmp)
        #print(newArr)
        return newArr

    #
    def test_result(self,target,maxi_count):
        if(target > maxi_count):
            print("fail mic test")
            return 2
        else:
            print("OK mic test")
            return 1
            
    def run(self):
        self.startTimer()
        CHUNK = 2**11
        RATE = 44100
        #option->sample 48k, CHUNK = 2^16
        #CHUNK =2**16
        #RATE = 48000
        
        p=pyaudio.PyAudio()
        #info = p.get_host_api_info_by_index(0)
        #numdevices = info.get('deviceCount')
        #for i in range(0, numdevices):
        #    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        #        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        #        pass

        stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,input=True,
                      frames_per_buffer=CHUNK)

        peakdata1 = 0
        peakdata2 = 0
        peakthdMIC1 = 0
        peakthdMIC2 = 0
        peakthdMIC3 = 0
        peakthdMIC4 = 0

        #get mic data for Nsec
        while True:
            data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
            dataMIC1 = data[0::4]
            dataMIC2 = data[1::4]
            dataMIC3 = data[2::4]
            dataMIC4 = data[3::4]
            
            thdM1 =np.size( self.thdArray(30000,dataMIC1) )
            thdM2 =np.size( self.thdArray(30000,dataMIC2) )
            thdM3 =np.size( self.thdArray(30000,dataMIC3) )
            thdM4 =np.size( self.thdArray(30000,dataMIC4) )
            
            #print("threshold MIC count:",str(thdM1))
            
            maxMIC1 = np.max(dataMIC1)
            maxMIC2 = np.max(dataMIC2)
            maxMIC3 = np.max(dataMIC3)
            maxMIC4 = np.max(dataMIC4)

            peakMIC1 =np.average(np.abs(dataMIC1))* 2
            peakMIC2 =np.average(np.abs(dataMIC2))* 2
            peakMIC3 =np.average(np.abs(dataMIC3))* 2
            peakMIC4 =np.average(np.abs(dataMIC4))* 2
            
            bars1="#"*int(50*peakMIC1/2**16)
            bars2="#"*int(50*peakMIC2/2**16)
            bars3="#"*int(50*peakMIC3/2**16)
            bars4="#"*int(50*peakMIC4/2**16)

            #display max data 
            #if(maxMIC1 > peakdata1):
            #    peakdata1 = maxMIC1 
            #    print("mic1:",str(peakdata1))

            #if(maxMIC2 > peakdata2):
            #    peakdata2 = maxMIC2
            #    print("mic2:",str(peakdata2))

            if(thdM1 > peakthdMIC1):
                peakthdMIC1 = thdM1
                #print("peak cound MIC1:",str(peakthdMIC1))

            if(thdM2 > peakthdMIC2):
                peakthdMIC2 = thdM2
                #print("peak cound MIC2:",str(peakthdMIC2))

            if(thdM3 > peakthdMIC3):
                peakthdMIC3 = thdM3
                #print("peak cound MIC3:",str(peakthdMIC3))
                
            if(thdM4 > peakthdMIC4):
                peakthdMIC4 = thdM4
                #print("peak cound MIC4:",str(peakthdMIC4))

            #termination
            if self.flagRun:
                break
        
        #test
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,**self._kwargs)
            
        
        self.test_result(11,peakthdMIC1)
        # this is occured, segmentation error, wtf
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        #freturn = 0
        #freturn = self.test_result(11,peakthdMIC1)
        #self.test_result(11,peakthdMIC1)
        
        
        #return freturn
        #print("program end")
        def join(self,*args):
            Thread.join(self, *args)
            return self._return

if __name__ == "__main__":
    a = swMIC()
    #a.run()
    a.start()
    rvalue = a.join()
    print(rvalue)