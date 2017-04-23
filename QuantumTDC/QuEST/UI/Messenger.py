'''
Created on Apr 21, 2017

@author: jee11
'''
from tkinter import Tk, Text, Frame, Entry, Button
from tkinter.constants import TOP, LEFT, RIGHT, END, BOTTOM
from QuEST.UI import UIWidgets
from threading import Thread, Lock
from queue import Queue
import time

class Messenger(Tk):
    '''
    classdocs
    '''


    def __init__(self,alldata):
        '''
        Constructor
        '''
        Tk.__init__(self)
        self.title("QuEST Messenger")
        self.send_queue=alldata.send_queue
        self.messagepad=Text(self)
        self.messagepad.pack(side=TOP)
        self.displaymessage=alldata.displaymessage
        self.sendframe=SendFrame(self,self.send_queue)
        self.sendframe.pack(side=BOTTOM)
        self.display=DisplayThread(self,textpad=self.messagepad,messagequeue=self.displaymessage)
        self.display.start()
        
        
        
    
        
        
    
        
        
class SendFrame(Frame):
    
    def __init__(self,master,send_queue):
        Frame.__init__(master)
        self.send_queue=send_queue
        self.entry=Entry(self,width=25)
        self.sendbutton=Button(self,command=self.send,text="Send",width=12)
        self.entry.pack(side=LEFT)
        self.sendbutton.pack(side=RIGHT)
        
    def send(self):
        to_send=self.entry.get()
        self.send_queue.put(to_send)
        
        
class DisplayThread(Thread):
    
    def __init__(self,textpad=Text(),messagequeue=Queue(0)):
        Thread.__init__(self)
        self.messagequeue=messagequeue
        self.textpad=textpad
        
    def run(self):
        self.display()
        
    def display(self):
        while(1):            
            if(~self.messagequeue.empty()):
                data=self.messagequeue.get()
                self.textpad.inset(END,data)
                self.textpad.see(END)
                self.messagequeue.task_done()
                time.sleep(1)
                
            
    
        
        
        

        
        
            