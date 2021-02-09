#서버 주소가 저장된 파일에서 주소를 불러들여 실행
import os
import subprocess
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

#define parameters
USBID_LOGITECH = "046d:c52b"
runLCD_CMD = "mplayer -nolirc -nosound -fs -fps 30 -vo fbdev:/dev/fb1 /home/user/docker/livot-setup/misc/bigbuckbunny320p.mp4"
class swLCD:
    def run():
        #process only
        #os.system(runLCD_CMD)

        #process & return
        #result = subprocess.run(['mplayer','-nolirc','-nosound','-fs','-fps','30','-vo','fbdev:/dev/fb1','/home/user/docker/livot-setup/misc/bigbuckbunny320p.mp4'],stdout=subprocess.PIPE)
        #print(result.stdout)
        
        #subprocess_timeout
        p1 = subprocess.Popen(runLCD_CMD,shell=True)
        print('swLCD pid:',str(p1.pid))
        
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
    swLCD.run()