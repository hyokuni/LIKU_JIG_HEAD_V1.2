import serial.tools.list_ports as sp

class portfinder:
    def __init__(self):
        comportlist = sp.comports()
        JigPort = []

    def refresh(self):
        comportlist = sp.comports()
    
    def getport(self):
        comportlist = sp.comports()
        JigPort = []

        for port, desc, hwid in sorted(comportlist):
            #print("%s" % (port))
            #print("%s" % (hwid))
            
            vidpid_pos = hwid.find('=')
            vidpid =hwid[vidpid_pos+1:vidpid_pos+10]
            #print(vidpid)
            
            if vidpid == '0403:6001':
                JigPort.append(port)
  
            #최종 횟수
            CntOfconnetedport = 0
            CntOfconnetedport = len(JigPort)

        if not CntOfconnetedport == 1:
            print("2개 이상의 시리얼 포트가 감지되었습니다")
            
        else:
            print("시리얼 포트를 찾았습니다!")
            print(JigPort)
            return True, JigPort[0]
        
        return False, 'FAIL'
        

