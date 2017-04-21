'''
Created on Mar 15, 2017

************************

Deprecated

*************************

@author: jee11
'''
from tkinter import *
from QuEST.TDC.SerialReader import SerialReader
from QuEST.TDC.ReaderThread import ReaderThread
from queue import Queue
from threading import Thread
import unicodedata
from QuEST.TDC import Received_Processor
from QuEST.TDC import Receiver_Thread
from QuEST.TDC import Sender_Thread
from QuEST.TDC import My_TCP
from threading import Lock

time_dict={"0":0}
time_queue=Queue(0)
time_counter=0
reader_switch="True"


server_send=Queue(0)
send_lock=Lock()
server_receive=Queue(0)
receive_lock=Lock()
server_socket=My_TCP.My_TCP("155.246.109.84",5005,"server")

server_sender=Sender_Thread.Sender_Thread(server_send,server_socket.conn,lock=send_lock)
server_receiver=Receiver_Thread.Receiver_Thread(server_receive,server_socket.conn,lock=receive_lock)


server_receive_processor=Received_Processor.Received_Processor(server_receive,con_type="server",lock=receive_lock)

server_sender.start()
server_receiver.start()

server_receive_processor.start()


tdc_serial=SerialReader(port='COM3',baudrate=38400)

#def read_line(time_queue,tdc_serial,time_dict,time_counter):
 #   tdc_serial.start_TDC()
  #  while(1):
   #     #print("inside reader")
    #    
     #   data=tdc_serial.read_line()
      #  print(data)        
       # time_queue.put(data)
        #time_counter=+1
        #if (int.from_bytes(data, byteorder='big',signed=False))>0:
         #   pass
          #  temp_dict={time_counter: data}
           # time_dict.update(temp_dict)
        
#reader_thread=Thread(target=read_line,args=(time_queue,tdc_serial,time_dict,time_counter))
#reader_thread.setDaemon(True)


reader_thread=ReaderThread(time_queue,tdc_serial,reader_switch)
reader_thread.reader_switch="True"

root=Tk()
root.title("QuEST TDC")


welcome_label=Label(root, text="Welcome to QuEST TDC")
welcome_label.pack(side=TOP)

serial_frame=Frame(root)
serial_frame.pack()

baudrate_entry=Entry(serial_frame,text="Baudrate").pack()

port_entry=Entry(serial_frame,text="Port Number").pack()


serial_button_frame=Frame(serial_frame)
serial_button_frame.pack()

serial_change_button=Button(serial_button_frame,text="Change",).pack()
serial_start_button=Button(serial_button_frame,text="Start", command=reader_thread.start).pack()
serial_stop_button=Button(serial_button_frame, text="Stop", command=reader_thread.stop_reading).pack()




text_pad_frame=Frame(root)
text_pad_frame.pack(side="right")



text_pad=Text(text_pad_frame, width=13, height=50)
text_pad.pack()
#text_pad.insert(END,"hI")



#tdc_serial.start_TDC()


        
        
def print_to_pad(time_queue):
    
    while(1):
        data=time_queue.get()
        text_pad.insert(END,data)
        text_pad.see(END)
        #text_pad.after(50,print_to_pad,args=(time_queue))
        time_queue.task_done()

#reader_thread.start()
#text_pad.after(1,print_to_pad,args=(time_queue,))
print_thread=Thread(target=print_to_pad,args=(time_queue,))
print_thread.setDaemon(True)
print_thread.start()
root.mainloop()
    
    
