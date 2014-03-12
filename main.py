'''
Created on Feb 5, 2014

@author: Scott R Phelps '1tguy'

A dashboard to control a robot named KIP
'''
import Tkinter
import serial
import ttk
import tkMessageBox
#import cv2



class kipControl(Tkinter.Tk):
    btnClicked=0  # Used for Select button of Com Port
    
  
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.geometry('600x365+200+200')
        
        self.afterId=None
        
        self.bind("<KeyPress-w>", self.startMotion)
        self.bind("<KeyPress-s>", self.startMotion)
        self.bind("<KeyPress-a>", self.startMotion)
        self.bind("<KeyPress-d>", self.startMotion)
        self.bind("<KeyRelease>", self.stopMotion)
        
        
        

    def initialize(self):
        self.grid()
        comSelect = ["ttyACM0","ttyACM1","ttyACM2","tty.usbmodem1411"]
        self.comSelected=Tkinter.Variable()
        self.box = ttk.Combobox(self.parent,values=comSelect,textvariable=self.comSelected)
        self.box.state(['readonly'])
        self.box.grid(column=0,row=0,sticky='EW')
        
        baudSelect = ["9600","14400","19200","28800","38400","57600","115200"]
        self.baudSelected=Tkinter.Variable()
        self.bbox = ttk.Combobox(self.parent,values=baudSelect,textvariable=self.baudSelected)
        self.bbox.state(['readonly'])
        self.bbox.grid(column=0,row=1,sticky='EW')
        
        buttonSelect = Tkinter.Button(self,text="Select",command=self.OnButtonClick)
        buttonSelect.grid(column=1,row=0,rowspan=2)
        
        buttonExit = Tkinter.Button(self,text="Quit",command=self.quit)
        buttonExit.grid(column=5,row=5)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=2,sticky='EW')
        self.labelVariable.set("Waiting for connection...")
        
        buttonFwd = Tkinter.Button(self,text="Forward",command=lambda: self.driveDir(1, 0, 0, 0)) # Use lambda: to use parameters of a function
        buttonFwd.grid(column=3,row=2)
        buttonLft = Tkinter.Button(self,text="Left",command=lambda: self.driveDir(0, 0, 1, 0))
        buttonLft.grid(column=2,row=3)
        
        buttonRgt = Tkinter.Button(self,text="Right",command=lambda: self.driveDir(0, 0, 0, 1))
        buttonRgt.grid(column=4,row=3)
        
        buttonRev = Tkinter.Button(self,text="Reverse",command=lambda: self.driveDir(0, 1, 0, 0))
        buttonRev.grid(column=3,row=4)
        
        buttonStop = Tkinter.Button(self,text="STOP",bg="red",command=self.processStop)
        buttonStop.grid(column=1,row=5,columnspan=2,sticky='EW')
        
        videoFrame = Tkinter.Frame(width=200,height=200,bg="black")
        videoFrame.grid(column=0,row=5)
        
        videoBtn = Tkinter.Button(self, text="Video")
        videoBtn.grid(column=0,row=6)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)
        
        
    def OnButtonClick(self):
    
        self.labelVariable.set(self.comSelected.get()+" - Serial Port Input Received")
        kipControl.btnClicked=1
        
    def driveDir(self, fwd, bkwd, lft, rgt):
        
        if kipControl.btnClicked == 1:
            
            ser = serial.Serial(port="/dev/"+ self.comSelected.get(),baudrate=self.baudSelected.get(),timeout=0)
          
            if fwd:
                ser.write("w")
            
            elif bkwd: 
                ser.write("s")
            
            elif lft: 
                ser.write("a")
            
            elif rgt: 
                ser.write("d")   
            
        else:
            
            tkMessageBox.showinfo("Error", "Select Com Port!")
            

    def OnPressEnter(self,event):
        self.labelVariable.set(self.comSelected.get()+" - Serial Port Input Received")
        
    def startMotion(self, event):
        
        if self.afterId != None:
            self.after_cancel(self.afterId)
            self.afterId = None
            
        elif kipControl.btnClicked == 0:
                tkMessageBox.showinfo("Error", "Select Com Port!")
             
        else:
            ser = serial.Serial(port="/dev/"+ self.comSelected.get(),baudrate=self.baudSelected.get(),timeout=0)
            if event.char == "w":
                ser.write("w")
               
            if event.char == "s":
                ser.write("s")
                
            if event.char == "a":
                ser.write("a")
               
            if event.char == "d":
                ser.write("d")
               
        
    def stopMotion(self, event):
        self.afterId = self.after_idle(self.processStop)
        
    def processStop(self):
        ser = serial.Serial(port="/dev/"+ self.comSelected.get(),baudrate=self.baudSelected.get(),timeout=0)
        
        ser.write("q")
        
        self.afterId = None
        
#     def camView(self):
#         vc = cv2.VideoCapture(0)
#         
#         if vc.isOpened():
#             rval, frame = vc.read()
#         else:
#             rval = False
#         while rval:
#             #cv2.imshow(self.videoFrame, frame)
#             
#             rval, frame = vc.read()
#             key = cv2.waitKey(20)
#             if key ==27:
#                 break
        

    
        
if __name__ == "__main__":
    app = kipControl(None)
    app.title('KIP Control Panel v.01')
    app.mainloop()
