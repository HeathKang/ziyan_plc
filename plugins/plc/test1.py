#!/usr/bin/python

"""

https://sourceforge.net/projects/libnodave/

ref: LOGO.py

https://support.industry.siemens.com/tf/ww/en/posts/python-libnodave-and-logo-oba7/89994/?page=0&pageSize=10

"""

import os

import ctypes

daveProtoPPI = 10 # PPI for S7 200 
daveProtoAS511 = 20 # S5 programming port protocol 
daveProtoS7online = 50 # use s7onlinx.dll for transport 
daveProtoISOTCP = 122 # ISO over TCP */
daveProtoISOTCP243 = 123 # ISO over TCP with CP243 */
daveProtoISOTCPR = 124 # ISO over TCP with Routing */
daveSpeed9k = 0
daveSpeed19k = 1
daveSpeed187k = 2
daveSpeed500k = 3
daveSpeed1500k = 4
daveSpeed45k = 5
daveSpeed93k = 6
daveBlockType_OB = '8'
daveBlockType_DB = 'A'
daveBlockType_SDB = 'B'
daveBlockType_FC = 'C'
daveBlockType_SFC = 'D'
daveBlockType_FB = 'E'
daveBlockType_SFB = 'F'


class PLC(object):
    """
    libnodave ctypes wrapper
    """
    
    def __init__(self, ip, port):
        """ init """
        self.ip = ip
        self.port = port
        self.ph = 0         # Porthandle
        self.di = 0         # Dave Interface Handle
        self.dc = 0
        self.res = 1
        self.rack = 0       # Verbindung nicht O.K. bei Start
        self.slot = 2
        self.mpi = 2        # MPI
        self.dave = ""
        self.daveDB = 132
        #Pfad zur DLL
        
        #DLL_LOC = Dateipfad + '/' + ('libnodave.so')
        
        APPDIR = os.path.dirname(os.path.abspath(__file__))

        if os.name == 'nt':
            DLL_LOC = os.path.join(APPDIR, 'libnodave', 'win', 'libnodave.dll')        
            self.dave = ctypes.windll.LoadLibrary(DLL_LOC)
        if os.name == 'posix':
            #Dateipfad = os.getcwd() 
            #DLL_LOC = Dateipfad + '/' + ('libnodave.so')
            DLL_LOC = os.path.join(APPDIR, 'libnodave.so')        
            self.dave = ctypes.cdll.LoadLibrary(DLL_LOC)

    def connect(self):        
        """ Open connection """
        print("connect ...")
        self.ph = self.dave.openSocket(self.port, self.ip)
        if self.ph > 0:
            print("Port Handle OK.")
        else:
            print("Port Handle Not OK.")
            raise(Exception("can't open connection"))
            
        # Dave Interface handle
        self.di = self.dave.daveNewInterface(self.ph, self.ph, 'IF1', 0,  daveProtoISOTCP , daveSpeed187k)
        print ("Dave Interface Handle :%s" % self.di)
        
        # Init Adapter
        self.res = self.dave.daveInitAdapter(self.di)
        if self.res == 0:
            print("Init Adapter OK.")
        else:
            print("Init Adapter Not OK.")
            
            
        # dave Connection
        self.dc = self.dave.daveNewConnection(self.di, self.mpi, self.rack, self.slot )       # daveNewConnection(di, MPI, rack, slot)
        print("Dave Connection: %d" % self.dc)
        
        self.res = self.dave.daveConnectPLC(self.dc)
        self.dave.daveSetTimeout(self.di, 5000000)
        print("res: %s" % self.res)
        
    def readbytes(self, db, start, dlen):
        """ read """
        
        print ("- read")
        if self.res == 0:
            rd = self.dave.daveReadBytes(self.dc, self.daveDB ,db,start,dlen, 0)
            print rd
            if rd != 0:
                raise(Exception('no pointer set'))
            print ("ReadBytes: %s" % dlen) #+ str(self.res)
            for z in range(dlen):                
                a=self.dave.daveGetU16(self.dc)
                print z," ", a
            
        else:
            print ("please connect")
            
    def writebytes(self, db, wort, wert):
        """ write """
        
        print ("- write")
        u=self.dave.daveSwapIed_16(wert) 
        buffer = ctypes.c_int(int(u))
        buffer_p =  ctypes.pointer(buffer)        
        a = self.dave.daveWriteManyBytes(self.dc, self.daveDB, db, wort,2, buffer_p)
    
    def disconnect(self):
        """ disconnect """
        
        self.dave.daveDisconnectPLC(self.dc);
        self.dave.closePort(self.ph)
        print("- PLC disconnected")


def main():
    """ for test """
    host = "192.168.1.10"
    #host = "127.0.0.1"
    plc = PLC(host,102)
    plc.connect()
    plc.readbytes(11,4,2)  #(start_add,offset)
    plc.writebytes(11,4,124) #(db,start_add,offset)
    '''
        
    
    '''
    

    #plc.readbytes(11,0,6)

    plc.disconnect()

if __name__ == '__main__':
    
    main()










