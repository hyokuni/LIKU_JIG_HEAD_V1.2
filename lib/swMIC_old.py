import os
import subprocess
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *


#define parameters
runMIC_CMD="audacity"

class swMIC():
    def run():
        #result = subprocess.run(['aplay','-D',CARD_NUM,SOUND_SRC_PATH],stdout=subprocess.PIPE)        
        #print(result.stdout)
 
       #subprocess_timeout
        p1 = subprocess.Popen(runMIC_CMD,shell=True)
        print('swMIC pid:',str(p1.pid))
        
        try:
            p1.communicate(timeout=60)
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