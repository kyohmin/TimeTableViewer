import tkinter as tk
import ttkbootstrap as ttk


root = ttk.Window(themename="flatly")
root.geometry("500x500")
columns = ("indexNum", "fileName")

myTree = ttk.Treeview(root, columns = columns, show="headings", bootstyle="primary")
myTree.column("fileName",anchor="w")

myTree.heading('indexNum', text="#", anchor="w")
myTree.heading('fileName', text="File Name", anchor="w")
myTree.column("indexNum", width=20, minwidth=30,stretch=tk.YES)

contacts = []

for i in range(10):
    contacts.append((f'First {i}', f'Name {i}'))

for contact in contacts:
    myTree.insert("", ttk.END, values=contact)

filesList = ["asdas/asdasd/asdasd","asdas/asdasd/asdasd","asdas/asdasd/asdasd","asdas/asdasd/asdasd"]

for index, file in enumerate(filesList):
    myTree.insert("",ttk.END, values=(index,file))

myTree.pack() 

root.mainloop() 