import os, csv
import math
import datetime

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox as mb
from tkinter import filedialog as fd


# ===== Custom Data Structures =====
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __iter__(self):
        currentNode = self
        while currentNode:
            yield currentNode
            currentNode = currentNode.next

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def __iter__(self):
        currentNode = self.head
        while currentNode:
            yield currentNode
            currentNode = currentNode.next

    def __contains__(self, node):
        currentNode = self.head
        while currentNode:
            if currentNode.data == node:
                return True
            currentNode = currentNode.next


    def append(self, data):
        newNode = Node(data)
        if self.head == None:
            self.head = newNode
            self.tail = newNode
        
        else:
            self.tail.next = newNode
            self.tail= newNode

class HashNode:
    def __init__(self, key = -1):
        self.key = key
        self.value = LinkedList()
        self.next = None

class HashTable:
    def __init__(self, size):
        self.cnt = int(math.floor(size * 1.3))
        self.table = [HashNode() for _ in range(self.cnt)]

    def customHash(self, key):
        key = str(key)
        hashedKey = sum(ord(char) for char in key) % self.cnt
        return hashedKey
    
    def add(self, key, data):        
        cur = self.table[self.customHash(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next.value.append(data)
                return
            cur = cur.next
        cur.next = HashNode(key)
        cur.next.value.append(data)


    def get(self, key) -> LinkedList:
        cur = self.table[self.customHash(key)].next
        while cur:
            if cur.key == key:
                return cur.value
            cur = cur.next
        return -1

class Stack:
    def __init__(self):
        self.head = None
    
    def __iter__(self):
        currentNode = self.head
        while currentNode:
            yield currentNode
            currentNode = currentNode.next

    def __contains__(self, node):
        currentNode = self.head
        while currentNode:
            if currentNode.data == node:
                return True
            currentNode = currentNode.next


    def push(self, data):
        newNode = Node(data)
        if self.head == None:
            self.head = newNode
        
        else:
            newNode.next = self.head
            self.head = newNode

    def isEmpty(self):
        if self.head == None:
            return 1
        else:
            return 0

    def pop(self) -> Node:
        if self.isEmpty():
            return None
        else:
            tmp = self.head
            self.head = self.head.next
            tmp.next = None # For Garbage collection
            return tmp.data



# ===== Schedule Data =====
class Schedule():
    def __init__(self, module:str, moduleCode:str, cohort:str, course:str, fullPart:str, session:str, activityDate:str, scheduledDay:str,startTime:str,endTime:str,duration:str,location:str,size:str,lecturer:str,zone:str):
        self.__module = module
        self.__moduleCode = moduleCode
        self.__cohort = cohort
        self.__course = course
        self.__fullPart = fullPart
        self.__session = session
        self.__activityDate = activityDate
        self.__scheduledDay = scheduledDay
        self.__startTime = startTime
        self.__endTime = endTime
        self.__duration = duration
        self.__location = location
        self.__size = size
        self.__lecturer = lecturer
        self.__zone = zone
    
    def get(self, key) -> dict:
        value = {
            "module" : self.__module, "moduleCode" : self.__moduleCode, "cohort" : self.__cohort,
            "course" : self.__course, "fullPart" : self.__fullPart, "session" : self.__session,
            "activityDate" : self.__activityDate, "scheduledDay" : self.__scheduledDay,
            "startTime" : self.__startTime, "endTime" : self.__endTime, "duration" : self.__duration,
            "location" : self.__location, "size" : self.__size, "lecturer" : self.__lecturer, "zone" : self.__zone
        }[key]
        
        return value
    
    def getAll(self) -> list:
        li = [
            self.__module, self.__moduleCode, self.__cohort, self.__course, self.__fullPart,
            self.__session, self.__activityDate, self.__scheduledDay, self.__startTime,
            self.__endTime, self.__duration, self.__location, self.__size, self.__lecturer, self.__zone
        ]

        return  li



# ===== Handler Classes =====
class DataHandler:

    def __init__(self):
        self.__schedules = LinkedList()
        self.__filesPathList = []
        self.__rangeList = []

        # To hand over the range number to DisplayHandler for intialization of Hash Table
        self.__moduleRange = set()
        self.__moduleCodeRange = set()
        self.__cohortRange = set()
        self.__courseRange = set()
        self.__fullPartRange = set()
        self.__sessionRange = set()
        self.__activityDateRange = set()
        self.__scheduledDayRange = set()
        self.__startTimeRange = set()
        self.__endTimeRange = set()
        self.__durationRange = set()
        self.__locationRange = set()
        self.__sizeRange = set()
        self.__lecturerRange = set()
        self.__zoneRange = set()

    def setSchedules(self):
        self.__schedules.head = None  # Reset the head before storing the schedules
        self.__resetRange()

        for fileDirectory in self.__filesPathList:
            with open(fileDirectory, "r") as csvfile:
                csvData = csv.reader(csvfile, delimiter=",")
                for row in csvData:
                    if row[0] == '':
                        continue

                    module, moduleCode, cohort, course, fullPart, session = self.__extractData(row[1], row[2])

                    self.__setRange(
                        module, moduleCode, cohort, course, fullPart, session, self.__dateInput(row[3]),
                        self.__dateInput(row[3]).isoweekday(), self.__timeInput(row[5]),
                        self.__timeInput(row[6]),row[7].lstrip("0"), row[8], int(row[9]), row[10], row[11]
                    )
                    
                    self.__schedules.append(
                        Schedule(
                            module, moduleCode, cohort, course, fullPart, session, self.__dateInput(row[3]),
                            self.__dateInput(row[3]).isoweekday(), self.__timeInput(row[5]), self.__timeInput(row[6]),
                            row[7].lstrip("0"), row[8], int(row[9]), row[10], row[11]
                        )
                    )

        # Storing size of range for optimal hashtable size
        self.__rangeList = [len(self.__moduleRange), len(self.__moduleCodeRange), len(self.__cohortRange), len(self.__courseRange), len(self.__fullPartRange), 
                            len(self.__sessionRange), len(self.__activityDateRange), len(self.__scheduledDayRange), len(self.__startTimeRange), len(self.__endTimeRange), 
                            len(self.__durationRange), len(self.__locationRange), len(self.__sizeRange), len(self.__lecturerRange), len(self.__zoneRange)]

    def getSchedules(self) -> Node:
        return self.__schedules.head
    
    def getRangeList(self) -> list:
        return self.__rangeList

    def setFilesPathList(self, filesList):
        self.__filesPathList = filesList

    def getFilesPathList(self):
        return self.__filesPathList

    def setRange(self, schedules):
        self.__resetRange()
        try:
            for i in schedules:
                module, moduleCode, cohort, course, fullPart, session, activityDate, scheduleDay, startTime, endTime, duration, location, size, lecturer, zone = i.data.getAll()
                self.__setRange(module, moduleCode, cohort, course, fullPart, session, activityDate, scheduleDay, startTime, endTime, duration, location, size, lecturer, zone)
        except:
            pass

    def getRange(self, category):
        value = {
        "module": self.__moduleRange,
        "moduleCode": self.__moduleCodeRange,
        "cohort": self.__cohortRange,
        "course": self.__courseRange,
        "fullPart": self.__fullPartRange,
        "session": self.__sessionRange,
        "activityDate": self.__activityDateRange,
        "scheduledDay": self.__scheduledDayRange,
        "startTime": self.__startTimeRange,
        "endTime": self.__endTimeRange,
        "duration": self.__durationRange,
        "location": self.__locationRange,
        "size": self.__sizeRange,
        "lecturer": self.__lecturerRange,
        "zone": self.__zoneRange,
        }[category]

        return value

    def __dateInput(self, strVal):
        day, month, year = strVal.split("/")
        return datetime.date(int(year),int(month),int(day))

    def __timeInput(self, strVal):
        hour, minute,second = strVal.split(":")
        return datetime.time(int(hour),int(minute),int(second))

    def __setRange(self, module:str, moduleCode:str, cohort:str, course:str, fullPart:str, session:str, activityDate:str, scheduleDay:str, startTime:str, endTime:str, duration:str, location:str, size:str, lecturer:str, zone:str):
        self.__moduleRange.add(module)
        self.__moduleCodeRange.add(moduleCode)
        self.__cohortRange.add(cohort)
        self.__courseRange.add(course)
        self.__fullPartRange.add(fullPart)
        self.__sessionRange.add(session)
        self.__activityDateRange.add(activityDate)
        self.__scheduledDayRange.add(scheduleDay)
        self.__startTimeRange.add(startTime)
        self.__endTimeRange.add(endTime)
        self.__durationRange.add(duration)
        self.__locationRange.add(location)
        self.__sizeRange.add(size)
        self.__lecturerRange.add(lecturer)
        self.__zoneRange.add(zone)

    def __extractData(self,name:str, description:str) -> list:
        course,cohort,fullPart,moduleCode,session = name.split("_")
        cohort = fullPart + "_" + cohort
        module = description[4:].split(" (")[0]
        
        return [module, moduleCode, cohort, course, fullPart, session]
    
    def __resetRange(self):
        self.__moduleRange.clear()
        self.__moduleCodeRange.clear()
        self.__cohortRange.clear()
        self.__courseRange.clear()
        self.__fullPartRange.clear()
        self.__sessionRange.clear()
        self.__activityDateRange.clear()
        self.__scheduledDayRange.clear()
        self.__startTimeRange.clear()
        self.__endTimeRange.clear()
        self.__durationRange.clear()
        self.__locationRange.clear()
        self.__sizeRange.clear()
        self.__lecturerRange.clear()
        self.__zoneRange.clear() 


    

class DisplayHandler:
    def __init__(self, schedulesHead:Node, rangeList:list):
        # In case the user does not want to filter, the lined list's starting point is stored
        self.__originalSchedules = schedulesHead    # For backup when user wants to filter again
        self.__sortedSchedules = self.__originalSchedules

        # For filtering data. Used Custom Hash Table. Custom Hash Table stores linked list for common key value
        self.__moduleHT = HashTable(rangeList[0])
        self.__moduleCodeHT = HashTable(rangeList[1])
        self.__cohortHT = HashTable(rangeList[2])
        self.__courseHT = HashTable(rangeList[3])
        self.__fullPartHT = HashTable(rangeList[4])
        self.__sessionHT = HashTable(rangeList[5])
        self.__activityDateHT = HashTable(rangeList[6])
        self.__scheduledDayHT = HashTable(rangeList[7])
        self.__startTimeHT = HashTable(rangeList[8])
        self.__endTimeHT = HashTable(rangeList[9])
        self.__durationHT = HashTable(rangeList[10])
        self.__locationHT = HashTable(rangeList[11])
        self.__sizeHT = HashTable(rangeList[12])
        self.__lecturerHT = HashTable(rangeList[13])
        self.__zoneHT = HashTable(rangeList[14])

        self.__setFilter(schedulesHead)
    
    def filterSchedule(self, category:str, specificValue:str) -> LinkedList:
        tmp = None
        if category == "module":
            tmp = self.__moduleHT.get(specificValue)
        elif category == "moduleCode":
            tmp = self.__moduleCodeHT.get(specificValue)
        elif category == "cohort":
            tmp = self.__cohortHT.get(specificValue)
        elif category == "course":
            tmp = self.__cohortHT.get(specificValue)
        elif category == "fullPart":
            tmp = self.__fullPartHT.get(specificValue)
        elif category == "session":
            tmp = self.__sessionHT.get(specificValue)
        elif category == "activityDate":
            tmp = self.__activityDateHT.get(specificValue)
        elif category == "scheduledDay":
            tmp = self.__scheduledDayHT.get(specificValue)
        elif category == "startTime":
            tmp = self.__startTimeHT.get(specificValue)
        elif category == "endTime":
            tmp = self.__endTimeHT.get(specificValue)
        elif category == "duration":
            tmp = self.__durationHT.get(specificValue)
        elif category == "location":
            tmp = self.__locationHT.get(specificValue)
        elif category == "size":
            tmp = self.__sizeHT.get(specificValue)
        elif category == "lecturer":
            tmp = self.__lecturerHT.get(specificValue)
        elif category == "zone":
            tmp = self.__zoneHT.get(specificValue)

        if tmp is not None:
            return tmp.head

    def commonSchedules(self, filteredSchedules) -> LinkedList:
        # Restore before doing it
        # self.restoreSortedSchedules()
    

        node1 = self.__sortedSchedules
        node2 = filteredSchedules
        resultLinkedList = LinkedList()
        availabilityCheck = set()
        while node2 is not None:
            availabilityCheck.add(node2.data)
            node2 = node2.next

        while node1 is not None:
            if node1.data in availabilityCheck:
                resultLinkedList.append(node1.data)
            node1 = node1.next

        self.__sortedSchedules = resultLinkedList.head
            
        # return self.__sortedSchedules
        
    def restoreSortedSchedules(self):
        self.__sortedSchedules = self.__originalSchedules

    def rangeSearch(self,start, end, category):
        if category == "time":
            self.sort("startTime")
            # Finding starting point that starts the range
            head1 = self.__sortedSchedules
            prev = None
            for i in self.__sortedSchedules:
                if i.data.get("startTime") >= start:
                    if prev is not None:
                        head1 = i
                    break

            self.commonSchedules(head1)
            self.sort("endTime")
            
            tail = self.__sortedSchedules
            tail = None
            for i in self.__sortedSchedules:
                if i.data.get("endTime") > end:
                    if tail is not None:
                        tail.next = None
                    break
                tail = i

        else:    
            self.sort(category)
            head = self.__sortedSchedules
            endNode = None
            startFound = False
            for i in self.__sortedSchedules:
                if i.data.get(category) >= start and startFound== False:
                    head = i
                    startFound = True
                if i.data.get(category) > end:  
                    if endNode is not None:
                        endNode.next = None
                    break
                endNode = i
            
            self.__sortedSchedules = head

    def getResult(self) -> Node:
        return self.__sortedSchedules
    
    def sort(self, category, isAscending=True):
        head = self.__sortedSchedules

        self.__sortedSchedules = self.__mergeSort(head, category)

        # For Descending Order
        if isAscending == False:
            stack = Stack()

            for i in self.__sortedSchedules:
                stack.push(i)

            newHead = currentNode = stack.pop()

            while not stack.isEmpty():
                currentNode.next = stack.pop()
                currentNode = currentNode.next

            currentNode.next = None

            self.__sortedSchedules = newHead

    def __setFilter(self, schedules: Node):
        try:
            for schedule in schedules:
                self.__moduleHT.add(schedule.data.get("module"), schedule.data)
                self.__moduleCodeHT.add(schedule.data.get("moduleCode"), schedule.data)
                self.__cohortHT.add(schedule.data.get("cohort"), schedule.data)
                self.__courseHT.add(schedule.data.get("course"), schedule.data)
                self.__fullPartHT.add(schedule.data.get("fullPart"), schedule.data)
                self.__sessionHT.add(schedule.data.get("session"), schedule.data)
                self.__activityDateHT.add(schedule.data.get("activityDate"), schedule.data)
                self.__scheduledDayHT.add(schedule.data.get("scheduledDay"), schedule.data)
                self.__startTimeHT.add(schedule.data.get("startTime"), schedule.data)
                self.__endTimeHT.add(schedule.data.get("endTime"), schedule.data)
                self.__durationHT.add(schedule.data.get("duration"), schedule.data)
                self.__locationHT.add(schedule.data.get("location"), schedule.data)
                self.__sizeHT.add(schedule.data.get("size"), schedule.data)
                self.__lecturerHT.add(schedule.data.get("lecturer"), schedule.data)
                self.__zoneHT.add(schedule.data.get("zone"), schedule.data)
        except TypeError:
            pass

    def __mergeSort(self, head, category) -> "Node":
        if head is None or head.next is None:
            return head

        mid = self.__split(head)
        left = head
        right = mid.next
        mid.next = None 

        left = self.__mergeSort(left, category)
        right = self.__mergeSort(right, category)

        sortedHead = self.__merge(left, right, category)

        return sortedHead

    def __split(self, head):
        half = head
        end = head

        while end.next is not None and end.next.next is not None:
            half = half.next
            end = end.next.next

        return half

    def __merge(self, left, right, category):
        startNode = Node(None)
        currentNode = startNode

        # Loop through to sort between two linked lists
        while left is not None and right is not None:
            if left.data.get(category) < right.data.get(category):
                currentNode.next = left
                left = left.next
            else:
                currentNode.next = right
                right = right.next

            currentNode = currentNode.next

        # After One side is done sorting, add the rest values
        if left is not None:
            currentNode.next = left
        elif right is not None:
            currentNode.next = right

        return startNode.next  # Because first Node was used to create rest of the nodes

    def setHead(self, head):
        self.__sortedSchedules = head


# 1: Module, 2: Module code, 3: cohort, 4: Course, 5: Full/Part, 6: Session, 7: Activity Date, 8: ScheduledDay, 9: Start Time, 10: End Time
# 11: Duration, 12: Location 13: Size, 14: Lecturer, 15: Zone


class GUI(ttk.Window):
    def __init__(self):
        self.dataHandler = DataHandler()
        # self.displayOptionHandler = DisplayHandler()

        # Make a window setting
        self.initProgram()

        
        self.showPage(self.mainPage)
        self.mainloop()

    def initProgram(self):
        super().__init__()
        theme = ttk.Style()
        theme.theme_use("flatly")
        self.resizable(False,False)
        self.title("Timetable Viewer")
        self.geometry("750x500+500+250")
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight=1)

        # Initializing the pages
        self.mainPage = ttk.Frame(self)
        self.loadPage = ttk.Frame(self)
        self.viewPage = ttk.Frame(self, width = 1500, height=500)

        self.initMainPage()
        self.initLoadPage()
        self.initViewPage()

    def initMainPage(self):
        # Setting Page
        self.mainPage.grid(row=0, column=0, sticky="nswe")
        self.mainPage.rowconfigure(0,weight= 5)
        self.mainPage.rowconfigure(1,weight= 6)
        self.mainPage.columnconfigure(0,weight=1)
        self.mainPage.columnconfigure(1,weight=1)
        self.mainPage.columnconfigure(2,weight=1)
        self.mainPage.columnconfigure(3,weight=1)
        self.mainPage.columnconfigure(4,weight=1)

        # Predefining title and button style
        titleFont = ("Arial", 40, "bold")
        self.myButtonStyle = ttk.Style()
        self.myButtonStyle.configure('my.TButton', font=("Arial", 20))

        # Specific Setting
        self.mainPageLabel = ttk.Label(self.mainPage, text="Timetable Viewer", font = titleFont)
        self.mainPageSeparator = ttk.Separator(self.mainPage, bootstyle="primary")
        self.startBtn = ttk.Button(self.mainPage, text="START", style="my.TButton", command=lambda:[self.showPage(self.loadPage)])
        self.exitBtn = ttk.Button(self.mainPage, text="EXIT", style="my.TButton", command=self.destroy)

        # Show on screen
        self.mainPageLabel.grid(row = 0 , column=2, sticky = "s", pady=(0,30))
        self.mainPageSeparator.grid(row = 0, column=2, sticky= "swe", pady=(0,0), padx=200)
        self.startBtn.grid(row = 1, column = 2, sticky = "nwe", pady=(60), ipady = 10, padx=150)
        self.exitBtn.grid(row = 1, column = 2, sticky = "nwe", pady=(135,0), ipady=10, padx=150)

    def initLoadPage(self):
        # Setting Page
        self.loadPage.grid(row=0, column=0, sticky="nswe")
        self.loadPage.rowconfigure(0,weight=4)
        self.loadPage.rowconfigure(1,weight=4)
        self.loadPage.rowconfigure(2,weight=2)
        self.loadPage.columnconfigure(0,weight=2)
        self.loadPage.columnconfigure(1,weight=3)
        self.loadPage.columnconfigure(2,weight=2)

        # Predefining title and button styl
        titleFont = ("Arial", 40, "bold")
        self.midButtonStyle = ttk.Style()
        self.midButtonStyle.configure('mid.TButton', font=("Arial", 15))
        self.deleteButtonStyle = ttk.Style()
        self.deleteButtonStyle.configure('s.danger.Outline.TButton', font=("Arial", 10), bootstyle="dark-outline")
        self.clearButtonStyle = ttk.Style()
        self.clearButtonStyle.configure('s.warning.Outline.TButton', font=("Arial", 10), bootstyle="dark-outline")

        # Specific Setting
        column = ("indexNum", "fileName")
        self.loadPageLabel = ttk.Label(self.loadPage, text="Locate The CSV Files", anchor="center", font=titleFont)
        self.openFolderButton = ttk.Button(self.loadPage, text="Open Folder", bootstyle="dark-outline", command=lambda:[self.queryFolderPath()])
        self.fileTree = ttk.Treeview(self.loadPage, columns = column, show="headings", bootstyle="dark")
        self.scrollbar = ttk.Scrollbar(self.loadPage, orient="vertical",command=self.fileTree.yview)
        self.deleteBtn = ttk.Button(self.loadPage, text="Delete", style="s.danger.Outline.TButton", command=lambda:[self.deleteFile()])
        self.clearBtn = ttk.Button(self.loadPage, text="Clear", style="s.warning.Outline.TButton", command=lambda:[self.clearAllFiles()])
        self.backHomeButton = ttk.Button(self.loadPage, text="Back", style="mid.TButton", command=lambda:[self.showPage(self.mainPage)])
        self.nextButton = ttk.Button(self.loadPage, text="Next", style="mid.TButton", command=lambda:[self.showPage(self.viewPage)])

        # Show on screen    
        self.loadPageLabel.grid(row=0,column=0, sticky="nwe", pady=(30,0), columnspan=3)
        self.openFolderButton.grid(row=0,column=1, sticky="s", pady=(0,10), ipady=1, ipadx=40)
        self.fileTree.grid(row=1,column=1, sticky="ns")
        self.scrollbar.grid(row=1,column=1,sticky="ens", padx=(0,33))
        self.fileTree.configure(yscrollcommand=self.scrollbar.set)
        self.deleteBtn.grid(row=2, column=1, sticky="n", pady=(5,0), padx=(100,0))
        self.clearBtn.grid(row=2, column=1, sticky="n", pady=(5,0), padx=(0,100))
        self.backHomeButton.grid(row=2,column=0, sticky="s", pady=(0,20), padx=(0,0), ipadx=20, ipady=5)
        self.nextButton.grid(row=2,column=2, sticky="s", pady=(0,20), padx=(0,0), ipadx=20, ipady=5)

        # Setting table for list of files
        self.fileTree.column("indexNum", anchor="w")
        self.fileTree.column("fileName", anchor="w")
        self.fileTree.heading("indexNum", text="#", anchor="w")
        self.fileTree.heading("fileName", text="File Name", anchor="w")
        self.fileTree.column("indexNum", width=50, minwidth=50, stretch=tk.NO)
        self.fileTree.column("fileName", width=300, minwidth=300, stretch=tk.NO)
        
    def initViewPage(self):
        # Setting Page
        self.viewPage.grid(row=0, column=0, sticky="nswe")
        self.viewPage.columnconfigure(0,weight=2)
        self.viewPage.columnconfigure(1,weight=8)
        self.viewPage.rowconfigure(0,weight=1)

        # Split the screen in half
        self.filterFrame = ttk.Frame(self.viewPage,bootstyle="light")
        self.tableFrame = ttk.Frame(self.viewPage)

        # Setting for the splitted screen
        self.filterFrame.grid(row=0,column=0,sticky="nswe")
        self.tableFrame.grid(row=0,column=1,sticky="nswe")
        # self.tableFrame.grid_propagate(False)


        self.filterFrame.columnconfigure(0,weight=1, uniform='filter')
        self.filterFrame.columnconfigure(1,weight=1, uniform='filter')
        self.filterFrame.columnconfigure(2,weight=1, uniform='filter')
        self.filterFrame.rowconfigure(0,weight=1)
        self.filterFrame.rowconfigure(1,weight=1)
        self.filterFrame.rowconfigure(2,weight=1)
        self.filterFrame.rowconfigure(3,weight=1)
        self.filterFrame.rowconfigure(4,weight=1)
        self.filterFrame.rowconfigure(5,weight=1)
        self.filterFrame.rowconfigure(6,weight=1)
        self.filterFrame.rowconfigure(7,weight=1)
        self.filterFrame.rowconfigure(8,weight=1)
        self.filterFrame.rowconfigure(9,weight=1)

        self.tableFrame.columnconfigure(0, weight=1)
        self.tableFrame.rowconfigure(0, weight=1)
        self.tableFrame.rowconfigure(1, weight=5)
        

        # Predefining
        titleFont = ("Arial", 20, "bold")

        # Table
        column = ["module", "moduleCode", "cohort", "course", "fullPart", "session", "activityDate", "scheduledDay", "startTime", "endTime", "duration","location","size","lecturer","zone"]
        self.scheduleViewer = ttk.Treeview(self.tableFrame, columns = column, show="headings", bootstyle="primary")
        self.scheduleViewer.grid(row=1,column=0, padx=(10,21),pady=(0,21), sticky="nswe")
        self.scheduleViewer.column("module", anchor="w", minwidth=150, width=10)
        self.scheduleViewer.column("moduleCode", anchor="w", minwidth=100, width=10)
        self.scheduleViewer.column("cohort", anchor="w", minwidth=60, width=10)
        self.scheduleViewer.column("course", anchor="w", minwidth=100, width=10)
        self.scheduleViewer.column("fullPart", anchor="w", minwidth=70, width=10)
        self.scheduleViewer.column("session", anchor="w", minwidth=70, width=10)
        self.scheduleViewer.column("activityDate", anchor="w", minwidth=100, width=10)
        self.scheduleViewer.column("scheduledDay", anchor="w", minwidth=80, width=10)
        self.scheduleViewer.column("startTime", anchor="w", minwidth=80, width=10)
        self.scheduleViewer.column("endTime", anchor="w", minwidth=80, width=10)
        self.scheduleViewer.column("duration", anchor="w", minwidth=50, width=10)
        self.scheduleViewer.column("location", anchor="w", minwidth=80, width=10)
        self.scheduleViewer.column("size", anchor="w", minwidth=50, width=10)
        self.scheduleViewer.column("lecturer", anchor="w", minwidth=100, width=10)
        self.scheduleViewer.column("zone", anchor="w", minwidth=50, width=10)

        self.scheduleViewer.heading("module", text="Module", anchor="w")
        self.scheduleViewer.heading("moduleCode", text="Module Code",anchor="w")
        self.scheduleViewer.heading("cohort", text="Cohort",anchor="w")
        self.scheduleViewer.heading("course", text="Course",anchor="w")
        self.scheduleViewer.heading("fullPart", text="Full/Part",anchor="w")
        self.scheduleViewer.heading("session", text="Session",anchor="w")
        self.scheduleViewer.heading("activityDate", text="Date",anchor="w")
        self.scheduleViewer.heading("scheduledDay", text="Day",anchor="w")
        self.scheduleViewer.heading("startTime", text="Start Time",anchor="w")
        self.scheduleViewer.heading("endTime", text="End Time",anchor="w")
        self.scheduleViewer.heading("duration", text="Duration",anchor="w")
        self.scheduleViewer.heading("location", text="Location",anchor="w")
        self.scheduleViewer.heading("size", text="Class Size",anchor="w")
        self.scheduleViewer.heading("lecturer", text="Lecturer",anchor="w")
        self.scheduleViewer.heading("zone", text="Zone",anchor="w")

        self.scheduleScrollVerBar = ttk.Scrollbar(self.tableFrame, orient="vertical",command=self.scheduleViewer.yview)
        self.scheduleScrollHorBar = ttk.Scrollbar(self.tableFrame, orient="horizontal",command=self.scheduleViewer.xview)
        self.scheduleScrollVerBar.grid(row=1,column=0,sticky="ens",padx=(0,10),pady=(0,21))
        self.scheduleScrollHorBar.grid(row=1,column=0,sticky="wes", padx=(10,10),pady=(0,10))
        self.scheduleViewer.configure(yscrollcommand=self.scheduleScrollVerBar.set)
        self.scheduleViewer.configure(xscrollcommand=self.scheduleScrollHorBar.set)
 
        # Specific Setting
        menuButtonStyle = ttk.Style()
        menuButtonStyle.configure("new.primary.Outline.TMenubutton", font=("Arial",13, "bold"))
        resetButton = ttk.Style()
        resetButton.configure("reset.danger.Outline.TButton", font=("Arial",10))
        self.filterLabel = ttk.Label(self.filterFrame, text="Filter Schedules", font=titleFont, bootstyle="inverse-light")
        self.RangeLabel = ttk.Label(self.filterFrame, text="Range Schedules", font=titleFont, bootstyle="inverse-light")
    
        self.startDate = ttk.DateEntry(self.filterFrame, width=8, dateformat="%d-%m-%Y")
        self.endDate = ttk.DateEntry(self.filterFrame, width=8, dateformat="%d-%m-%Y")
        self.applyDateButton = ttk.Button(self.filterFrame, text="Apply Date", bootstyle="primary-Outline",command=lambda:[self.queryFilterDateTime("date",self.startDate.entry.get(),self.endDate.entry.get())])
        self.applyTimeButton = ttk.Button(self.filterFrame, text="Apply Time", bootstyle="primary-Outline",command=lambda:[self.queryFilterDateTime("time",self.startTimeEntry.get(),self.endTimeEntry.get())])
        self.startTimeEntry = ttk.Entry(self.filterFrame, width=13)
        self.endTimeEntry = ttk.Entry(self.filterFrame, width=13)
        self.backLoadButton = ttk.Button(self.filterFrame, text="Back", bootstyle="primary",command=lambda:[self.showPage(self.loadPage)])
        self.scheduleLabel = ttk.Label(self.tableFrame, text="Schedules", font=titleFont)
        self.resetSchedulesButton = ttk.Button(self.filterFrame, text="Reset", style="reset.danger.Outline.TButton",command=lambda:[self.showPage(self.viewPage)])
        self.exportButton = ttk.Button(self.filterFrame, text="Export", bootstyle="primary", command=lambda:[mb.show_error("You chose a folder with no CSV files\nPlease choose a folder with CSV files", "No Files Error")])

        # Menubuttons
        self.moduleMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Module")
        self.moduleCodeMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Module Code")
        self.cohortMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Cohort")
        self.courseMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Course")
        self.fullPartMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Full / Part")
        self.sessionMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Session")
        self.activityDateMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Date")
        self.scheduledDayMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Day")
        self.startTimeMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Start Time")
        self.endTimeMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="End Time")
        self.durationMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Duration")
        self.locationMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Location")
        self.sizeMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Size")
        self.lecturerMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Lecturer")
        self.zoneMenu = ttk.Menubutton(self.filterFrame, style="new.primary.Outline.TMenubutton", text="Zone")

        # Sort By Button
        self.sortIn = tk.BooleanVar()
        self.ascButton = ttk.Radiobutton(self.tableFrame, variable=self.sortIn, text="Ascending", value=True)
        self.desButton = ttk.Radiobutton(self.tableFrame, variable=self.sortIn, text="Descending", value=False)
        self.sortByMenu = ttk.Menubutton(self.tableFrame, style="new.primary.Outline.TMenubutton", text="Sort By")
        self.sortByVar = tk.StringVar()
        sortByOptions = ttk.Menu(self.sortByMenu)
        for x in ["Module","Module Code","Cohort","Course","Full/Part","Session","Date","Day","Start Time","End Time","Duration","Location","Size","Lecturer","Zone"]:
            sortByOptions.add_radiobutton(label=x, variable=self.sortByVar, command=lambda x=x:self.selectedValue("sortBy",x,self.sortIn.get()))
        self.sortByMenu['menu'] = sortByOptions

        self.ascButton.invoke()

        # Show on screen
        self.filterLabel.grid(row=0, column=0,columnspan=3, sticky="w", padx=(10,0))
        self.RangeLabel.grid(row=6,column=0,columnspan=3,sticky="w",padx=(10,0))
        self.scheduleLabel.grid(row=0, column=0, sticky="w",padx=(10,0))
        self.startDate.grid(row=7,column=0, ipadx=10)
        self.endDate.grid(row=7,column=1, ipadx=10)
        self.applyDateButton.grid(row=7,column=2)
        self.startTimeEntry.grid(row=8,column=0)
        self.endTimeEntry.grid(row=8,column=1)
        self.applyTimeButton.grid(row=8,column=2)
        self.backLoadButton.grid(row=9, column=0, sticky="s", pady=(0,10), padx=(0,0), ipadx=20, ipady=5)
        self.resetSchedulesButton.grid(row=9, column=1, sticky="s", pady=(0,15), padx=40, ipadx=20, ipady=1)
        self.exportButton.grid(row=9,column=2,stick="s", pady=(0,10), padx=(0,0), ipadx=20, ipady=5)
        self.moduleMenu.grid(row=1,column=0,sticky="we",padx=10)
        self.moduleCodeMenu.grid(row=1,column=1,sticky="we",padx=10)
        self.cohortMenu.grid(row=1,column=2,sticky="we",padx=10)
        self.courseMenu.grid(row=2,column=0,sticky="we",padx=10)
        self.fullPartMenu.grid(row=2,column=1,sticky="we",padx=10)
        self.sessionMenu.grid(row=2,column=2,sticky="we",padx=10)
        self.activityDateMenu.grid(row=3, column=0,sticky="we",padx=10)
        self.scheduledDayMenu.grid(row=3,column=1,sticky="we",padx=10)
        self.locationMenu.grid(row=3,column=2,sticky="we",padx=10)
        self.startTimeMenu.grid(row=4,column=0,sticky="we",padx=10)
        self.endTimeMenu.grid(row=4,column=1,sticky="we",padx=10)
        self.durationMenu.grid(row=4,column=2,sticky="we",padx=10)
        self.lecturerMenu.grid(row=5,column=0,sticky="we",padx=10)
        self.sizeMenu.grid(row=5,column=1,sticky="we",padx=10)
        self.zoneMenu.grid(row=5,column=2,sticky="we",padx=10)
        self.sortByMenu.grid(row=0,column=0,sticky="e",padx=(0,21),pady=(0,0))
        self.ascButton.grid(row=0,column=0,padx=(0,250), sticky="e")
        self.desButton.grid(row=0,column=0,padx=(0,150), sticky="e")

    def selectedValue(self, category, value, isASC = True):
        if category == "sortBy":
            newCategory = {
                "Module" : "module",
                "Module Code" : "moduleCode",
                "Cohort" : "cohort",
                "Course" : "course",
                "Full/Part" : "fullPart",
                "Session" : "session",
                "Date" : "activityDate",
                "Day" : "scheduledDay",
                "Start Time" : "startTime",
                "End Time" : "endTime",
                "Duration" : "duration",
                "Location" : "location",
                "Size" : "size",
                "Lecturer" : "lecturer",
                "Zone" : "zone",
            }[value]
            self.displayHandler.sort(newCategory, isASC)
            pass
        else:
            self.displayHandler.commonSchedules(self.displayHandler.filterSchedule(category,value))
            self.dataHandler.setRange(self.displayHandler.getResult())
        

        # Post Filtering or Sorting
        self.displaySchedules()
        self.updateOptions()

    def updateOptions(self):
        disabledButtonStyle = ttk.Style()
        disabledButtonStyle.configure("dis.dark.TMenubutton", font=("Arial",13, "bold"))
        enabledButtonStyle = ttk.Style()
        enabledButtonStyle.configure("en.primary.Outline.TMenubutton", font=("Arial",13, "bold"))

        moduleOptions = ttk.Menu(self.moduleMenu)
        self.moduleVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("module")):
            moduleOptions.add_radiobutton(label=x, variable=self.moduleVar, command=lambda x=x:self.selectedValue("module",x))
        self.moduleMenu['menu'] = moduleOptions

        if len(self.dataHandler.getRange("module")) <= 1:
            self.moduleMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.moduleMenu.configure(style="en.primary.Outline.TMenubutton")

        moduleCodeOptions = ttk.Menu(self.moduleCodeMenu)
        self.moduleCodeVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("moduleCode")):
            moduleCodeOptions.add_radiobutton(label=x, variable=self.moduleCodeVar, command=lambda x=x:self.selectedValue("moduleCode",x))
        self.moduleCodeMenu['menu'] = moduleCodeOptions

        if len(self.dataHandler.getRange("moduleCode")) <= 1:
            self.moduleCodeMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.moduleCodeMenu.configure(style="en.primary.Outline.TMenubutton")

        cohortOptions = ttk.Menu(self.cohortMenu)
        self.cohortVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("cohort")):
            cohortOptions.add_radiobutton(label=x, variable=self.cohortVar, command=lambda x=x:self.selectedValue("cohort",x))
        self.cohortMenu['menu'] = cohortOptions

        if len(self.dataHandler.getRange("cohort")) <= 1:
            self.cohortMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.cohortMenu.configure(style="en.primary.Outline.TMenubutton")

        courseOptions = ttk.Menu(self.courseMenu)
        self.courseVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("course")):
            courseOptions.add_radiobutton(label=x, variable=self.courseVar, command=lambda x=x:self.selectedValue("course",x))
        self.courseMenu['menu'] = courseOptions

        if len(self.dataHandler.getRange("course")) <= 1:
            self.courseMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.courseMenu.configure(style="en.primary.Outline.TMenubutton")

        fullPartOptions = ttk.Menu(self.fullPartMenu)
        self.fullPartVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("fullPart")):
            fullPartOptions.add_radiobutton(label=x, variable=self.fullPartVar, command=lambda x=x:self.selectedValue("fullPart",x))
        self.fullPartMenu['menu'] = fullPartOptions

        if len(self.dataHandler.getRange("fullPart")) <= 1:
            self.fullPartMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.fullPartMenu.configure(style="en.primary.Outline.TMenubutton")

        sessionOptions = ttk.Menu(self.sessionMenu)
        self.sessionVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("session")):
            sessionOptions.add_radiobutton(label=x, variable=self.sessionVar, command=lambda x=x:self.selectedValue("session",x))
        self.sessionMenu['menu'] = sessionOptions

        if len(self.dataHandler.getRange("session")) <= 1:
            self.sessionMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.sessionMenu.configure(style="en.primary.Outline.TMenubutton")

        activityDateOptions = ttk.Menu(self.activityDateMenu)
        self.activityDateVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("activityDate")):
            activityDateOptions.add_radiobutton(label=x, variable=self.activityDateVar, command=lambda x=x:self.selectedValue("activityDate",x))
        self.activityDateMenu['menu'] = activityDateOptions

        if len(self.dataHandler.getRange("activityDate")) <= 1:
            self.activityDateMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.activityDateMenu.configure(style="en.primary.Outline.TMenubutton")

        day = ["", "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        scheduledDayOptions = ttk.Menu(self.scheduledDayMenu)
        self.scheduledDayVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("scheduledDay")):
            scheduledDayOptions.add_radiobutton(label=day[x], variable=self.scheduledDayVar, command=lambda x=x:self.selectedValue("scheduledDay",x))
        self.scheduledDayMenu['menu'] = scheduledDayOptions

        if len(self.dataHandler.getRange("scheduledDay")) <= 1:
            self.scheduledDayMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.scheduledDayMenu.configure(style="en.primary.Outline.TMenubutton")

        startTimeOptions = ttk.Menu(self.startTimeMenu)
        self.startTimeVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("startTime")):
            startTimeOptions.add_radiobutton(label=x, variable=self.startTimeVar, command=lambda x=x:self.selectedValue("startTime",x))
        self.startTimeMenu['menu'] = startTimeOptions

        if len(self.dataHandler.getRange("startTime")) <= 1:
            self.startTimeMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.startTimeMenu.configure(style="en.primary.Outline.TMenubutton")

        endTimeOptions = ttk.Menu(self.endTimeMenu)
        self.endTimeVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("endTime")):
            endTimeOptions.add_radiobutton(label=x, variable=self.endTimeVar, command=lambda x=x:self.selectedValue("endTime",x))
        self.endTimeMenu['menu'] = endTimeOptions

        if len(self.dataHandler.getRange("endTime")) <= 1:
            self.endTimeMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.endTimeMenu.configure(style="en.primary.Outline.TMenubutton")

        durationOptions = ttk.Menu(self.durationMenu)
        self.durationVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("duration")):
            durationOptions.add_radiobutton(label=x, variable=self.durationVar, command=lambda x=x:self.selectedValue("duration",x))
        self.durationMenu['menu'] = durationOptions
        
        if len(self.dataHandler.getRange("duration")) <= 1:
            self.durationMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.durationMenu.configure(style="en.primary.Outline.TMenubutton")

        locationOptions = ttk.Menu(self.locationMenu)
        self.locationVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("location")):
            locationOptions.add_radiobutton(label=x, variable=self.locationVar, command=lambda x=x:self.selectedValue("location",x))
        self.locationMenu['menu'] = locationOptions

        if len(self.dataHandler.getRange("location")) <= 1:
            self.locationMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.locationMenu.configure(style="en.primary.Outline.TMenubutton")

        sizeOptions = ttk.Menu(self.sizeMenu)
        self.sizeVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("size")):
            sizeOptions.add_radiobutton(label=x, variable=self.sizeVar, command=lambda x=x:self.selectedValue("size",x))
        self.sizeMenu['menu'] = sizeOptions

        if len(self.dataHandler.getRange("size")) <= 1:
            self.sizeMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.sizeMenu.configure(style="en.primary.Outline.TMenubutton")

        lecturerOptions = ttk.Menu(self.lecturerMenu)
        self.lecturerVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("lecturer")):
            lecturerOptions.add_radiobutton(label=x, variable=self.lecturerVar, command=lambda x=x:self.selectedValue("lecturer",x))
        self.lecturerMenu['menu'] = lecturerOptions

        if len(self.dataHandler.getRange("lecturer")) <= 1:
            self.lecturerMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.lecturerMenu.configure(style="en.primary.Outline.TMenubutton")

        zoneOptions = ttk.Menu(self.zoneMenu)
        self.zoneVar = tk.StringVar()
        for x in self.insertionSort(self.dataHandler.getRange("zone")):
            zoneOptions.add_radiobutton(label=x, variable=self.zoneVar, command=lambda x=x:self.selectedValue("zone",x))
        self.zoneMenu['menu'] = zoneOptions

        if len(self.dataHandler.getRange("zone")) <= 1:
            self.zoneMenu.configure(style="dis.dark.TMenubutton")
        else:
            self.zoneMenu.configure(style="en.primary.Outline.TMenubutton")

    def queryFilterDateTime(self, category, start, end):
        if category == "date":
            dateformat = "%d-%m-%Y"
            start = datetime.datetime.strptime(f"{start}",dateformat).date()
            end = datetime.datetime.strptime(f"{end}",dateformat).date()
            self.displayHandler.rangeSearch(start,end,"activityDate")
        elif category == "time":
            dateformat = "%H:%M"
            start = datetime.datetime.strptime(f"{start}",dateformat).time()
            end = datetime.datetime.strptime(f"{end}",dateformat).time()
            self.displayHandler.rangeSearch(start,end,"time")

        self.displaySchedules()
        self.updateOptions()
            
        
    def queryFolderPath(self):
        folderPath = fd.askdirectory()
        filesList = []
        if folderPath != "":
            try:
                for file in os.listdir(folderPath):
                    if file.endswith(".csv"):
                        filesList.append(os.path.join(folderPath, file))
                self.dataHandler.setFilesPathList(filesList)
                self.displayFiles()

                if len(filesList) == 0:
                    noFilesFound = mb.show_error("You chose a folder with no CSV files\nPlease choose a folder with CSV files", "No Files Error")
            except FileNotFoundError:
                print("ERROR")

    def displayFiles(self):
        for i in self.fileTree.get_children():
            self.fileTree.delete(i)

        filesList = self.dataHandler.getFilesPathList()
        try:
            for index, file in enumerate(filesList):
                self.fileTree.insert("",ttk.END, values=(index+1,file))
        except:
            print("ERROR")

    def clearAllFiles(self):
        for i in self.fileTree.get_children():
            self.fileTree.delete(i)

        self.dataHandler.setFilesPathList([])

    def deleteFile(self):
        selections = self.fileTree.selection()        
        for item in selections:
            self.fileTree.delete(item)

        newList = []
        i = 0
        for row in self.fileTree.get_children():
            for filePath in self.fileTree.item(row)["values"]:
                if i % 2 == 1:
                    newList.append(filePath)
                i+=1


        self.dataHandler.setFilesPathList(newList)


        self.displayFiles()

    def showPage(self, frame):
        if frame == self.viewPage:
            self.geometry("1500x500+100+250")
            self.dataHandler.setSchedules()
            self.displayHandler = DisplayHandler(self.dataHandler.getSchedules(), self.dataHandler.getRangeList())
            self.updateOptions()
            self.displaySchedules()
        else:
            self.geometry("750x500+500+250")

        frame.tkraise()

    def displaySchedules(self):
        for i in self.scheduleViewer.get_children():
                self.scheduleViewer.delete(i)
        dayString = ["","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        try:
            for schedule in self.displayHandler.getResult():
                li = schedule.data.getAll()
                li[7] = dayString[li[7]]
                self.scheduleViewer.insert("", tk.END, value=li)
        except TypeError:
            print("No Files")
            for i in self.scheduleViewer.get_children():
                self.scheduleViewer.delete(i)

    def insertionSort(self,arr):
        newList = []
        for i in arr: newList.append(i)

        for i in range(1,len(newList)):
            value = newList[i]
            pointer = i
            while pointer > 0 and newList[pointer-1] > value:
                newList[pointer] = newList[pointer-1]
                pointer -=1
            newList[pointer] = value

        return newList


# MAIN ====================
a = GUI()