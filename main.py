#Run3 Building GUI
import sys
import os
import cv2
from cv2.data import haarcascades as hc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    #cred:https://stackoverflow.com/users/5168024/nautilius
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Methods
def convert_to_jpg(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img
def detect_face(image):
    status_label.config(text="started detecting", fg="blue")
    status_label.update()
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    status_label.config(text="used cascade classifier", fg="blue")
    status_label.update()
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    status_label.config(text="used gray", fg="blue")
    status_label.update()
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    status_label.config(text="used face cascade", fg="blue")
    status_label.update()
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        y=max(0,y-int(0.4*h))
        h=min(int(h*1.8),image.height-y)
        x=max(0,x-int((h-w)/2))
        w=min(h,image.width)
        if w>h:
            x+=(w-h) // 2
            w=h
        elif h>w:
            y+=(h-w) // 2
            h=w
        cropped_face = image.crop((x,y,x+w,y+h))
        return cropped_face
    else:
        return None
def resize_image(image, size=(510, 510)):
    return image.resize(size)
def add_label(image, label):
    box=ImageDraw.Draw(image)
    box.rectangle((0,510-50,510,510), fill="white")
    font = ImageFont.truetype(resource_path("assets\\fonts\\arialbd.ttf"), 45)
    text_width=font.getlength(label)
    x=(510-text_width)//2
    box.text((x, 510-50), label, fill="black", font=font)
    return image
#ProcessingImage
def process_image(input_path, output_path):
    img=convert_to_jpg(input_path)
    status_label.config(text="converted to jpg", fg="blue")
    status_label.update()
    img=detect_face(img)
    status_label.config(text="detected face", fg="blue")
    status_label.update()
    if(img is None):
        return
    img=resize_image(img)
    #img=change_bg(img)
    filename=os.path.basename(input_path)
    label=filename.split('.')[0]
    img=add_label(img,label)
    status_label.config(text="new label", fg="blue")
    status_label.update()
    output_file=os.path.join(output_path, f"{label}.jpg")
    img.save(output_file)

def main(input_dir, output_dir, status_label):
    status_label.config(text="Loading...", fg="blue")
    status_label.update()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        status_label.config(text="iteration starts", fg="blue")
        status_label.update()
        if filename.lower().endswith(('.png', '.jpeg', '.jpg')):
            status_label.config(text="check file type", fg="blue")
            status_label.update()
            input_path = os.path.join(input_dir, filename)
            status_label.config(text="start processing", fg="blue")
            status_label.update()
            process_image(input_path, output_dir)
    status_label.config(text="Successfully resized images!", fg="green")
    status_label.update()

def select_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, input_folder)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, output_folder)

def start_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    main(input_folder, output_folder, status_label)
#app GUI
app = tk.Tk()
app.title("NCC Image Resizer")
app.geometry("425x300")
app.resizable(False, False)
# Welcome message
welcome_label = tk.Label(app, text="Welcome to NCC Image Resizer", font=("Arial", 16))
welcome_label.grid(row=0, column=0, columnspan=3, pady=10)
# Instructions
instructions_text = "Note: Save photos of all cadets in one\nfolder with file name as cadets regimental number\ne.g. UP2023SDA234567.jpg\n(png, jpeg format also accepted)"
instructions_label = tk.Label(app, text=instructions_text, font=("Arial", 10), justify='center')
instructions_label.grid(row=1, column=0, columnspan=3, pady=5)
# Input folder selection
input_folder_label = tk.Label(app, text="Select Input Folder:")
input_folder_label.grid(row=2, column=0, pady=5)
input_folder_entry = tk.Entry(app, width=40)
input_folder_entry.grid(row=2, column=1, pady=5)
input_folder_button = tk.Button(app, text="Browse", command=select_input_folder)
input_folder_button.grid(row=2, column=2, pady=5)
# Output folder selection
output_folder_label = tk.Label(app, text="Select Output Folder:")
output_folder_label.grid(row=3, column=0, pady=5)
output_folder_entry = tk.Entry(app, width=40)
output_folder_entry.grid(row=3, column=1, pady=5)
output_folder_button = tk.Button(app, text="Browse", command=select_output_folder)
output_folder_button.grid(row=3, column=2, pady=5)
# Status Lavel
status_label = tk.Label(app, text="", font=("Arial", 12), fg="green")
status_label.grid(row=6, column=0, columnspan=3, pady=5)
# Process Images button
process_button = tk.Button(app, text="RESIZE", command=start_processing)
process_button.grid(row=4, column=0, columnspan=3, pady=10)
app.mainloop()