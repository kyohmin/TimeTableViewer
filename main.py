import os, csv
import math

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd

# FOr loading and exporting excel
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Color

# ===== Data Structures =====

# LinkedList
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def __iter__(self):
       node = self.head
       while node:
           yield node
           node = node.next

    def append(self, data):
        newNode = Node(data)
        self.tail = newNode
        if self.head == None:
            self.head = newNode
            self.tail = newNode
        
        else:
            currentNode = self.head
            while currentNode.next != None:
                currentNode = currentNode.next

            currentNode.next = newNode



    def popFront(self):
        if self.head == None:
            return
        else: # When there is at least one value in the Linked List
            result = self.head
            if self.head.next != None: # When there is only one value in the Linked List
                self.head = self.head.next
            else:  # When head is the only vlaue
                self.head = None
                self.tail = None

            return result.data
        
    def remove(self, index):
        pass

class HashNode:
    def __init__(self, key = -1):
        self.key = key
        self.next = next

class HashSet:
    def __init__(self, size):
        self.cnt = int(math.floor(size * 1.3))
        self.table = [HashNode() for _ in range(size)]

    def customHash(self, key):
        hashedKey = sum(ord(char) for char in key) % self.size
        return hashedKey
    
    def add(self, key, value):
        cur = self.table[self.customHash(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next.val = value
                return
            cur = cur.next
        cur.next = HashNode(key)

    def get(self, key):
        cur = self.table[self.customHash(key)].next
        while cur:
            if cur.key == key:
                return cur.value
            cur = cur.next
        return -1



class DataHandler:
    def __init__(self):
        self.__schedules = LinkedList()
        self.__filesPathList = []
        self.__scheduleSize = 0

    def resetSchedules(self):
        self.__schedules = LinkedList()
        self.__storeSchedule()

    def getFilesPathList(self):
        return self.__filesPathList
    
    def setFilesPathList(self, filesList):
        self.__filesPathList = filesList

    def removeSpecificFile(self, file):
        self.__filesPathList.remove(file)


    def __storeSchedule(self):
        for fileDirectory in self.__filesPathList:
            with open(fileDirectory, "r") as csvfile:
                csvData = csv.reader(csvfile, delimiter=",")
                for row in csvData:
                    if row[0] == '':
                        continue
                    self.__schedules.append(Schedule(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],row[11]))
                    self.__scheduleSize += 1
                    


    def getScheduleSize(self):
        return self.__scheduleSize
    
    def getSchedules(self):
        return self.__schedules

class DisplayOptionHandler:
    def __init__(self):
        self.__sortedResult = LinkedList()
        self.__filters = [NoFilter(),StringFilter(),DateTimeFilter()]

    def getResult(self):
        return self.__sortedResult

    def queryFilterOption():
        pass

    def querySortOption():
        pass

    def reverseResult():
        pass

class ResultHandler:
    def __init__(self):
        self.__result = LinkedList()
        self.__exportLocation = ""

    def queryFileType():
        pass

    def queryExportLocation():
        pass

    def displaySchedules():
        pass

    def exportExcel():
        pass

    def exportPDF():
        pass

class Schedule():
    def __init__(self, name: str, description:str, activityDate:str, scheduledDay:str,startTime:str,endTime:str,duration:str,location:str,size:str,lecturer:str,zone:str):
        self.__module, self.__moduleCode, self.__cohort, self.__course, self.__fullPart, self.__session = self.extractData(name, description)
        self.__description = description
        self.__activityDate = activityDate
        self.__scheduledDay = scheduledDay
        self.__startTime = startTime
        self.__endTime = endTime
        self.__duration = duration
        self.__location = location
        self.__size = size
        self.__lecturer = lecturer
        self.__zone = zone

    def extractData(self,name, description):
        course,cohort,fullPart,moduleCode,session = name.split("_")
        cohort = fullPart + "_" + cohort
        module = description[4:].split(" (")[0]
        
        return [module, moduleCode, cohort, course, fullPart, session]

    def getDetail(self):
        return [self.__sessionName, self.__description, self.__activityDate]
        

class Filter:
    def __init__(self):
        self.filteredResult = []

    def returnFilteredResult(self):
        return self.filteredResult
    
class NoFilter(Filter):
    def __init__(self):
        super().__init__()

class StringFilter(Filter):
    def __init__(self):
        super().__init__()
        self.moduleSet = {}
        self.lecturerSet = {}
        self.locationSet = {}

    def optionExits():
        pass

    def sort():
        pass

    def search():
        pass

class DateTimeFilter(Filter):
    def __init__(self):
        super().__init__()
        self.filteredResult = []
        self.endDate = ""
        self.startTime = ""
        self.endTime = ""
        self.specificDate = ""
        self.specificTime = ""

    def sort():
        pass

# class Main:
#     def __init__(self):
        

class GUI(ttk.Window):
    def __init__(self):
        # Initializing the handlers
        self.dataHandler = DataHandler()
        self.displayOptionHandler = DisplayOptionHandler()
        self.resultHandler = ResultHandler()

        # Make a window
        super().__init__()
        theme = ttk.Style()
        theme.theme_use("flatly")
        self.resizable(False,False)
        self.title("Timetable Viewer")
        self.geometry("750x500+200+200")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.mainPage = ttk.Frame(self)
        self.loadPage = ttk.Frame(self)
        self.viewPage = ttk.Frame(self, width=1400, height=500)

        # Main Page
        self.mainPage.grid(row=0, column=0, sticky="nswe")
        self.mainPage.rowconfigure(0,weight=2)
        self.mainPage.rowconfigure(1,weight=1)
        self.mainPage.rowconfigure(2,weight=2)
        self.mainPage.columnconfigure(0,weight=1)
        self.mainPage.columnconfigure(1,weight=1)
        self.mainPage.columnconfigure(2,weight=1)
        self.mainPage.columnconfigure(3,weight=1)
        self.mainPage.columnconfigure(4,weight=1)

        myStyle = ttk.Style()
        myStyle.configure('my.TButton', font=("Arial", 16))


        mainPageLabel = ttk.Label(self.mainPage, text="Timetable Viewer", font = ("Arial", 30, "bold"))
        mainPageLabel.grid(row=0, column=2, sticky= "s")
        startBtn = ttk.Button(self.mainPage, text="Start", style="my.TButton", command=lambda:[self.changeFrame(self.loadPage)])
        startBtn.grid(row=1,column=2, sticky= "swe", ipady=12, padx=100)
        exitBtn = ttk.Button(self.mainPage, text="Exit", style="my.TButton" ,command=self.destroy)
        exitBtn.grid(row=2,column=2, sticky= "nwe", pady=(15,0), ipady=12, padx=100)

        # Load Page
        self.loadPage.grid(row=0, column=0, sticky="nswe")
        self.loadPage.rowconfigure(0,weight=4)
        self.loadPage.rowconfigure(1,weight=4)
        self.loadPage.rowconfigure(2,weight=2)
        self.loadPage.columnconfigure(0,weight=1)
        self.loadPage.columnconfigure(1,weight=3)
        self.loadPage.columnconfigure(2,weight=1)

        """borderwidth=10, relief="solid"""

        self.loadPageLabel = ttk.Label(self.loadPage, text="Locate the Folder with CSV files", anchor="center", font=("Arial", 26, "bold"),borderwidth=10, relief="solid")
        self.loadPageLabel.grid(row=0,column=1, sticky="nwe", pady=(50,0))
        self.openFolderButton = ttk.Button(self.loadPage, text="Open Folder", style="my.TButton", command=lambda:[self.queryFolderDirectory()])
        self.openFolderButton.grid(row=0,column=1, sticky="n", pady=(120,0), ipady=5, ipadx=40)
        self.backButton = ttk.Button(self.loadPage, text="back", style="my.TButton", command=lambda:[self.changeFrame(self.mainPage)])
        self.backButton.grid(row=2,column=0, sticky="s", pady=(0,20), padx=20, ipadx=30, ipady=7)
        self.nextButton = ttk.Button(self.loadPage, text="next", style="my.TButton", command=lambda:[self.openViewPage()])
        self.nextButton.grid(row=2,column=2, sticky="s", pady=(0,20), padx=20, ipadx=30, ipady=5)
        self.listBox = tk.Listbox(self.loadPage, relief="flat", font=("Arial", 20))
        self.listBox.grid(row=1,column=1, sticky="nswe")
        self.scrollStyle = ttk.Style()
        self.scrollStyle.configure("TScrollbar",background="#000000")
        self.scrollbar = ttk.Scrollbar(self.loadPage, orient="vertical",command=self.listBox.yview)
        self.scrollbar.grid(row=1,column=2,sticky="wns")
        self.listBox.configure(yscrollcommand=self.scrollbar.set)

        deleteButton = ttk.Button(text="Delete")
        self.clearButton = ttk.Button(self.loadPage, text="Clear", command=lambda:[self.clearAll()])
        self.clearButton.grid(row=2,column=1,sticky="w", padx=(130,0))
        self.deleteButton = ttk.Button(self.loadPage, text="Delete", command=lambda:[self.deleteFile()])
        self.deleteButton.grid(row=2,column=1,sticky="e", padx=(0,130))

        # View Page
        self.viewPage.grid(row=0,column=0,sticky="nsew")
        self.viewPage.columnconfigure(0,weight=1)
        self.viewPage.columnconfigure(1,weight=1)
        self.viewPage.columnconfigure(2,weight=5)
        self.viewPage.rowconfigure(0,weight=1)
        self.viewPage.rowconfigure(1,weight=5)
        self.viewPage.rowconfigure(2,weight=1)
        self.backLoadButton = ttk.Button(self.viewPage, text="back", style="my.TButton", 
        command=lambda:[self.changeFrame(self.loadPage)])
        self.backLoadButton.grid(row=2, column=0, sticky="ws", ipady=7, ipadx=30, padx=20, pady=(0,20))

        # Filtering Setting
        self.filterLabel = ttk.Label(self.viewPage,text="Filtering Options", font=("Arial", 26,"bold"))

        # Setting for the table
        columns = ("Module", "Lecturer", "Location") #"Date", "Start Time", "End Time"
        self.tree = ttk.Treeview(self.viewPage, columns=columns, show="headings")
        self.tree.heading("Module", text="Module Name")
        self.tree.heading("Lecturer", text="Lecturer")
        self.tree.heading("Location", text="Location")
        # self.tree.heading("Date", text="Date")
        # self.tree.heading("Start Time", text="Start Time")
        # self.tree.heading("End Time", text="End Time")

        self.tree.grid(row = 1, column = 2, sticky="nsew")
        


        # Run
        self.changeFrame(self.mainPage)
        self.mainloop()

    def openViewPage(self):
        self.geometry("1400x500")
        self.viewPage.tkraise()
        self.dataHandler.setData()
        dummyList = []
        for i in range(5):
            dummyList.append(tuple(self.dataHandler.getSchedules().popFront().getDetail()))
        for i in dummyList:
            print(i)

        for i in dummyList:
            self.tree.insert("", tk.END, values=i)
        

    def changeFrame(self, frame):
        self.geometry("750x500")
        frame.tkraise()

    def queryFolderDirectory(self):
        folderDirectory = fd.askdirectory()
        filesList = []
        if folderDirectory != "":
            try:
                for file in os.listdir(folderDirectory):
                    if file.endswith(".csv"):
                        filesList.append(os.path.join(folderDirectory, file))

                self.dataHandler.setFilesPathList(filesList)
                self.displayFiles()
            except FileNotFoundError:
                pass


    def displayFiles(self):
        self.listBox.delete(0,"end")
        i = 1
        filesList = self.dataHandler.getFilesPathList()
        try:
            for file in filesList:
                self.listBox.insert('end', "File "+str(i) + ": " + file)
                i+=1
        except:
            pass

    def clearAll(self):
        self.listBox.delete(0,"end")
        self.dataHandler.setFilesPathList([])

    def deleteFile(self):
        print(self.listBox.get(self.listBox.curselection()).split(": ",1)[1])
        self.dataHandler.removeSpecificFile(self.listBox.get(self.listBox.curselection()).split(": ",1)[1])
        self.listBox.delete(tk.ANCHOR)
        self.displayFiles()
        

a = GUI()
