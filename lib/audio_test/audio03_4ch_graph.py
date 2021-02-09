import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=4,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    dataMIC1 = data[0::4]
    dataMIC2 = data[1::4]
    dataMIC3 = data[2::4]
    dataMIC4 = data[3::4]
    
    peakMIC1 =np.average(np.abs(dataMIC1))*2
    peakMIC2 =np.average(np.abs(dataMIC2))*2
    peakMIC3 =np.average(np.abs(dataMIC3))*2
    peakMIC4 =np.average(np.abs(dataMIC4))*2
    
    bars1="#"*int(50*peakMIC1/2**16)
    bars2="#"*int(50*peakMIC2/2**16)
    bars3="#"*int(50*peakMIC3/2**16)
    bars4="#"*int(50*peakMIC4/2**16)
    print("-------------------------")
    print("-------------------------")
    print("-------------------------")
    print("%05d %s"%(peakMIC1,bars1))
    print("%05d %s"%(peakMIC2,bars2))
    print("%05d %s"%(peakMIC3,bars3))
    print("%05d %s"%(peakMIC4,bars4))
    print("-------------------------")
    print("-------------------------")
    print("-------------------------")

stream.stop_stream()
stream.close()
p.terminate()