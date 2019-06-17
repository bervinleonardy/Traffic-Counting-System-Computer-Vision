from imutils.video import FPS
import numpy
import os
from pygame import mixer
import time
import cv2
import imutils
from tkinter import *
import tkinter.messagebox
import tkinter.ttk
import tkinter.filedialog

root=Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Traffic Counting System')
root.iconbitmap(r'D:\Skripsi Opick\GITHUB_WORKFLOW\Opencv_Traffic_Counting_System\icon.ico')
frame.config(background='light blue')
label = Label(frame, text="Monitoring Traffic Counting System",bg='light blue',font=('Times 20 bold'))
label.pack(side=TOP)
filename = PhotoImage(file="D:\Skripsi Opick\GITHUB_WORKFLOW\Opencv_Traffic_Counting_System\login-bg.png")
background_label = Label(frame,image=filename)
background_label.pack(side=TOP)



def hel():
   help(cv2)

def Contri():
   tkinter.messagebox.showinfo("Contributors","\nBLAXTECH \n")


def anotherWin():
   tkinter.messagebox.showinfo("About",'Driver Cam version v13.80.853.0\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3')

def driverDetails():
   tkinter.messagebox.showinfo("Information Details",
   '======== Start of device information ========\n	    Device name:           Logitech HD Webcam C310\n	    USB Vendor ID (VID):   0x046D\n	    USB Product ID (PID):  0x081B\n	    USB Revision (BCD):    0x0012\n	    Firmware Version:      7.1.1011\n	    Firmware CRC:          0xF3E0\n	    EEPROM Version:        1.27\n	    Sensor Type:           2.0\n	    Driver Version:        13.80.853.0\n======== End of device information ========\n')                                    
   

menu = Menu(root)
root.config(menu=menu)

subm1 = Menu(menu)
menu.add_cascade(label="Tools",menu=subm1)
subm1.add_command(label="Open CV Docs",command=hel)

subm2 = Menu(menu)
menu.add_cascade(label="About",menu=subm2)
subm2.add_command(label="Contributors",command=Contri)
subm2.add_command(label="Driver Cam",command=driverDetails)

subm3 = Menu(menu)
menu.add_cascade(label="Information Details",menu=subm3)
subm3.add_command(label="About",command=anotherWin)



def keluar():
   exit()
  
def deteksi_kamera():
   # initialize the video writer (we'll instantiate later if need be)
   writer = None

   # initialize the frame dimensions (we'll set them as soon as we read
   # the first frame from the video)
   W = None
   H = None   
   kamera =cv2.VideoCapture(0)
   pesan = tkinter.messagebox.askyesno("Info","\nApakah ingin menggunakan file video? \n")
   while pesan == False:
         ret,frame=kamera.read()
         if frame is None :
            tkinter.messagebox.showwarning("Kesalahan","\nKamera tidak terdeteksi \n")
            break      
         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         cv2.imshow('Kamera',frame)
         if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
   kamera.release()
   cv2.destroyAllWindows()
   while pesan == True:
      filevideo = tkinter.filedialog.askopenfilename(initialdir = "/",title = "Pilih file",filetypes = (("file video","*.AVI"),("all files","*.*")))
      filebuka = os.path.abspath(os.path.expanduser(os.path.expandvars(filevideo)))
      print(filebuka)
      bacavideo = cv2.VideoCapture(filebuka)
      # Check if camera opened successfully
      if (bacavideo.isOpened()== False): 
         tkinter.messagebox.showwarning("Kesalahan","\n Error membuka stream video \n")      
      while(bacavideo.isOpened()== True):
         ret, frame = bacavideo.read()
         if ret == True:
            cv2.imshow('Kamera',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
               break
         # Break the loop
         else: 
            break               
      bacavideo.release()
      cv2.destroyAllWindows()
      tkinter.messagebox.showinfo("Info","\n Stream video selesai \n") 
      return(Menu)
   else:   
      tkinter.messagebox.showwarning("Kesalahan","\n Tidak Ada File \n")
   return(Menu)

def kamera_rekam():
   # initialize the video writer (we'll instantiate later if need be)
   tulis = None

   # initialize the frame dimensions (we'll set them as soon as we read
   # the first frame from the video)
   W = None
   H = None   
   filerekam = tkinter.filedialog.asksaveasfilename(defaultextension=".avi",filetypes = (("video","*.avi"),("all files","*.*")))   
   # pathrekam = os.path.abspath(os.path.expanduser(os.path.expandvars(filerekam)))
   # print(pathrekam)
   if filerekam is None: 
      return   
   rekam =cv2.VideoCapture(0)
   frame = rekam.read()
   frame = frame[1]
   f_height, f_width, _ = frame.shape
   print (f_height , f_width) 
   fps = FPS().start()
   # fourcc=cv2.VideoWriter_fourcc(*'MJPG') 
   # tulis=cv2.VideoWriter(filerekam,fourcc,30,(fwidth,fheight))
   while (rekam.isOpened()):
      frame=rekam.read()
      frame = frame[1]
      if frame is None:
         break          
      frame = imutils.resize(frame, width=640)
      # if the frame dimensions are empty, set them
      if W is None or H is None:
         (H, W) = frame.shape[:2]  
      if filerekam is not None and tulis is None:
         fourcc = cv2.VideoWriter_fourcc(*"MJPG")
         tulis = cv2.VideoWriter(filerekam, fourcc, 30,
               (W, H), True)                   
      # opsi penyimpanan frame dengan RGB/GRAY dengan convert)         
      gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      color = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
      if tulis is not None:
         tulis.write(frame)         
      cv2.imshow('Kamera dan Rekam',frame)
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break
      fps.update()  
   # check to see if we need to release the video writer pointer
   if tulis is not None:
      tulis.release()   
   rekam.release()
   cv2.destroyAllWindows()  
   tkinter.messagebox.showinfo("Info","\n Rekam video selesai \n") 
   return(Menu)    
   while False:   
      tkinter.messagebox.showwarning("Kesalahan","\n Folder Tidak Ditemukan \n")
   return(Menu)   

def webdet():
   capture =cv2.VideoCapture(0)
   face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
   eye_glass = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
   

   while True:
       ret, frame = capture.read()
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = face_cascade.detectMultiScale(gray)
    

       for (x,y,w,h) in faces:
           font = cv2.FONT_HERSHEY_COMPLEX
           cv2.putText(frame,'Face',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
           cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
           roi_gray = gray[y:y+h, x:x+w]
           roi_color = frame[y:y+h, x:x+w]
        
          
           eye_g = eye_glass.detectMultiScale(roi_gray)
           for (ex,ey,ew,eh) in eye_g:
              cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

       
       cv2.imshow('frame',frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
          break
   capture.release()
   cv2.destroyAllWindows()

def webdetRec():
   capture =cv2.VideoCapture(0)
   face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
   eye_glass = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
   fourcc=cv2.VideoWriter_fourcc(*'XVID') 
   op=cv2.VideoWriter('Sample2.avi',fourcc,9.0,(640,480))

   while True:
       ret, frame = capture.read()
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = face_cascade.detectMultiScale(gray)
    

       for (x,y,w,h) in faces:
           font = cv2.FONT_HERSHEY_COMPLEX
           cv2.putText(frame,'Face',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
           cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
           roi_gray = gray[y:y+h, x:x+w]
           roi_color = frame[y:y+h, x:x+w]
        
          

           eye_g = eye_glass.detectMultiScale(roi_gray)
           for (ex,ey,ew,eh) in eye_g:
              cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
       op.write(frame)
       cv2.imshow('frame',frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
          break
   op.release()      
   capture.release()
   cv2.destroyAllWindows()

   
def alert():
   mixer.init()
   alert=mixer.Sound('beep-07.wav')
   alert.play()
   time.sleep(0.1)
   alert.play()   
   
def blink():
   capture =cv2.VideoCapture(0)
   face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
   eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
   blink_cascade = cv2.CascadeClassifier('CustomBlinkCascade.xml')

   while True:
      ret, frame = capture.read()
      gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray)

      for (x,y,w,h) in faces:
         font = cv2.FONT_HERSHEY_COMPLEX
         cv2.putText(frame,'Face',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
         roi_gray = gray[y:y+h, x:x+w]
         roi_color = frame[y:y+h, x:x+w]

         eyes = eye_cascade.detectMultiScale(roi_gray)
         for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

         blink = blink_cascade.detectMultiScale(roi_gray)
         for(eyx,eyy,eyw,eyh) in blink:
            cv2.rectangle(roi_color,(eyx,eyy),(eyx+eyw,eyy+eyh),(255,255,0),2)
            alert()
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF ==ord('q'):
          break
         
  
   capture.release()
   cv2.destroyAllWindows()

   
but1=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=deteksi_kamera,text='Buka Kamera',font=('helvetica 15 bold'))
but1.place(x=5,y=104)

but2=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=kamera_rekam,text='Buka Kamera dan Rekam',font=('helvetica 15 bold'))
but2.place(x=5,y=176)

but3=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=webdet,text='Buka Kamera dan Deteksi',font=('helvetica 15 bold'))
but3.place(x=5,y=250)

but4=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=webdetRec,text='Deteksi dan Rekam',font=('helvetica 15 bold'))
but4.place(x=5,y=322)

# but5=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=blink,text='Detect Eye Blink & Record With Sound',font=('helvetica 15 bold'))
# but5.place(x=5,y=400)

but5=Button(frame,padx=5,pady=5,width=8,bg='white',fg='black',relief=GROOVE,text='KELUAR',command=keluar,font=('helvetica 15 bold'))
but5.place(x=188,y=478)


root.mainloop()