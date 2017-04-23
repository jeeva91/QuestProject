'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread, Lock
from queue import Queue

class ReceivedProcessor(Thread):
    '''
    classdocs
    '''


    def __init__(self, received=Queue(),lock=Lock()):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.received=received
        self.lock=lock
        
    def run(self):
        self.process()
        
    def process(self):
        while(True):
            if(~self.received.empty()):
                bytedata=self.received.get()
                data=bytedata.decode('utf-8')
                command=data.partition(" ")
                if(command[0]=="goodut"):
                    pass
                    self.process_goodut(command[2])
                elif(command[0]=="stop"):
                    self.process_stop()
                elif(command[0]=="XOR"):
                    self.process_CRC(command[2])
                elif(command[0]=="message"):
                    self.process_message(command[2])
    
    def process_goodut(self, mygooduts):
        pass
    def process_stop(self):
        pass
    def process_CRC(self,mycrcdata):
        pass
    def process_message(self,enc_message):
        pass           
        
        