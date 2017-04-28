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
from QuEST.TDC.SaveFile import SaveFile
from QuEST.UI.Messenger import Messenger
from QuEST.COM.ReceivedProcessor import ReceivedProcessor
from QuEST.COM.SendProcessor import SendProcessor
from QuEST.TDC.KeyHasher import KeyHasher
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
        #print("inside get data "+data)
        if (data==''):
            if(self.label_text=="Port No"):
                #print("default port COM3 chosen")
                data="COM3"
                return data
            elif (self.label_text=="Baud rate"):
                #print("default baud rate 38400 chosen")
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
        self.config(state=DISABLED)
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
        self.ui.stop_button.config(state=NORMAL)
        self.config(state=DISABLED)
        if(str(type(self.serial_reader))=="<class 'str'>"):
            print("initializing TDC")
            self.serial_reader=TDCReader() #initialize the serial reader
            port=self.ui.port_input.get_data()
            #print(port)
            self.serial_reader.port=port #set the port number
            self.serial_reader.baudrate=self.ui.baud_input.get_data() #set the baudrate
        if(self.all_data.tdc_reader==""):
            self.tdc_reader=TDCReaderThread(self.hash_queue,self.serial_reader) #initalize the reader thread
            self.tdc_reader.start() #start the thread
            self.all_data.tdc_reader=self.tdc_reader
            self.hasher=KeyHasher(self.all_data)
            self.hasher.start()
            self.all_data.hasher=self.hasher
            print("from start printing the type of tdc reader " + str(type(self.tdc_reader)))
            print(type(self.all_data.tdc_reader))
            self.display_ut=TextPadWriter(self.console.micro_time, self.all_data.ut) #initialize the thread to put the data in the textpad
            self.displaygoodut=TextPadWriter(self.console.good_utime, self.all_data.good_ut)
            self.display_ut.start() #start putting the data in the textpad
            self.displaygoodut.start()
            
        
class StopButton(Button):        
    def __init__(self,master, alldata):
        Button.__init__(self,master,text="Stop",command=self.stop,width=12)
        self.serial_reader=alldata.tdc_reader
        self.alldata=alldata
        print(type(self.serial_reader))
        self.saver=master.saver
        self.config(state=DISABLED)
        self.start_button=master.start_button
    def stop(self):
        pass
        print("Stopping to read from TDC")
        self.saver.config(state=NORMAL)
        self.config(state=DISABLED)
        self.start_button.config(state=NORMAL)
        print("inside stop button")
        self.serial_reader=self.alldata.tdc_reader
        print((str(type(self.serial_reader))=="<class 'str'>"))
        if(~(str(type(self.serial_reader))=="<class 'str'>")): 
            print(type(self.serial_reader))
            if(self.serial_reader.is_alive()):
                self.serial_reader.stop_reading()
                self.serial_reader.join()
                self.alldata.tdc_reader=""
                
            
        
class ConnectButton(Button):        
    def __init__(self,master,all_data):
        Button.__init__(self,master,text="Connect",command=self.connect,width=12)
        self.ui=master
        self.alldata=all_data
        self.receiver=all_data.receiver
        self.encrypt_socket=all_data.encrypt_socket
        self.received_data=all_data.received_data
        self.sender=all_data.sender
        self.receivedprocessor=all_data.receivedprocessor
        self.send_data=all_data.send_data
        
    def connect(self):
        self.disconnect=self.ui.disconnect
        self.communicate=self.ui.start_sending
        self.messenger_button=self.ui.messenger
        self.config(state=DISABLED)
        self.disconnect.config(state=NORMAL)
        self.communicate.config(state=NORMAL)
        self.messenger_button.config(state=NORMAL)
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
        self.receivedprocessor=ReceivedProcessor(self.alldata)
        self.receivedprocessor.start()
        self.sender=Sender_Thread(tosend=self.send_data,send_socket=self.encrypt_socket)
        self.sender.start()
        
        
        
class DisconnectButton(Button):        
    def __init__(self,master,all_data):
        Button.__init__(self,master,text="Disconnect",command=self.disconnect,width=12)
        self.sockettoclose=all_data.encrypt_socket
        self.sendprocessor=all_data.sendprocessor
        self.receiver=all_data.receiver
        self.receivedprocessor=all_data.receivedprocessor
        self.sender=all_data.sender
        self.messenger=all_data.messenger
        self.config(state=DISABLED)
        self.master=master
        
        # to make all queues empty here
        
        
        #self.send_thread=all_data.
    def disconnect(self):
        self.connect=self.master.connect
        self.communicate=self.master.start_sending
        self.messenger_button=self.master.messenger
        print("disConnecting to the server/client")
        self.connect.config(state=NORMAL)
        self.config(state=DISABLED)
        self.communicate.config(state=DISABLED)
        self.messenger_button.config(state=DISABLED)
        if(self.messenger==""):
            pass
        else:
            self.messenger.destroy()
        self.sendprocessor.off()
        self.receiver.off()
        self.receivedprocessor.off()
        self.sender.off()
        
        self.sockettoclose.close()
        
        
class StartSendingButton(Button):        
    def __init__(self,master,alldata):
        Button.__init__(self,master,text="Error Check",command=self.send,width=12)
        self.alldata=alldata
        self.sendprocessor=alldata.sendprocessor
        self.config(state=DISABLED)
    def send(self):
        pass
        print("Communicating with the other lab")
        self.sendprocessor=SendProcessor(self.alldata)
        self.sendprocessor.start()
        
        
class MessengerButton(Button):
    def __init__(self,master, alldata):
        Button.__init__(self,master,text="Messenger",command=self.start_messenger,width=12)
        self.alldata=alldata
        self.messenger=alldata.messenger
        self.config(state=DISABLED)
    def start_messenger(self):
        pass
        print("Starting the messenger")
        self.messenger=Messenger(self.alldata)
        self.messenger.mainloop()
class SaveButton(Button):
    def __init__(self,master, alldata):
        Button.__init__(self,master,text="Save",command=self.start_save,width=12)
        self.save_data=alldata.save_data
        self.config(state=DISABLED)
    def start_save(self):
        pass
        print("Starting to save")
        self.config(state=DISABLED)
        self.saver=SaveFile(self.save_data)
        self.saver.start()
        
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
        while(1):
            if(~self.data_queue.empty()):
                data=self.data_queue.get()
                self.text_pad.insert(END,data)
                self.text_pad.insert(END,"\n")
                self.text_pad.see(END)
                self.data_queue.task_done() 
                
                        
