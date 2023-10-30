import sqlite3
from tkinter import *
import tkinter as tk

def get_joke():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute("SELECT joke FROM db ORDER BY RANDOM() LIMIT 1;")
    result = cur.fetchone()
    if result is not None:
        joke = result[0]
        return joke
    else:
        return "Нету шуток :("

def show_joke(event=None):
    joke = get_joke()
    lable.config(text=joke)
    

root = Tk()
root.geometry("665x450")

button = Button(root, text="Получить шутку", command=show_joke)
button.pack()

lable = tk.Label(root)
lable.pack()

root.mainloop()