'''
Created on Apr 13, 2017

@author: jee11
'''
from threading import Thread

class TDCReaderThread(Thread):
    '''
    classdocs
    '''


    def __init__(self, time_queue,send_queue,tdc_reader):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.time_queue=time_queue
        self.send_queue=send_queue
        self.tdc_reader=tdc_reader
        self.tdc_switch="True"
        self.tdc_reader.start_TDC()
        
    def run(self):
        self.start_reading()
        
    def start_reading(self):
        while(self.tdc_switch=="True"):
            data=self.tdc_reader.readline()
            print(data)
            self.time_queue.put(data)
            self.send_queue.put(data)
            
    def stop_reading(self):
        self.tdc_switch="False"
        