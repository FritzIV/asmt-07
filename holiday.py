from datetime import datetime,date
import json
from bs4 import BeautifulSoup
import requests
import dataclasses
from pydantic.dataclasses import dataclass
import copy


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date -- pydantic dataclass enforces the type hints when creating a Holiday object
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str
    date: date
    
    def __str__ (self):
        return self.name
        # String output
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    innerHolidays: list[Holiday] = dataclasses.field(default_factory=list)
   
    def addHoliday(self, holidayObj, output = True):
        if isinstance(holidayObj, Holiday):
            if holidayObj not in self.innerHolidays:
                if output:
                    print(f"Success:\n {holidayObj} ({holidayObj.date}) has been added to the holiday list.")
                self.innerHolidays.append(holidayObj)
            else:
                print(f'{holidayObj} is already in holiday list')
        else:
            print(f"{holidayObj} is not a Holiday Object")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self, HolidayName, Date, output = True):
        for holiday in self.innerHolidays:
            if HolidayName == holiday.name and Date == holiday.date:
                return holiday
        if output:
            print(f'{HolidayName} and {Date} not in list of holidays')
        return None
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName, Date):
        removed = ''
        range_ = len(self.innerHolidays)
        i = 0
        while i < range_:
            if HolidayName == self.innerHolidays[i].name and Date == self.innerHolidays[i].date:
                removed = self.innerHolidays.pop(i)
                print(f"Success: \n{removed} has been removed from the holiday list.")
                range_ -= 1
            i += 1
        if removed == '':
            print(f'Error: \n{HolidayName} not found.')
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self, filelocation):
        with open(filelocation, 'r') as f:
            data = json.load(f)
        for hol in data['holidays']:
            tmpDate = datetime.strptime(hol['date'],"%Y-%m-%d").date()
            tmpName = hol['name']
            tmpHoliday = Holiday(tmpName,tmpDate)
            self.addHoliday(tmpHoliday, output=False)
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, filelocation):
        holiday_dict = {"holidays":[{'name':hol.name, 'date':hol.date.strftime('%Y-%m-%d')} for hol in self.innerHolidays]}
        with open(filelocation, 'w') as f:
            json.dump(holiday_dict, f, indent=4)
        # Write out json file to selected file.
        
    def scrapeHolidays(self):
        for year in range(2020,2025):
            html = requests.get(f"https://www.timeanddate.com/holidays/us/{year}").text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', attrs={'id':'holidays-table'})
            tbody = table.find('tbody')
            for date_, holiday_ in zip(tbody.find_all('th'),tbody.find_all('a')):
                fDate = datetime.strptime((date_.text + " " + str(year)),"%b %d %Y").date()
                temp_holiday = Holiday(date = fDate,name = holiday_.text)
                if temp_holiday not in self.innerHolidays:
                    self.addHoliday(temp_holiday, output=False)
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        return len(self.innerHolidays)
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        holidays = sorted(list(filter(lambda x: (x.date.isocalendar()[1] == int(week_number) and x.date.year == int(year)) , self.innerHolidays)), key = lambda x: x.date)
        
        if week_number == 1: # This if statement fixes the issue of the last days of december sometimes being counted in the first week of the year
            range_ = len(holidays)
            i = 0
            while i < range_:
                if holidays[i].date.month == 12:
                    holidays.pop(i)
                    range_ -= 1
                i += 1

        elif week_number == 52: # This elif statement fixes the issue of the first days of january sometimes being counted in the last week of the year
            range_ = len(holidays)
            i = 0
            while i < range_:
                if holidays[i].date.month == 1:
                    holidays.pop(i)
                    range_ -= 1
                i += 1
        return holidays
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, holidayList):
        for hol in holidayList:
            print(hol)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    def getWeather(self, weekNum):
        pass
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        year = datetime.now().year
        week = datetime.now().isocalendar()[1]
        current = self.filter_holidays_by_week(year,week)
        self.displayHolidaysInWeek(current)
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results


def main():
    # 1. Initialize HolidayList Object
    hInit = HolidayList()

    # 2. Load JSON file via HolidayList read_json function
    hInit.read_json('holidays.json')

    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    hInit.scrapeHolidays()

    h = copy.deepcopy(hInit) # use initial HolidayList to compare with h when users exit to see if they have made changes

    # 3. Create while loop for user to keep adding or working with the Calendar
    print('start_up') # turn into a variable for text pulled from config
    stillWorking = True
    while stillWorking:

    # 4. Display User Menu (Print the menu)
        print('main_menu') # turn into a variable for text pulled from config

    # 5. Take user input for their action based on Menu and check the user input for errors
        action = ''
        goodInput = False
        while not goodInput:
            action = input('Input a number[1-5]: ')
            action = action.strip()
            if action in ['1','2','3','4','5']:
                goodInput = True
            else:
                print(f'{action} is not a number 1-5')

    # 6. Run appropriate method from the HolidayList object depending on what the user input is
        if      action == '1':
            print('add_a_holiday')
            userHoliday = input('Holiday: ')
            userDate = ''
            goodInput = False
            while not goodInput:
                userDate = input(f'Date for {userHoliday}: ')
                userDate = userDate.strip()
                try:
                    userDateF = datetime.strptime(userDate,"%Y-%m-%d").date()
                except ValueError:
                    print(f'Error: \n{userDate} is not a valid date. Please try again.')
                    continue
                else:
                    goodInput = True
            holToAdd = Holiday(userHoliday, userDateF)
            h.addHoliday(holToAdd)

        elif    action == '2':
            print('remove_a_holiday')
            userHoliday = input('Holiday Name: ')
            userDate = ''
            goodInput = False
            while not goodInput:
                userDate = input(f'Date for {userHoliday}: ')
                userDate = userDate.strip()
                try:
                    userDateF = datetime.strptime(userDate,"%Y-%m-%d").date()
                except ValueError:
                    print(f'Error: \n{userDate} is not a valid date. Please try again.')
                    continue
                else:
                    goodInput = True
            h.removeHoliday(userHoliday, userDateF)

        
        elif    action == '3':
            print('save_holiday_list')
            userSave = ''
            goodInput = False
            while not goodInput:
                userSave = input('Are you sure you want to save your changes? [y/n] ')
                userSave = userSave.strip().lower()
                if userSave in ['y','n']:
                    goodInput = True
                else:
                    print(f'{userSave} is not a valid input')
                if userSave == 'y':
                    h.save_to_json('holiday_list.json')
                    print('Success: \nYour changes have been saved.')
                else:
                    print('Canceled: \nHoliday list file save canceled')

        elif    action == '4':
            print('view_holidays')
            userYear = input('Which year?: ')
            userWeek = input('Which week? #[1-52, Leave blank for the current week and year]: ')
            if userWeek == '':
                h.viewCurrentWeek()
            else:
                yearRange = [str(i) for i in range(1,3001)]
                weekRange = [str(i) for i in range(1,53)]
                if userYear not in yearRange or userWeek not in weekRange:
                    print(f'Error: \nWeek {userWeek} and year {userYear} are out of range.')
                else:
                    hol_list = h.filter_holidays_by_week(userYear,userWeek)
                    if len(hol_list) == 0:
                        print('No holidays added for that week.')
                    else:
                        h.displayHolidaysInWeek(hol_list)
        
        elif    action == '5':
            print("exit")
            if hInit == h: # if no changes have been made
                userExit = ''
                goodInput = False
                while not goodInput:
                    userExit = input('Are you sure you want to exit? [y/n] ')
                    userExit = userExit.strip().lower()
                    if userExit in ['y','n']:
                        goodInput = True
                    else:
                        print(f'Error: \n{userExit} is not a valid input')
                if userExit == 'y':
                    print('Goodbye!')
                    stillWorking = False
            else: 
                userExit = ''
                goodInput = False
                while not goodInput:
                    userExit = input(
                    'Are you sure you want to exit? \nYour changes will be lost. \n[y/n] ')
                    userExit = userExit.strip().lower()
                    if userExit in ['y','n']:
                        goodInput = True
                    else:
                        print(f'{userExit} is not a valid input')
                if userExit == 'y':
                    print('Goodbye!')
                    stillWorking = False


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.