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
        self.ut=Queue(0)
        self.good_ut=Queue(0)
        self.received_data=Queue(0)
        self.send_data=Queue(0)
        self.encrypt_socket=""
        self.tdc_serial=""
        self.tdc_reader=""
        self.receiver=""
        