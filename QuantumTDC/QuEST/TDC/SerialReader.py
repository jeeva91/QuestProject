'''
Created on Mar 15, 2017
**************



Deprecated

**************

@author: jee11
'''
import serial 
class SerialReader(object):
    '''
    classdocs
    '''
    


    def __init__(self, port, baudrate=38400):
        
        '''Constructor
        '''
        self.__tdc_serial=serial.Serial()           #serial object creation
        self.__tdc_serial.baudrate=baudrate         #set the baudrate
        self.__tdc_serial.port=port                 #set the port number
        
    def change_baudrate(self, baudrate):
        '''Changes the baudrate of the serial port
        '''
        self.__tdc_serial.baudrate=baudrate
        
    def change_port(self, port):
        '''Change the port number of the serial port
        '''
        self.__tdc_serial.port=port
    
    def read_line(self):
        '''Read line of the given size
        '''
        return self.__tdc_serial.readline()
    
    def read(self, size):
        '''Read the given size
        '''
       # print("inside read")
        
        return self.__tdc_serial.read(size)
    
    def start_TDC(self):
        '''Open the serail port
        '''
        self.__tdc_serial.open()
        print(self.__tdc_serial.is_open)
        print(self.__tdc_serial)
        
    def stop_TDC(self):
        '''Close the serial port
        '''
        self.__tdc_serial.close()
        
    
        