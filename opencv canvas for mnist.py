import os
import PIL
import cv2
import glob
import numpy as np
from tkinter import *
from PIL import Image, ImageDraw, ImageGrab
from keras.models import load_model
model = load_model(r'C:\Users\kumar\Downloads\mnist.h5') 

root = Tk()
root.resizable(0,0)
root.title("Handwritten digit recognition")

lastx , lasty= None,None
image_number = 0
cv = Canvas(root, width =640, height = 480, bg = 'white')
cv.grid(row = 0, column = 0, pady = 2, sticky=W, columnspan=2)

cv.bind('<Button-1>', activate_event)

btn_save = Button(text = "Recognize Digit", command= Recognize_Digit)
btn_save.grid(row=2, column=0, pady = 1, pdx = 1)
button_clear = Button(text = "clear widget", command = clear_widget)
button_clear.grid(row = 2, column=1, pady = 1, padx = 1)
root.mainloop()

def clear_widget():
    cv.delete("all")

def activate_event(event):
    global lastx, lasty
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y

def draw_lines(event):
    global lastx, lasty
    x,y = event.x, event.y
    cv.create_line(( lastx, lasty, x,y), width=8, fill='black', capstyle = ROUND, smooth = TRUE, splinesteps =12)
    lastx, lasty = x,y

def Recognize_Digit():
    global image_number
    predictions = []
    percentage = []
    filename = f'image_{image_number}.png'
    widget = cv

    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    x1 = x+widget.winfo_width()
    y1 = y+widget.winfo_height()

    ImageGrab.grab().crop((x,y,x1,y1)).save(filename)

    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    ret , th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x,y),(x+w , y+h), (255,0,0), 1)
        top = int(0.05 * th.shape[0])
        bottom = top
        left = int(0.05 * th.shape[1])
        right = left
        th_up = cv2.copyMakeBorder(th, top,bottom,left,right, cv2.BORDER_REPLICATE)
        roi = th[y-top:y+h+bottom, x-left:x+w+right]
        img = cv2.resize(roi, (28,28), Interpolation=cv2.INTER_AREA)
        img = img.reshape(1,28,28,1)
        img = img/255.0
        pred = model.predict([img])[0]
        final_pred = np.argmax(pred)
        data = str(final_pred)+' '+str(int(max(pred)*100))+'%'
        font= cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (255,0,0)
        thickness = 1
        cv2.putText(image, data, (x,y-5), font, fontScale,color, thickness )
    cv2.imshow('image', image)
    cv2.waitKey(0)

    
