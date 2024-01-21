# day of week identifiers
Mon = 0
Tue = 1
Wed = 2
Thu = 3
Fri = 4
Sat = 5
Sun = 6
weekdayTbl = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# month identifiers
Jan = 1
Feb = 2
Mar = 3
Apr = 4
May = 5
Jun = 6
Jul = 7
Aug = 8
Sep = 9
Oct = 10
Nov = 11
Dec = 12
monthTbl = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

eventTbl = ["sunrise", "sunset"]

# return the position of a possibly abbreviated item in a list
# position is based starting at 1, a result of 0 means the item wasn't found
def pos(item, itemList):
    for i in range(len(itemList)):
        if item.capitalize() == itemList[i][0:len(item)]:
            return i + 1
    return 0

class SchedTime():
    def __init__(self, timeString=""):
        self.timeString = timeString
        self.year = []
        self.month = []
        self.day = []
        self.hour = []
        self.minute = []
        self.weekday = []
        self.event = []
        self.error = False
        self.errorMsg = ""
        self.parseString(self.timeString)
        if self.error:
            print('"'+self.timeString+'" - ***', self.errorMsg, "***")
        else:
            print('"'+self.timeString+'" -', (self.year, self.month, self.day, self.hour, self.minute, self.weekday, self.event))

    # parse a schedTime string specification
    def parseString(self, timeString):
        tsList = timeString.split(" ")      # first, split the string on spaces
        self.parseList(tsList)

    # parse a list of items either space or comma delimited
    def parseList(self, tsList):
        for ts in tsList:
            rangeItems = ts.split("-")
            if len(rangeItems) == 2:        # item contains a range
                if rangeItems[0] in ["", ":"]:
                    self.parseItem(ts)      # the - is actually a negative sign
                else:
                    self.parseList(self.parseRange(rangeItems))
            elif len(rangeItems) > 2:
                self.error = True
                self.errorMsg = "Invalid range"
            else:
                listItems = ts.split(",")
                if len(listItems) >= 2:     # item contains a comma separated list
                    self.parseList(listItems)
                else:                       # item contains a single value
                    self.parseItem(ts)

    # parse a single item
    def parseItem(self, ts):
        try:                                        # is it an integer?
            tsInt = int(ts)
            if tsInt > 31:                          # valid year
                self.year.append(tsInt)
            elif (tsInt <= 31) and (tsInt > 0):     # valid day
                self.day.append(tsInt)
            else:
                self.error = True
                self.errorMsg = "Invalid day"
        except ValueError:                          # not an integer
            if ts != "":                            # empty string is valid
                if pos(ts, monthTbl):               # item is a month
                    self.month.append(pos(ts, monthTbl))
                elif pos(ts, weekdayTbl):           # item is a weekday
                    self.weekday.append(pos(ts, weekdayTbl) - 1)
                elif ts.lower() in eventTbl:        # item is an event
                    self.event.append(ts.lower())
                else:                               # item is a time
                    tsTime = ts.split(":")          # split hours and minutes
                    if len(tsTime) == 2:            # exactly one colon
                        try:
                            if tsTime[0] != "":     # time contains an hour
                                self.hour.append(int(tsTime[0]))
                            if tsTime[1] != "":     # time contains a minute
                                self.minute.append(int(tsTime[1]))
                        except ValueError:          # not an integer
                            self.error = True
                            self.errorMsg = "Invalid time"
                    elif len(tsTime) > 2:           # too many colons
                        self.error = True
                        self.errorMsg = "Invalid time"
                    elif len(tsTime) < 2:           # no colon
                        self.error = True
                        self.errorMsg = "Invalid spec"

    # expand a range into a list
    def parseRange(self, rangeItems):
        pos1 = pos(rangeItems[0], monthTbl)
        pos2 = pos(rangeItems[1], monthTbl)
        if pos1 and pos2 and (pos1 < pos2):         # both items are months
            return monthTbl[pos1-1:pos2]
        else:
            pos1 = pos(rangeItems[0], weekdayTbl)
            pos2 = pos(rangeItems[1], weekdayTbl)
            if pos1 and pos2 and (pos1 < pos2):     # both items are weekdays
                return weekdayTbl[pos1-1:pos2]
        self.error = True
        self.errorMsg = "Invalid values in range"
        return []

# valid time strings
SchedTime("2024 Dec 25")
SchedTime("Dec 25 2024")
SchedTime("25 Dec 2024")
SchedTime("17:00")
SchedTime("Jun 21 Sunrise")
SchedTime("Friday 17:00")
SchedTime("Apr-Sep 13:00")
SchedTime(":00,:10,:20,:30,:40,:50")
SchedTime("Mon-Fri 12:00")
SchedTime("may,aug sunset")
SchedTime("Mon,Wed,Fri 18:00")
SchedTime("Tu,Th 20:00")
SchedTime("2023 September 24")
SchedTime("1 9:00")
SchedTime("30 12:00")
SchedTime("sunset :-20")
SchedTime("Sunrise -1:00")

# valid strings that don't look like they should be
SchedTime("")
SchedTime("1066 Dec 25")
SchedTime("Jun 42 sunrise")
SchedTime("Mon,Wed,Fri,Feb 18:00")
SchedTime("Jan Wed Fri Feb")
SchedTime("12:")
SchedTime("1,2,4,8,16,32,64,128,256")

# invalid time strings
SchedTime("17:00:00")
SchedTime("Fridays 17:00")
SchedTime("Apr-Sep-Dec 13:00")
SchedTime(":00,:1O,:20,:30,:40,:50")
SchedTime("Fri-Mon 12:00")
SchedTime("May,Aug noon")
SchedTime("2023 Septober 24")
SchedTime("-1 9:00")
SchedTime("0 12:00")
SchedTime("sunset -20")
SchedTime("random garbage")
