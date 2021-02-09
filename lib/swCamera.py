import os
import subprocess
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *


#define parameters
USBID_LOGITECH = "046d:c52b"
runSpeaker_CMD = "mplayer -nolirc -nosound -fs -fps 30 -vo fbdev:/dev/fb1 /home/user/docker/livot-setup/misc/bigbuckbunny320p.mp4"
runSpeaker_CMD = "aplay -D plughw:$card_num,0 /home/user/docker/livot-setup/misc/voice_mono_48000Hz_16bit_PCM.wav"
CARD_NUM = 'plughw:2,0'
#SOUND_SRC_PATH = '/home/user/docker/livot-setup/misc/voice_mono_48000Hz_16bit_PCM.wav'
SOUND_SRC_PATH = '/home/user/Downloads/organfinale.wav'
runCamera_CMD="vlc v4l2:///dev/video0" 

class swCamera():
    def run():
        #result = subprocess.run(['aplay','-D',CARD_NUM,SOUND_SRC_PATH],stdout=subprocess.PIPE)        
        #print(result.stdout)
 
       #subprocess_timeout
        p1 = subprocess.Popen(runCamera_CMD,shell=True)
        print('swCamera pid:',str(p1.pid))
        
        try:
            p1.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            #subprocess.call(['taskkill','/f','/t','/pid',str(p1.pid)],shell=True)
            print(p1.pid)
            #subprocess.call(['kill','-9',str(p1.pid)],shell=True)
            subprocess.run(['kill','-9',str(p1.pid+1)],stdout=subprocess.PIPE)
            print("except timeout, try kill process:",str(p1.pid+1))
        
        #result 
        
        #return state(0=runok,1=device error)
        #return 0 
 
 
 
if __name__ == "__main__":
    pass