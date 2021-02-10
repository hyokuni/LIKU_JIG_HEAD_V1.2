import sys
import threading
from lib.serial485 import serial485

ttybaud = 1500000
ttyport = '/dev/ttyAMA0' #raspberrypi3b+ only

class swMotor(threading.Thread):
    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self._return = None
        
        self.flag_motorstop = 0
        
    # motor 동작시키기
    def th_motor_move(self,num,angle,mvtime,stiffness,refresh):
        #모터 enable 명령 실행
        #print('enable servo')
        self.ser.ctrlenable(num,0x01)
        
        #모터 시작 명령 실행(필수)
        self.ser.controlbegin(num)
        
        #서보 명령 실행
        #print('move servo')
        self.ser.servocmd(num,angle,mvtime,stiffness,refresh)
        
        #각도,agc 값 받기
        angle, agc = self.ser.getAngleAgc(num)
        print('thread angle' + str(angle) + ',thread agc' + str(agc))
        



 
    # motor 동작시키기
    def th_motor_motion(self,num,start_angle,end_angle,counter,mvtime,stiffness,refresh):
        #모터 enable 명령 실행
        #print('enable servo')
        self.ser.ctrlenable(num,0x01)
        
        #모터 시작 명령 실행(필수)
        self.ser.controlbegin(num)
        
        #서보 명령 실행
        #print('move servo')

        for i in range(1,counter+1):
            self.ser.servocmd(num,start_angle,mvtime,stiffness,refresh)
            angle, agc = self.ser.getAngleAgc(num)
            print('angle:',angle,',agc:',agc)
            
            #motor stop flag
            if self.flag_motorstop == 1:
                self.flag_motorstop = 0
                break
                        
            self.ser.servocmd(num,end_angle,mvtime,stiffness,refresh)
            angle, agc = self.ser.getAngleAgc(num)
            print('angle:',angle,',agc:',agc)
            
            #motor stop flag
            if self.flag_motorstop == 1:
                self.flag_motorstop = 0
                break
        
        #각도,agc 값 받기
#        angle, agc = self.ser.getAngleAgc(num)
#        print('thread angle' + str(angle) + ',thread agc' + str(agc))
        
       # elif num == 12:
       #    self.dp_ams12.display(angle)
       #    self.dp_agc12.display(agc)

        #motor disable
        self.ser.ctrlenable(num,0x00)
    
    
    def run(self):
        print('connect uart')
        
        global ttyport,ttybaud
        self.ttyport = ttyport
        self.ttybaud = ttybaud
        
        self.ser = serial485(self.ttyport,self.ttybaud,22)
        connect_stat = self.ser.connect(self.ttyport,self.ttybaud)
        
        #only run uart is connected
        if not connect_stat == True:
            print('connect fail')
            self._return = -1 #fail to connect
            
        else:
            print('connect ok')
          
            #motor check 13
            print('connection check-no13')
            if self.ser.ping(13) == 1:
                print('motor13 response ok')
            else:
                print('motor13 response fail')
                return -1

            #motor check 14
            print('connection check-no13')
            if self.ser.ping(14) == 1:
                print('motor14 response ok')
            else:
                print('motor14 response fail')
                return -1

            print('set cset')
            #self.ser.csetnow(11)
            #self.ser.csetnow(12)
                        
            print('move no13-low')
            print('check angle, and goal compare')
            self.th_motor_motion(13,1800,2200,10,200,15,1)
            
            print('move no13-high')
            print('check angle, and goal compare')
            
            print('move no14-low')
            print('check angle, and goal compare')
            self.th_motor_motion(14,1800,2200,10,200,15,1)
            
            
            print('move no14-high')
            print('check angle, and goal compare')
            
            pass
    
    def join(self,*args):
        threading.Thread.join(self)
        return self._return
	