from Crawl_ticket_prices import *
from save_to_database import *

###################
start_date = convert_string_to_date('28/09/2023')
end_date = convert_string_to_date('04/10/2023')
delta = end_date - start_date   # returns timedelta
###################
DEPARTURE = 'SGN'
ARRIVAL = 'VDH'
###################
if __name__ == '__main__':
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        path = 'https://www.vietjetair.com/vi'
        browser = openChrome(path)
        while True:
            try:
                processing(browser, DEPARTURE, ARRIVAL, day)
                DATA = get_all_flights_info(browser, DEPARTURE, ARRIVAL, day)
                browser.quit()
                break
            except:
                continue
        try:
            save_to_database(DATA)
        except:
            print("Unable to save the new data")