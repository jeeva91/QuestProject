'''
Created on Apr 13, 2017

@author: jee11
'''
from tkinter import Frame, IntVar
from tkinter import Label
from tkinter import Entry
from tkinter import *
from threading import Thread
from QuEST.TDC.TDCReader import TDCReader
from QuEST.TDC.TDCReaderThread import TDCReaderThread
from QuEST.COM.My_TCP import My_TCP
from QuEST.COM.Receiver_Thread import Receiver_Thread
from QuEST.COM.Sender_Thread import Sender_Thread
class InputFrame(Frame):
    def __init__(self,master,label_text="label"):
        Frame.__init__(self, master,width=350,height=70)
        #print(self.winfo_height())
        #print(self.winfo_width())
        self.label_text=label_text
        self.label=Label(self,text=label_text,width=12)
        self.entry=Entry(self,width=10)
        self.label.pack(side=LEFT)
        self.entry.pack(side=RIGHT)
    def get_data(self):         
        data=self.entry.get()
        print("inside get data "+data)
        if (data==''):
            if(self.label_text=="Port No"):
                print("default port COM3 chosen")
                data="COM3"
                return data
            elif (self.label_text=="Baud rate"):
                print("default baud rate 38400 chosen")
                data=38400
                return data
            else: return data
    
class CheckBoxFrame(Frame):
    def __init__(self,master,label_text="server"):
        Frame.__init__(self,master,width=350,height=70)
        #self.label=Label(self,text=label_text).pack(side=LEFT)
        self.value=IntVar()
        self.checkbox=Checkbutton(self,text=label_text,variable=self.value)
        self.checkbox.pack()
        
    def getvalue(self):
        return self.value.get()
        
class ChangeButton(Button):        
    def __init__(self,master,all_data):
        Button.__init__(self,master,text="Change",command=self.change,width=12)
        self.tdc_reader=all_data.tdc_reader
    def change(self):
        pass
        print("Changed clicked")
        
class StartButton(Button):        
    def __init__(self, master, console, all_data):
        Button.__init__(self, master, text="Start", command=self.start, width=12)
        print(type(master))
        self.ui=master
        self.console=console
        self.all_data=all_data
        self.hash_queue=all_data.hash_queue
        self.tdc_reader=all_data.tdc_reader
        self.serial_reader=""
    def start(self):
        pass
        print("Starting to read from TDC")
        if(str(type(self.serial_reader))=="<class 'str'>"):
            print("initializing TDC")
            self.serial_reader=TDCReader() #initialize the serial reader
            self.serial_reader.port=self.ui.port_input.get_data() #set the port number
            self.serial_reader.baudrate=self.ui.baud_input.get_data() #set the baudrate
        if(str(type(self.tdc_reader))=="<class 'str'>"):
            self.tdc_reader=TDCReaderThread(self.hash_queue,self.serial_reader) #initalize the reader thread
            self.tdc_reader.start() #start the thread
            self.display_ut=TextPadWriter(self.console.micro_time, self.all_data.ut) #initialize the thread to put the data in the textpad
            self.displaygoodut=TextPadWriter(self.console.good_utime, self.all_data.good_ut)
            self.display_ut.start() #start putting the data in the textpad
            self.displaygoodut.start()
            
        
class StopButton(Button):        
    def __init__(self,master, alldata):
        Button.__init__(self,master,text="Stop",command=self.stop,width=12)
        self.serial_reader=alldata.tdc_reader
    def stop(self):
        pass
        print("Stopping to read from TDC")
        if(~(str(type(self.serial_reader))=="<class 'str'>")): 
            if(self.serial_reader.is_alive()):
                self.serial_reader.stop_reading()
                self.serial_reader.join()
                self.serial_reader=""
                
            
        
class ConnectButton(Button):        
    def __init__(self,master,all_data):
        Button.__init__(self,master,text="Connect",command=self.connect,width=12)
        self.ui=master
        self.receiver=all_data.receiver
        self.encrypt_socket=all_data.encrypt_socket
        self.received_data=all_data.received_data
        self.sender=all_data.sender
        self.send_data=all_data.send_data
    def connect(self):
        pass
        print("Connecting to the server/client")
        self.IP=self.ui.IP_input.get_data()
        self.if_server=self.ui.if_server.getvalue()
        if(self.if_server):
            self.con_type="server"
        else:
            self.con_type="client"
        self.encrypt_socket=My_TCP(ip=self.IP,port=5005,con_type=self.con_type).my_socket
        print("connected", self.encrypt_socket)
        self.receiver=Receiver_Thread(received=self.received_data,rcv_socket=self.encrypt_socket)
        self.receiver.start()
        self.sender=Sender_Thread(tosend=self.send_data,send_socket=self.encrypt_socket)
        self.sender.start()
        
        
class DisconnectButton(Button):        
    def __init__(self,master,all_data):
        Button.__init__(self,master,text="Disconnect",command=self.disconnect,width=12)
        self.sockettoclose=all_data.encrypt_socket
        #self.send_thread=all_data.
    def disconnect(self):
        pass
        print("disConnecting to the server/client")
        self.sockettoclose.close()
        
        
class StartSendingButton(Button):        
    def __init__(self,master,mytcpsocket):
        Button.__init__(self,master,text="Communicate",command=self.send,width=12)
        self.mytcpsocket=mytcpsocket
    def send(self):
        pass
        print("Communicating with the other lab")        
        
class ConsoleFrame(Frame):
    def __init__(self,master, console_name="micro time"):
        Frame.__init__(self,master)
        self.label=Label(self,text=console_name)
        self.console=Text(self,width=30)
        self.label.pack()
        self.console.pack()
        
class TextPadWriter(Thread):
    def __init__(self, text_pad, data_queue):
        self.data_queue=data_queue
        self.text_pad=text_pad.console
        Thread.__init__(self)
        self.setDaemon(True)
    def run(self):
        pass
        self.display()
    def display(self,):
        counter=0
        while(1):
            #self.text_pad.insert(END,counter)
            #self.text_pad.see(END)
            #counter=counter+1
            if(~self.data_queue.empty()):
                data=self.data_queue.get()
                self.text_pad.insert(END,data)
                self.text_pad.see(END)
                self.data_queue.task_done() 
                
                        
