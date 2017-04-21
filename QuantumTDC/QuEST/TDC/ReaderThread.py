'''
Created on Apr 12, 2017
**************************

deprecated--- s00n will be replaced and deleted



@author: Quest10
'''
from threading import Thread
import time
from queue import Queue
from threading import Lock
from QuEST.TDC import SerialReader


class ReaderThread(Thread):
    '''
    classdocs
    '''


    def __init__(self, time_queue, send_queue, tdc_serial, reader_switch):
        '''
        Constructor
        '''
        self.time_queue=time_queue
        self.send_queue=send_queue
        #self.lock=Lock()
        self.tdc_serial=tdc_serial
        self.tdc_serial.start_TDC()
        self.reader_switch=reader_switch
        Thread.__init__(self)
        
        
    def run(self):
        self.start_reading()
    
    def start_reading(self):
        while(self.reader_switch=="True"):
            data=self.tdc_serial.read_line()
            print(data)
            self.time_queue.put(data)
            self.send_queue.put(data)
            
    def stop_reading(self):
        self.reader_switch="False"
            
            