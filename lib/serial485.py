#version2, 20.09.18

import serial
import time

class serial485:
    def __init__(self, serialPort='/dev/ttyHS0', serialBaud=1500000, nActuators=22):
        self.port = serialPort
        self.baud = serialBaud
        self.numAct = nActuators       
        self.connected = False
    

    
    def connect(self, SP, SB):
        
        self.port = SP
        self.baud = SB
        self.connected = False
    
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0)
            print('Connected')
            self.connected = True
            return True

        except:
            print('Failed')
            self.connected = False
            return False
    
    def ping(self,act_id):
        txdata = [0xFE,0xEF]
        msglength = 5
        actnum = act_id & 0xFF
        msgtype = 0x80 + 3
        msgH = 0x01
        msgL = 0x01
        crc = (msglength + actnum + msgtype + msgH + msgL)&0xFF
        
        txdata.append(msglength)
        txdata.append(actnum)
        txdata.append(msgtype)
        txdata.append(msgL)
        txdata.append(msgH)
        txdata.append(crc)
        print(txdata)
        
        hextxdata = bytearray(txdata)
        print(hextxdata)
        
        #데이터 전송하기
        self.ser.write(hextxdata)
        time.sleep(0.1)
        
        #데이터 읽기
        self.resp_data = self.ser.readline()
        #print('data response:' + self.response_data)
        print(self.resp_data)
        #데이터 확인
        #print(type(self.resp_data))

        #수신응답 데이터 확인
        ack_msglength = 7
        ack_msgtype = 0x03
        ack_msgL = (msgL+1)&0xFF
        ack_msgH = msgH
        ack_crc = (ack_msglength + actnum + ack_msgtype + msgH + msgL + ack_msgL + ack_msgH )&0xFF
        
        cf_ping = [0xFE,0xEF]

        cf_ping.append(ack_msglength)
        cf_ping.append(actnum)
        cf_ping.append(ack_msgtype)
        cf_ping.append(msgL)
        cf_ping.append(msgH)
        cf_ping.append(ack_msgL)
        cf_ping.append(ack_msgH)
        cf_ping.append(ack_crc)
        
        print(cf_ping)
        
        hex_cf_ping = bytearray(cf_ping)
        print(hex_cf_ping)
        
        if self.resp_data == hex_cf_ping :
            print('if ok')
            return 1
        else :
            return 0
        
    def motordirection(self,act_id):
        print('motor direction')
        #송신 데이터
        txdata1 = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 0x94
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata1.append(msglength)
        txdata1.append(actnum)
        txdata1.append(msgtype)
        txdata1.append(crc)
        print(txdata1)            
        
        hextxdata1 = bytearray(txdata1)
        print(hextxdata1)
        
        #데이터 전송하기
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(hextxdata1)
        time.sleep(1)
        
        #데이터 읽기
        self.resp_data1 = self.ser.read(13)
        #self.resp_data2 = self.ser.readline()
        #self.resp_data3 = self.ser.readline()
        print(self.resp_data1)
        #print(self.resp_data2)
        #print(self.resp_data3)
        print(self.resp_data1[10])
        
        if self.resp_data1[10] &0x08:
            print('motor reverse')
            return 1
        else:
            print('motor direct')
            return 0
        #print(type(self.resp_data))
        #print(self.resp_data[0])

    def angle_raw_check(self,act_id):
        print('angle raw get')
        #송신 데이터
        txdata1 = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 0x87
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata1.append(msglength)
        txdata1.append(actnum)
        txdata1.append(msgtype)
        txdata1.append(crc)
        print(txdata1)            
        
        hextxdata1 = bytearray(txdata1)
        print(hextxdata1)
        
        #데이터 전송하기
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(hextxdata1)
        #time.sleep(0.1)
        time.sleep(0.01)
        
        #데이터 읽기
        self.resp_data1 = self.ser.readline()
        print(self.resp_data1)
        
        #ams 센서에 자석 반응이 있으면 1, 없거나 연결되지 않으면 0 리턴
        angle = (self.resp_data1[6] * 0x100) + self.resp_data1[5]
    
        if angle >= 50 and angle <= 4000:
            return 1
        else :
            return 0
    
    def agc_check(self,act_id):
        print('agc get')
        #송신 데이터
        txdata1 = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 0x87
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata1.append(msglength)
        txdata1.append(actnum)
        txdata1.append(msgtype)
        txdata1.append(crc)
        print(txdata1)            
        
        hextxdata1 = bytearray(txdata1)
        print(hextxdata1)
        
        #데이터 전송하기
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(hextxdata1)
        #time.sleep(0.1)
        time.sleep(0.01)
        
        #데이터 읽기
        self.resp_data1 = self.ser.readline()
        print(self.resp_data1)
        
        print(self.resp_data1[9])
        return self.resp_data1[9]
        
    def motortest(self,act_id,pwm):
        #송신 데이터
        txdata = [0xFE,0xEF]
        msglength = 4
        actnum = act_id & 0xFF
        msgtype = 0x80 + 6
        motor_pwm = pwm & 0xFF
        crc = (msglength + actnum + msgtype + motor_pwm)&0xFF
    
        txdata.append(msglength)
        txdata.append(actnum)
        txdata.append(msgtype)
        txdata.append(motor_pwm)
        txdata.append(crc)
        print(txdata)    

        hextxdata = bytearray(txdata)
        print(hextxdata)
        
        #데이터 전송하기
        self.ser.write(hextxdata)
        time.sleep(1)
        
        #데이터 읽기
        self.resp_data = self.ser.readline()
        #print('data response:' + self.response_data)
        print(self.resp_data)    

    def csetnow(self,act_id):
        #송신 데이터
        txdata = [0xFE,0xEF]
        msglength = 6
        actnum = act_id & 0xFF
        msgtype = 0x80 + 8
        cmd_cset = 0x01
        data = 0x00
        data1 = 0x00
        crc = (msglength + actnum + msgtype + cmd_cset + data + data1)&0xFF
    
        txdata.append(msglength)
        txdata.append(actnum)
        txdata.append(msgtype)
        txdata.append(cmd_cset)
        txdata.append(data)
        txdata.append(data1)
        txdata.append(crc)
        print(txdata)    

        hextxdata = bytearray(txdata)
        print(hextxdata)
        
        #데이터 전송하기
        self.ser.write(hextxdata)
        time.sleep(0.1)
        
        #데이터 읽기
        self.resp_data = self.ser.readline()
        #print('data response:' + self.response_data)
        print(self.resp_data)        
 
    #param
    #@state     1:enable, 0:disable
    def ctrlenable(self,act_id,state):
        #송신 데이터
        txdata = [0xFE,0xEF]
        msglength = 4
        actnum = act_id & 0xFF
        msgtype = 0x80 + 4
        controlonoff = state & 0xFF
        
        crc = (msglength + actnum + msgtype + controlonoff)&0xFF
    
        txdata.append(msglength)
        txdata.append(actnum)
        txdata.append(msgtype)
        txdata.append(controlonoff)
        txdata.append(crc)
        print(txdata)    

        hextxdata = bytearray(txdata)
        print(hextxdata)
        
        #데이터 전송하기
        self.ser.write(hextxdata)
        #time.sleep(0.1)
        time.sleep(0.01)
        
        #데이터 읽기
        self.resp_data = self.ser.readline()
        #print('data response:' + self.response_data)
        print(self.resp_data)    

 
    def servocmd(self,act_id,angle,mvtime,stiffness,refresh):
        #송신 데이터
        txdata = [0xFE,0xEF]
        msglength = 9
        actnum = act_id & 0xFF
        msgtype = 0x05
        angle_L = angle & 0xFF
        angle_H = (angle>>8) & 0xFF
        movems_L = mvtime & 0xFF
        movems_H = (mvtime>>8) & 0xFF
        stiff = stiffness & 0xFF
        mode = refresh & 0xFF
        
        crc = (msglength + actnum + msgtype + angle_L + angle_H + movems_L + movems_H + stiff + mode)&0xFF
    
        txdata.append(msglength)
        txdata.append(actnum)
        txdata.append(msgtype)
        txdata.append(angle_L)
        txdata.append(angle_H)
        txdata.append(movems_L)
        txdata.append(movems_H)
        txdata.append(stiff)
        txdata.append(mode)
        txdata.append(crc)
        #print(txdata)    

        hextxdata = bytearray(txdata)
        #print(hextxdata)
        
        #데이터 전송하기
        self.ser.write(hextxdata)
        time.sleep(0.5)
        
        #데이터 읽기
        #self.resp_data = self.ser.readline()
        #print('data response:' + self.response_data)
        #print(self.resp_data)        

    def getAngle(self,act_id):
        print('angle get')
        #송신 데이터
        txdata1 = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 0x87
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata1.append(msglength)
        txdata1.append(actnum)
        txdata1.append(msgtype)
        txdata1.append(crc)
        print(txdata1)            
        
        hextxdata1 = bytearray(txdata1)
        print(hextxdata1)
        
        #데이터 전송하기
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(hextxdata1)
        #time.sleep(0.1)
        time.sleep(0.01)
        
        #데이터 읽기
        self.resp_data1 = self.ser.readline()
        print(self.resp_data1)

        #init value
        angle = 0
        agc = 0
        
        #값이 없을 때 에러 발생
        try:
            #ams 센서에 자석 반응이 있으면 1, 없거나 연결되지 않으면 0 리턴
            #angle = (self.resp_data1[8] * 0x100) + self.resp_data1[7]
            angle = (self.resp_data1[8]<<8) + self.resp_data1[7]
            print('real angle' + str(angle))
        except:
            print('angle read error,check to alive actuator')
        
        return angle

    def getAngleAgc(self,act_id):
        #print('angle get')
        #송신 데이터
        txdata1 = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 0x87
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata1.append(msglength)
        txdata1.append(actnum)
        txdata1.append(msgtype)
        txdata1.append(crc)
        #print(txdata1)            
        
        hextxdata1 = bytearray(txdata1)
        #print(hextxdata1)
        
        #데이터 전송하기
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(hextxdata1)
        #time.sleep(0.1)
        time.sleep(0.02)
        
        #데이터 읽기
        #self.resp_data1 = self.ser.readline()
        
        #self.resp_data1 = self.ser.read(10)
        #print(self.resp_data1)
        #self.resp_data1.clear()
        
        sumdata = bytearray()
        #print(type(sumdata))
        while(True):
            readdata = self.ser.read(1)
            #print(self.resp_data1)
            if not readdata:
                #print('end of read')
                break
                
            #sumdata.append(readdata)
            sumdata += bytearray(readdata)
            #print(readdata)
            #print("sumdata: ",sumdata)
        
        #init value
        angle = 0
        agc = 0
        
        if len(sumdata)>9 and sumdata[0] == 0xfe and sumdata[1] == 0xef :
        #if len(sumdata)>9:
        #if len(self.resp_data1)>9:
         #   try:
         #       #ams 센서에 자석 반응이 있으면 1, 없거나 연결되지 않으면 0 리턴
         #       #angle = (self.resp_data1[8] * 0x100) + self.resp_data1[7]
         #       print('test')
         #       print(sumdata)
         #       angle = int((sumdata[8]<<8) + sumdata[7])
         #       print('test')
         #       
         #       agc = int(sumdata[9])
         #       
         #       print('real angle:' + str(angle) +',agc:' + str(agc))
         #       #print(angle)
         #       #print(agc)
         #       
         #   #except:
         #   #    angle = 0
         #   #    agc = 0
         #   #    print('angle read error,check to alive actuator')
         #   print('test')
           
            #angle = int((sumdata[8]<<8) + sumdata[7])
            #angle = sumdata[8]<<8 + sumdata[7] 
            angle = (sumdata[8]*0x100) + sumdata[7]
            
            
            agc = sumdata[9]
            
            print('real angle:' + str(angle) +',agc:' + str(agc))
        else :
            print('error receive')

        return angle,agc
    

    #param
    #@state
    def controlbegin(self,act_id):
        #송신 데이터
        txdata = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 12
        
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata.append(msglength)
        txdata.append(actnum)
        txdata.append(msgtype)
        txdata.append(crc)
        #print(txdata)    

        hextxdata = bytearray(txdata)
        #print(hextxdata)
        
        #데이터 전송하기
        self.ser.write(hextxdata)
        #time.sleep(1.5)
        #time.sleep(0.1)
        time.sleep(0.01)
        
        #데이터 읽기
        self.resp_data = self.ser.readline()
        #print('data response:' + self.response_data)
        print(self.resp_data)

    def getTouch(self,act_id):
        #print('read touch')
        #송신 데이터
        txdata1 = [0xFE,0xEF]
        msglength = 3
        actnum = act_id & 0xFF
        msgtype = 0x94
        crc = (msglength + actnum + msgtype)&0xFF
    
        txdata1.append(msglength)
        txdata1.append(actnum)
        txdata1.append(msgtype)
        txdata1.append(crc)
        #print(txdata1)            
        
        hextxdata1 = bytearray(txdata1)
        #print(hextxdata1)
        
        #데이터 전송하기
        #self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(hextxdata1)
        time.sleep(0.01)
        
        #데이터 읽기
        self.resp_data1 = self.ser.read(13)
        #self.resp_data2 = self.ser.readline()
        #self.resp_data3 = self.ser.readline()
        
        #print(self.resp_data1)
        #print(self.resp_data2)
        #print(self.resp_data3)
        #print(self.resp_data1[10])
        
        if self.resp_data1[10] &0x01:
            #print('touched:1')
            return 1
        else:
            #print('not touched:0')
            return 0
        #print(type(self.resp_data))
        #print(self.resp_data[0])

    def serial_termination(self):
        self.ser.close()
        self.connected = False
        
        