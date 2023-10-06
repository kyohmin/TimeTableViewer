import os, csv
import math
import datetime


# ===== Custom Data Structures =====
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
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

    def append(self, data):
        newNode = Node(data)
        if self.head == None:
            self.head = newNode
        
        else:
            currentNode = self.head
            while currentNode.next != None:
                currentNode = currentNode.next

            currentNode.next = newNode

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
    
    def getDetail(self) -> list:
        return self.__module, self.__moduleCode, self.__cohort, self.__course, self.__fullPart, self.__session, self.__activityDate, self.__scheduledDay, self.__startTime, self.__endTime, self.__duration, self.__location, self.__size, self.__lecturer, self.__zone



# ===== Handler Classes =====
class DataHandler:
    def __init__(self):
        self.__schedules = LinkedList()
        self.__filesPathList = []
        self.__folderPath = "/Users/khms/CODE/ALGO/dataset"

        # Hash Set for range and availability check
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

        # Used for initializing HashTable
        self.__rangeList = []

    def storeSchedules(self):
        self.__queryFiles()
        for fileDirectory in self.__filesPathList:
            with open(fileDirectory, "r") as csvfile:
                csvData = csv.reader(csvfile, delimiter=",")
                for row in csvData:
                    if row[0] == '':
                        continue
                    module, moduleCode, cohort, course, fullPart, session = self.__extractData(row[1], row[2])
                    self.__storeRange(module, moduleCode, cohort, course, fullPart, session, row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                    self.__schedules.append(Schedule(module, moduleCode, cohort, course, fullPart, session, row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

        # Storing size of range for optimal hashtable size
        self.__rangeList = [len(self.__moduleRange), len(self.__moduleCodeRange), len(self.__cohortRange), len(self.__courseRange), len(self.__fullPartRange), 
                            len(self.__sessionRange), len(self.__activityDateRange), len(self.__scheduledDayRange), len(self.__startTimeRange), len(self.__endTimeRange), 
                            len(self.__durationRange), len(self.__locationRange), len(self.__sizeRange), len(self.__lecturerRange), len(self.__zoneRange)]
        
    def filteringOption(self, sortedResult:LinkedList) -> LinkedList:
        self.__resetRange()

        for schedule in sortedResult:
            self.__moduleRange.add(schedule.data.getDetail()[0])
            self.__moduleCodeRange.add(schedule.data.getDetail()[1])
            self.__cohortRange.add(schedule.data.getDetail()[2])
            self.__courseRange.add(schedule.data.getDetail()[3])
            self.__fullPartRange.add(schedule.data.getDetail()[4])
            self.__sessionRange.add(schedule.data.getDetail()[5] )
            self.__activityDateRange.add(schedule.data.getDetail()[6])
            self.__scheduledDayRange.add(schedule.data.getDetail()[7])
            self.__startTimeRange.add(schedule.data.getDetail()[8])
            self.__endTimeRange.add(schedule.data.getDetail()[9])
            self.__durationRange.add(schedule.data.getDetail()[10])
            self.__locationRange.add(schedule.data.getDetail()[11])
            self.__sizeRange.add(schedule.data.getDetail()[12])
            self.__lecturerRange.add(schedule.data.getDetail()[13])
            self.__zoneRange.add(schedule.data.getDetail()[14])

        return self.__moduleRange, self.__moduleCodeRange, self.__cohortRange, self.__courseRange, self.__fullPartRange, self.__sessionRange, self.__activityDateRange, self.__scheduledDayRange, self.__startTimeRange, self.__endTimeRange, self.__durationRange, self.__locationRange, self.__sizeRange, self.__lecturerRange, self.__zoneRange

    def __queryFiles(self):
        if self.__folderPath != "":
            try:
                for file in os.listdir(self.__folderPath):
                    if file.endswith(".csv"):
                        self.__filesPathList.append(os.path.join(self.__folderPath, file))
            except FileNotFoundError:
                self.__filesPathList

    def __storeRange(self, module:str, moduleCode:str, cohort:str, course:str, fullPart:str, session:str, activityDate:str, scheduleDay:str, startTime:str, endTime:str, duration:str, location:str, size:str, lecturer:str, zone:str):
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

    def getSchedules(self) -> LinkedList:
        return self.__schedules
    
    def getRange(self) -> list:
        return self.__rangeList
    
    

class DisplayOptionHandler:
    def __init__(self, schedules:str, rangeList:list):
        # In case the user does not want to filter, the lined list's starting point is stored
        self.__originalSchedules = schedules    # For backup when user wants to filter again
        self.__sortedSchedules= self.__originalSchedules

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

    def setFilter(self, schedule:Node):
        self.__moduleHT.add(schedule.data.getDetail()[0], schedule.data)
        self.__moduleCodeHT.add(schedule.data.getDetail()[1], schedule.data)
        self.__cohortHT.add(schedule.data.getDetail()[2], schedule.data)
        self.__courseHT.add(schedule.data.getDetail()[3], schedule.data)
        self.__fullPartHT.add(schedule.data.getDetail()[4], schedule.data)
        self.__sessionHT.add(schedule.data.getDetail()[5], schedule.data)
        self.__activityDateHT.add(schedule.data.getDetail()[6], schedule.data)
        self.__scheduledDayHT.add(schedule.data.getDetail()[7], schedule.data)
        self.__startTimeHT.add(schedule.data.getDetail()[8], schedule.data)
        self.__endTimeHT.add(schedule.data.getDetail()[9], schedule.data)
        self.__durationHT.add(schedule.data.getDetail()[10], schedule.data)
        self.__locationHT.add(schedule.data.getDetail()[11], schedule.data)
        self.__sizeHT.add(schedule.data.getDetail()[12], schedule.data)
        self.__lecturerHT.add(schedule.data.getDetail()[13], schedule.data)
        self.__zoneHT.add(schedule.data.getDetail()[14], schedule.data)
    
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

        self.__sortedSchedules = tmp
        return self.__sortedSchedules

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

    def getResult(self) -> LinkedList:
        return self.__sortedSchedules
    
    def sort(self, category, isAscending):
        return self.__sortedSchedules
        pass

    def mergeSort(self,head, category):
        if head is None or head.next is None:
            return head
        
        left = head
        right = self.getMid(head)
        tmp = right.next
        right.next = None
        right = tmp

        left = self.mergeSort(left, category)
        right = self.mergeSort(right, category)

        return self.merge(left, right, category)

    def getMid(self,head):
        half = head
        towardEnd = head

        while towardEnd.next is not None and towardEnd.next.next is not None:
            half = half.next
            towardEnd = towardEnd.next

        return half

    def merge(self, left, right, category):
        dummy = currentNode = Node(Schedule("a","a","a","a","a","a","a","a","a","a","a","a","a","a","a"))

        while left and right:
            if left.data.getDetail()[category] < right.data.getDetail()[category]:
                currentNode.next = left
                left = left.next
            else:
                currentNode.next = right
                right = left.next
            currentNode = currentNode.next
    
        if left:
            currentNode.next = left
        if right:
            currentNode.next = right

        return dummy.next
        
    def __dateTime(self, strVal):
        a, b, c = int(strVal.split("/"))
        return datetime.time(a,b,c)

# 1: Module, 2: Module code, 3: cohort, 4: Course, 5: Full/Part, 6: Session, 7: Activity Date, 8: ScheduledDay, 9: Start Time, 10: End Time
# 11: Duration, 12: Location 13: Size, 14: Lecturer, 15: Zone



# MAIN ====================

# Initialize DataHandler Class
dataHandler = DataHandler()
# (Place for ENtering path location) #
dataHandler.storeSchedules()

# Initializing Display Option Handler Class
displayOptionHandler = DisplayOptionHandler(dataHandler.getSchedules(),dataHandler.getRange())

a = 1

# Filter Setting
for schedule in dataHandler.getSchedules():
    displayOptionHandler.setFilter(schedule)
    a+=1


# for schedule in displayOptionHandler.filterSchedule("moduleCode", "DCNG"):
#     print(schedule.data.getDetail())


# print("============")

# stack = Stack()
# # stack.push(displayOptionHandler.filterSchedule("moduleCode", "DCNG"))
# # stack.push(displayOptionHandler.filterSchedule("fullPart", "FT"))
# # stack.push(displayOptionHandler.filterSchedule("scheduledDay", "Tuesday"))

# for i in displayOptionHandler.commonSchedules(stack):
#     print(i.data.getDetail())


# print("============")

# # This is for option 
# print(dataHandler.filteringOption(displayOptionHandler.getResult())[8])

# print("========================")


# print(dataHandler.filteringOption(displayOptionHandler.getResult())[1])
# print(a)
# # def filter(category, specificData):


displayOptionHandler.filterSchedule("moduleCode", "DM")
for i in displayOptionHandler.getResult():
    print(i.data.getDetail())

displayOptionHandler.mergeSort(displayOptionHandler.getResult().head,7)