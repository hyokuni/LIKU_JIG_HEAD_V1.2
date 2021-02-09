import pyaudio
import numpy as np

#maxValue = 2**16
maxValue = 2**16
p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16,channels=4,rate=44100,
				input=True, frames_per_buffer=1024)

while True:
    data = np.fromstring(stream.read(1024),dtype=np.int16)
    dataL = data[0::4]
    dataR = data[1::4]
    dataL3= data[2::4]
    dataR3= data[3::4]
    #print("dataL:%f dataR:%f"%(dataL,dataR))
    #print(dataL)
    
    peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
    peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue
    peakL3= np.abs(np.max(dataL3)-np.min(dataL3))/maxValue
    peakR3= np.abs(np.max(dataR3)-np.min(dataR3))/maxValue
    print("L:%00.02f R:%00.02f L:%00.02f R:%00.02f"%(peakL*100,peakR*100,peakL3*100,peakR3*100))
    
	#print("L:%00.02f R:%00.02f"%(peakL*100, peakR*100))
	
#error channel3,4 is not real data, 
