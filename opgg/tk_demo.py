import tkinter
import requests
import io
from PIL import Image,ImageTk
root = tkinter.Tk()
root.minsize(600,500)

img = requests.get("http://opgg-static.akamaized.net/images/lol/champion/Zoe.png")
data_stream = io.BytesIO(img.content)
pil_img = Image.open(data_stream)

tk_img = ImageTk.PhotoImage(pil_img)
label = tkinter.Label(root,image = tk_img,bg = 'white')
label.pack(padx=5,pady=200,side='right')
root.mainloop()