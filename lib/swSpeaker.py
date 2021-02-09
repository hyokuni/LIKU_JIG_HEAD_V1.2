#LIKU AUDIO is OK that has any card number.

#import os
import subprocess
import sys
import threading
#from PyQt5.QtWidgets import *
#from PyQt5 import uic
#from PyQt5.QtCore import *

#card_num=$(cat /proc/asound/cards | grep "USB-Audio" | grep " Torooc LIKU Audio" | awk '{print $1;}')
#aplay -D plughw:$card_num,0 ../../misc/voice_mono_48000Hz_16bit_PCM.wav

#define parameters
runSpeaker_CMD = "mplayer -nolirc -nosound -fs -fps 30 -vo fbdev:/dev/fb1 /home/user/docker/livot-setup/misc/bigbuckbunny320p.mp4"
runSpeaker_CMD = "aplay -D plughw:$card_num,0 /home/user/docker/livot-setup/misc/voice_mono_48000Hz_16bit_PCM.wav"
CARD_NUM = 'plughw:9,0'
#SOUND_SRC_PATH = '/home/user/docker/livot-setup/misc/voice_mono_48000Hz_16bit_PCM.wav'
SOUND_SRC_PATH = '/home/user/Downloads/organfinale.wav'
TOROOC_SPK_USB_ID = '0483:5741'

class swSpeaker(threading.Thread):
    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self._return = None
        
    def indexDetect(self):
        result = subprocess.run(['arecord','-l'],stdout=subprocess.PIPE)
        print(result.stdout)
        
        strtmp = ''
        strtmp = str(result.stdout)
        indexAudio = strtmp.find('Torooc LIKU Audio')
        return strtmp[indexAudio-10] 
    
    def usbdetect(self):
        result = subprocess.run(['lsusb'],stdout=subprocess.PIPE)
        #print(result)
        
        lsusbtxt = ''
        lsusbtxt = str(result.stdout)
        
        if not lsusbtxt.find(TOROOC_SPK_USB_ID) == -1:
            print('speaker connect')
            return 0
        else:
            print('speaker not connect')
            return -1
    
    def run(self):
        global CARD_NUM
        #LIKU device connect
        s = list(CARD_NUM)
        print(s)
        s[7] = self.indexDetect()
        print(s)
       # CARD_NUM[8] = self.indexDetect()
        #print(self.indexDetect())
        CARD_NUM = "".join(s)
        
        print("changed card Number:",CARD_NUM)
        
        #print(CARD_NUM)
        if self.usbdetect() == 0:
            result = subprocess.run(['aplay','-D',CARD_NUM,SOUND_SRC_PATH],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)        
            print(result.stdout)
            
            #save shell txt
            strresult =''
            strresult = str(result.stdout)
            
            #
            print(strresult.find('Playing WAVE'))
            
            #playback sound ok
            if not strresult.find('Playing WAVE') == -1:
                print('pass')
                self._return = 11
            else:
                self._return = None
        else:
            print('error')
            #return 22
            self._return = 22

    def join(self,*args):
        threading.Thread.join(self)
        return self._return

if __name__ == "__main__":
    sout = swSpeaker()
    sout.run()
    #sout.indexDetect()