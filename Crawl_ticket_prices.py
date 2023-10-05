from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re  # Regular expression
from datetime import date, timedelta, datetime
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
#################################################

def openChrome(path):
    # Mở Chrome và cho full màn hình
    # path = 'https://www.vietjetair.com/vi'
    chrome_driver_path = ChromeDriverManager().install()
    chrome_service = Service(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(service=chrome_service)
    browser.maximize_window()
    while True:
        try:
            browser.get(path)
            break
        except:
            continue
    return browser


def chooseDeparture(browser, symbol):
    while True:
        try:
            browser.find_element(
                By.CLASS_NAME, "MuiFormControl-root.MuiTextField-root.MuiFormControl-fullWidth").click()
            time.sleep(1)
            locations = browser.find_elements(By.CLASS_NAME, 'MuiPaper-root.MuiPaper-elevation1.MuiExpansionPanel-root.Mui-expanded.MuiExpansionPanel-rounded.MuiPaper-rounded')[
                1].find_element(By.CLASS_NAME, 'MuiExpansionPanelDetails-root').find_elements(By.CLASS_NAME, 'MuiBox-root')
            for location in locations:
                if symbol in location.text:
                    location.click()
                    break
            break
        except:
            continue


def chooseArrival(browser, symbol):
    while True:
        try:
            browser.find_elements(
                By.CLASS_NAME, "MuiInputBase-input.MuiOutlinedInput-input")[1].click()
            time.sleep(1)
            locations = browser.find_elements(By.CLASS_NAME, 'MuiCollapse-container.MuiCollapse-entered')[1].find_element(
                By.CLASS_NAME, 'MuiExpansionPanelDetails-root').find_elements(By.CLASS_NAME, 'MuiBox-root')
            for location in locations:
                if symbol in location.text:
                    location.click()
                    break
            break
        except:
            continue

def choose_day_in_calendar(browser, day):
        #Done choosing day
        calendar_frame = browser.find_element("xpath","/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[3]")
        disable_day = calendar_frame.find_elements(By.CLASS_NAME,'rdrDayDisabled')
        passive_day = calendar_frame.find_elements(By.CLASS_NAME,'rdrDayPassive')
        full_day = calendar_frame.find_elements(By.CLASS_NAME,'rdrDay')
        #get available day
        object_available_day = list(set(list(set(full_day).difference(passive_day))).difference(disable_day))

        #click on a right day
        for ele in object_available_day:
            if day == int(ele.text):
                ele.click()
                time.sleep(2)
                break

def chooseDate(browser, date):
    day = date.day
    month = date.month
    year = date.year
    #Click chỗ ngày đi để hiện lên calendar để chọn
    browser.find_element(
        By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]").click()
    while True:
        # time.sleep(2)
        calendar = browser.find_element(By.CLASS_NAME,"rdrMonthName")
        month_value = calendar.text.split(" ")[1]
        year_value = calendar.text.split(" ")[-1]
        if year == int(year_value):
            if month == int(month_value):
                choose_day_in_calendar(browser,day)
                break
            elif month < int(month_value):
                browser.find_element('xpath','/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/button[1]').click()
                continue
            else:
                #click next button
                browser.find_element('xpath','/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/button[2]').click()   
                continue
        elif year < int(year_value):
            #click previous button
            browser.find_element('xpath','/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/button[1]').click()
            continue
        else:
            #click next button
            browser.find_element('xpath','/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/button[2]').click()
            continue
    

def scroll_to_the_end(browser):
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def processing(browser, departure_symbol, arrival_symbol, date):
    # chấp nhận cookie
    while True:
        try:
            browser.find_element(
                By.CSS_SELECTOR, "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper.jss58 > div > div > div:nth-child(3) > button").click()
            break
        except:
            continue
    # Chọn vé 1 chiều
    while True:
        try:
            browser.find_elements(
                By.CLASS_NAME, "MuiFormControlLabel-root")[1].click()
            break
        except:
            continue

    # Choose Departure Place
    chooseDeparture(browser, departure_symbol)
    # Choose Arrival Place
    chooseArrival(browser, arrival_symbol)
    time.sleep(1)
    # Choose Date
    chooseDate(browser, date)
    # Tắt bảng chọn số vé
    browser.find_element(
        By.CLASS_NAME, 'MuiInputBase-root.MuiInputBase-formControl.MuiInputBase-adornedStart.MuiInputBase-adornedEnd').click()
    
    #Click nút 'Tìm vé rẻ nhất'
    browser.find_element(By.CLASS_NAME,'MuiTypography-root.pointer.MuiTypography-h3.MuiTypography-colorTextSecondary').click()
    #Bấm nút tìm chuyến bay
    browser.find_element(By.CLASS_NAME,'MuiButtonBase-root.MuiButton-root.MuiButton-contained').click()

    #Click on the date
    while True:
        try:
            browser.find_element(By.XPATH,f"//p[text() ='{date.day}']").click()
            break
        except:
            continue
    #Bấm nút 'Đi tiếp'
    while True:
        try:
            browser.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div/div/div[2]/button").click()
            break
        except:
            continue
    
    scroll_to_the_end(browser)

def get_flight_info(info,departure,arrival,date):
    FLIGHT_INFO = {}
    FLIGHT_INFO['Date'] = str(date)
    FLIGHT_INFO['No'] = info[0]
    FLIGHT_INFO['Departure Time'] = info[1].split(" ")[0]
    FLIGHT_INFO['Arrival Time'] = info[1].split(" ")[-1]
    FLIGHT_INFO['Type'] = info[2]
    FLIGHT_INFO['Departure'] = departure
    FLIGHT_INFO['Arrival'] = arrival

    prices_list = info[3:]
    prices = {
        'Business': 0,
        'SkyBoss': 0,
        'Deluxe': 0,
        'Eco': 0
    }
    for index in range(len(prices.keys())):
        if prices_list[index] == 'Hết chỗ':
            prices[list(prices.keys())[index]] = None
            continue
        else:
            prices[list(prices.keys())[index]] = int(prices_list[index].replace(',', '')) * 1000
    FLIGHT_INFO['Prices'] = prices
    return FLIGHT_INFO
    
def get_all_flights_info(browser,departure,arrival, date):
    #get all flights information
    eles = browser.find_elements('xpath','/html/body/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/div[4]/div[2]/div[1]/div')
    date_time_now = str(datetime.now())
    list_info = []
    for ele in eles:
        info = [value for value in ele.text.split("\n") if 'VND' not in value] #info of each flight
        one_flight_info = get_flight_info(info,departure,arrival, date)
        one_flight_info['Updated'] = date_time_now
        list_info.append(one_flight_info)
    return list_info

def convert_string_to_date(string_date):
    try:
        return datetime.strptime(string_date,'%d/%m/%Y').date()
    except ValueError as e:
        print("Error: day is out of range for month")
##################################################
# if __name__ == "__main__":
#     # st = input("Date: ")
#     date = convert_string_to_date('01/10/2023')
#     path = 'https://www.vietjetair.com/vi'
#     browser = openChrome(path)
#     # AIRPLANE_TICKETS = {}
#     while True:
#         try:
#             processing(browser, 'SGN', 'HAN', date)
#             print(get_all_flights_info(browser,'SGN', 'HAN', date))
#             break
#         except:
#             continue
        