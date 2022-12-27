# %%script C:\Users\ilzira\AppData\Local\Programs\Python\Python38\python.exe
import sys
print(sys.version)
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image, ImageEnhance
import pytesseract
#.strip("‪u202a")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = 0
        self.y = 0
        
        self.canvas = tk.Canvas(self, width = 300, height = 300, bg = "white", cursor = "cross")
        self.label = tk.Label(self, text = "Enter your number", font = ("Arial", 14))
        self.btn_recognise = tk.Button(self, text = "Recognize", command = self.recognize)
        clear_fn = lambda: self.canvas.delete("all")
        self.btn_clear = tk.Button(self, text = "Clear", command = clear_fn)
        
        self.canvas.bind("<B1-Motion>", func = self.on_click_draw)
        self.canvas.grid(row = 0, column = 0, pady = 2, sticky = W)
        self.label.grid(row = 0, column = 1, pady = 2, padx = 2)
        self.btn_recognise.grid(row = 1, column = 1, pady = 2, padx = 2)
        self.btn_clear.grid(row = 1, column = 0, pady = 2)

    def recognize(self):
        x = self.winfo_rootx() + self.canvas.winfo_x()
        y = self.winfo_rooty() + self.canvas.winfo_y() + 50
        x1 = x + self.canvas.winfo_width() 
        y1 = y + self.canvas.winfo_height() - 50
        img = ImageGrab.grab().crop((x, y, x1, y1))
    
        prediction = predict_number(img)
        try:
            self.label.configure(text=str(int(prediction)))
        except ValueError:
            self.label.configure(text="Can't resolve")
        
    def on_click_draw(self, event):
        r = 6
        self.x = event.x
        self.y = event.y
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, outline='red', fill='red')
            
def predict_number(image):
    enhancer = ImageEnhance.Contrast(image)
    img = enhancer.enhance(4)
    fn = lambda x: 255 if x > 200 else 0
    res = img.convert('L').point(fn, mode='1')
    text = pytesseract.image_to_string(res, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return text


app = App()
mainloop()
