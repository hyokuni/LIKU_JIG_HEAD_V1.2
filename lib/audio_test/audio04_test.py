import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

peakdata1 = 0
peakdata2 = 0

while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    dataMIC1 = data[0::4]
    dataMIC2 = data[1::4]
    dataMIC3 = data[2::4]
    dataMIC4 = data[3::4]
    
    maxMIC1 = np.max(dataMIC1)
    maxMIC2 = np.max(dataMIC2)

    peakMIC1 =np.average(np.abs(dataMIC1))*2
    peakMIC2 =np.average(np.abs(dataMIC2))*2
    peakMIC3 =np.average(np.abs(dataMIC3))*2
    peakMIC4 =np.average(np.abs(dataMIC4))*2
    
    bars1="#"*int(50*peakMIC1/2**16)
    bars2="#"*int(50*peakMIC2/2**16)
    bars3="#"*int(50*peakMIC3/2**16)
    bars4="#"*int(50*peakMIC4/2**16)

    if(maxMIC1 > peakdata1):
        peakdata1 = maxMIC1 
        print("mic1:",str(peakdata1))

    if(maxMIC2 > peakdata2):
        peakdata2 = maxMIC2
        print("mic2:",str(peakdata2))
 


stream.stop_stream()
stream.close()
p.terminate()
