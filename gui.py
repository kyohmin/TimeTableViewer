import os, csv
import math
import datetime

import tkinter as tk
import ttkbootstrap as ttk
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
        self.__folderPath = "/Users/khms/CODE/ALGO/dataset"
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
        self.__queryFiles()
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
                        self.__timeInput(row[6]),row[7], row[8], row[9], row[10], row[11]
                    )
                    
                    self.__schedules.append(
                        Schedule(
                            module, moduleCode, cohort, course, fullPart, session, self.__dateInput(row[3]),
                            self.__dateInput(row[3]).isoweekday(), self.__timeInput(row[5]), self.__timeInput(row[6]),
                            row[7], row[8], row[9], row[10], row[11]
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

    def __queryFiles(self):
        if self.__folderPath != "":
            try:
                for file in os.listdir(self.__folderPath):
                    if file.endswith(".csv"):
                        self.__filesPathList.append(os.path.join(self.__folderPath, file))
            except FileNotFoundError:
                self.__filesPathList

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
            tmp = self.__endTime.get(specificValue)
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

        self.__sortedSchedules = tmp.head

    def commonSchedules(self, filterStack:Stack) -> LinkedList:
        # Restore before doing it
        self.restoreSortedSchedules()
    
        while not filterStack.isEmpty():
            node1 = self.__sortedSchedules.head
            node2 = filterStack.pop().head
            resultLinkedList = LinkedList()
            availabilityCheck = set()
            while node2 is not None:
                availabilityCheck.add(node2.data)
                node2 = node2.next

            while node1 is not None:
                if node1.data in availabilityCheck:
                    resultLinkedList.append(node1.data)
                node1 = node1.next

            self.__sortedSchedules = resultLinkedList
            
        return self.__sortedSchedules
        
    def restoreSortedSchedules(self):
        self.__sortedSchedules = self.__originalSchedules

    def rangeSearch(self,start, end, category):
        head = self.__sortedSchedules.head
        self.__mergeSort(head, category)
        endNode = head
        startFound = False
        for i in self.__sortedSchedules.head:
            if i.data.get(category) < start and startFound== False:
                head = i.next
                if i.data.get(category) > start: startFound = True
            if i.data.get(category) > end:  
                break

            endNode = i

        endNode.next = None
        
        self.__sortedSchedules.head = head

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



# 1: Module, 2: Module code, 3: cohort, 4: Course, 5: Full/Part, 6: Session, 7: Activity Date, 8: ScheduledDay, 9: Start Time, 10: End Time
# 11: Duration, 12: Location 13: Size, 14: Lecturer, 15: Zone


class GUI(ttk.Window):
    def __init__(self):
        self.dataHandler = DataHandler()
        # self.displayOptionHandler = DisplayHandler()

        # Make a window setting
        self.initProgram()


        self.viewPage.grid(row=0, column=0, sticky="nswe")
        
        self.showPage(self.mainPage)
        self.mainloop()

    def initProgram(self):
        super().__init__()
        theme = ttk.Style()
        theme.theme_use("flatly")
        self.resizable(False,False)
        self.title("Timetable Viewer")
        self.geometry("750x500+200+200")
        self.rowconfigure(0, weight = 0)
        self.columnconfigure(0, weight=1)

        # Initializing the pages
        self.mainPage = ttk.Frame(self)
        self.loadPage = ttk.Frame(self)
        self.viewPage = ttk.Frame(self, width = 1500, height=500)
        self.initMainPage()
        self.initLoadPage()

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
        self.titleFont = ("Arial", 40, "bold")
        self.myButtonStyle = ttk.Style()
        self.myButtonStyle.configure('my.TButton', font=("Arial", 20))

        # Specific Setting
        self.mainPageLabel = ttk.Label(self.mainPage, text="Timetable Viewer", font = self.titleFont)
        self.mainPageSeparator = ttk.Separator(self.mainPage, bootstyle="primary")
        self.startBtn = ttk.Button(self.mainPage, text="START", style="my.TButton", command=lambda:[self.showPage(self.loadPage)])
        self.exitBtn = ttk.Button(self.mainPage, text="EXIT", style="my.TButton", command=self.destroy)

        # Show on screen       
        self.mainPageLabel.grid(row = 0 , column=2, sticky = "s", pady=(0,30))
        self.mainPageSeparator.grid(row = 0, column=2, sticky= "swe", pady=(0,0), padx=200)
        self.startBtn.grid(row = 1, column = 2, sticky = "nwe", pady=(60), ipady = 10, padx=100)
        self.exitBtn.grid(row = 1, column = 2, sticky = "nwe", pady=(135,0), ipady=10, padx=100)

    def initLoadPage(self):
        self.loadPage.grid(row=0, column=0, sticky="nswe")
        self.loadPage.rowconfigure(0,weight=4)
        self.loadPage.rowconfigure(1,weight=4)
        self.loadPage.rowconfigure(2,weight=2)
        self.loadPage.columnconfigure(0,weight=1)
        self.loadPage.columnconfigure(1,weight=3)
        self.loadPage.columnconfigure(2,weight=1)

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

    def showPage(self, frame):
        frame.tkraise()

# MAIN ====================

a = GUI()




# Initializing Display Option Handler Class
# displayHandler = DisplayHandler(dataHandler.getSchedules(), dataHandler.getRangeList())

# displayHandler.filterSchedule("moduleCode", "DCNG")

# displayHandler.sort("activityDate", True)

# a =0
# for i in displayHandler.getResult():
#     print(i.data.getAll())
#     a+=1
# print(a)

# print("============")
# displayHandler.sort("module")





print("============")

