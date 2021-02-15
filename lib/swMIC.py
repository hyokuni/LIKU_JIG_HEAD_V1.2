import pyaudio
import numpy as np
import threading
import time

# 5sec run, peak count, and result return
THD_MIC_COUNT = 11
RETURN_PASS = 22
RETURN_FAIL = 11

class swMIC(threading.Thread):
    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self.initMIC()

        self.count =0
        self.flagRun =0
        self._return = None
        self._nopen = None
        
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

    #obslate
    def test_result(self,target,maxi_count):
        if(target > maxi_count):
            print("fail mic test")
            self._return = 11
        else:
            print("OK mic test")
            self._return = 22
    
    #brand new
    def test_result_each(self,target,maxi_count,dnum):
        if(target > maxi_count):
            print("fail mic test:",str(dnum))
            rvalue = 1 <<(dnum-1)
            print("rvalue:",str(rvalue))
            return rvalue
            #return dnum
            
        else:
            print("OK mic test:",str(dnum))
            return 0
            
    def run(self):
        self.startTimer()
        #CHUNK = 2**11
        #RATE = 44100
        #option->sample 48k, CHUNK = 2^16
        CHUNK =2**16
        RATE = 48000
        
        self.torooc_device_index = 0
        
        try:
            p=pyaudio.PyAudio()
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            
            #dummy
            #stream=p.open()
            
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                    
                    #get device name
                    
                    strtmp =''
                    strtmp = p.get_device_info_by_host_api_device_index(0, i).get('name')
                    
                    #find LIKU Audio
                    #print( strtmp.find('LIKU Audio') )
                    
                    #save index
                    if strtmp.find('LIKU Audio') == 7:
                        self.torooc_device_index = i
                        #print('torooc index number:',self.torooc_device_index)
                        #print(type(self.torooc_device_index))
                    #else:
                    #    print('error find LIKU Audio')
                    #    self._nopen = -1
                    #    self._return = 11           
       
            if not self.torooc_device_index:
                self._nopen = -1
                self._return = 15
                
            stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,input=True,
                          input_device_index=self.torooc_device_index,frames_per_buffer=CHUNK)

            #peakdata1 = 0
            #peakdata2 = 0
            peakthdMIC1 = 0
            peakthdMIC2 = 0
            peakthdMIC3 = 0
            peakthdMIC4 = 0

            print('start record in 5sec')

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
                
                #maxMIC1 = np.max(dataMIC1)
                #maxMIC2 = np.max(dataMIC2)
                #maxMIC3 = np.max(dataMIC3)
                #maxMIC4 = np.max(dataMIC4)

                #peakMIC1 =np.average(np.abs(dataMIC1))* 2
                #peakMIC2 =np.average(np.abs(dataMIC2))* 2
                #peakMIC3 =np.average(np.abs(dataMIC3))* 2
                #peakMIC4 =np.average(np.abs(dataMIC4))* 2
                
                #bars1="#"*int(50*peakMIC1/2**16)
                #bars2="#"*int(50*peakMIC2/2**16)
                #bars3="#"*int(50*peakMIC3/2**16)
                #bars4="#"*int(50*peakMIC4/2**16)

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
                    print('flag out')
                    break
            #old
            #self.test_result(11,peakthdMIC1)
            
            #new
            global THD_MIC_COUNT
            print(THD_MIC_COUNT)
            print(peakthdMIC1)
            print(peakthdMIC2)
            print(peakthdMIC3)
            print(peakthdMIC4)
            print("----")
            
            err_mic = 0
            err_mic = err_mic + self.test_result_each(THD_MIC_COUNT,peakthdMIC1,1) #mic1
            err_mic = err_mic + self.test_result_each(THD_MIC_COUNT,peakthdMIC2,2) #mic2
            err_mic = err_mic + self.test_result_each(THD_MIC_COUNT,peakthdMIC3,3) #mic3
            err_mic = err_mic + self.test_result_each(THD_MIC_COUNT,peakthdMIC4,4) #mic4
            
            print("err_mic result:",str(err_mic))
            
            #return result
            global RETURN_PASS
            
            if err_mic == 0:
                self._return = RETURN_PASS
            else:
                self._return = err_mic
            
            print('return value:',str(self._return))
            
            
        except:
            print('except')
        finally:
            print('finally')
            if(self._nopen == None):
                if stream is not None:
                    stream.close()
                if p is not None:
                    #p.terminate()
                    pass
                time.sleep(1)
            
        #stream.stop_stream()
        #stream.close()
        #p.terminate()    #segmentation error
        #print("program end")

    def join(self,*args):
        threading.Thread.join(self)
        print(self._return)
        return self._return


if __name__ == "__main__":
    a = swMIC()
    a.run()
