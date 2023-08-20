day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def add_1_day(month, day):
    if day == day_in_month[month-1]:
        month += 1
        day = 1
        if month > 12:
            month = 1
        return month, day
    return month, day+1
    
def sub_1_day(month, day):
    if day == 1:
        month -= 1
        if month<1:
            month = 12
        day = day_in_month[month-1]
        return month, day
    return month, day-1
    
def add_day(month, day, days):
    if days<0:
        return sub_day(month, day, -days)
    for _ in range(days):
        month, day = add_1_day(month, day)
    return month, day
    
def sub_day(month, day, days):
    for _ in range(days):
        month, day = sub_1_day(month, day)
    return month, day

def bitween_days(day1, day2):#day1 - day2
    if day1[0] == day2[0]:
        return day1[1]-day2[1]
    if day1[0] > day2[0]:
        sum = day1[1]
        for i in range(day1[0]-2, day2[0]-2, -1):
            sum += day_in_month[i]
        return sum - day2[1]
    if day1[0] < day2[0]:
        return -bitween_days(day2, day1)
    
#print(bitween_days([7, 21], [8, 17]))