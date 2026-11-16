import sys, tkinter as tk
from PIL import Image, ImageTk, ImageSequence

img = Image.open(sys.argv[1])
root = tk.Tk()
root.title("Amar")
root.attributes("-topmost", True)
root.lift()
root.focus_force()

frames = [ImageTk.PhotoImage(f.copy().convert("RGBA").resize((200, 200)))
          for f in ImageSequence.Iterator(img)]
delay = img.info.get("duration", 100)
label = tk.Label(root)
label.pack()

def play(i=0):
    label.config(image=frames[i])
    root.after(delay, play, (i + 1) % len(frames))

play()
root.mainloop()

