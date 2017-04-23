'''
Created on Apr 19, 2017

@author: jee11
'''
from queue import Queue
from _overlapped import NULL
from QuEST.TDC.TDCReaderThread import TDCReaderThread

class EncrptorData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ut=Queue(0)            #display
        self.good_ut=Queue(0)       #display
        self.goot_utsend=Queue(0)   #send processor
        self.received_data=Queue(0) #receiver and processor
        self.hash_queue=Queue(0)    #hasher
        self.send_data=Queue(0)     #for tcp sending
        self.encrypt_socket=""
        self.tdc_serial=""
        self.tdc_reader=""
        self.receiver=""
        self.displaymessage=Queue(0) #to display message
        self.key={"":0}
        