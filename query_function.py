from save_to_database import *
from Crawl_ticket_prices import *
import pandas as pd
import numpy as np

date = convert_string_to_date('27/09/2023')
start_date = convert_string_to_date('28/09/2023')
end_date = convert_string_to_date('29/09/2023')


class FindThroughDatabase:
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def show(self):
        # if len(self.data) == 0:
        #     print("No data")
        # else:
        #     print(self.data)
        # col_names = ['Date', 'No', 'Type', 'Departure', 'Arrival', 'DepartureTime',
        #              'ArrivalTime', 'Business', 'SkyBoss', 'Deluxe', 'Eco', 'Updated']
        # df = pd.DataFrame(np.array(self.get_data()), columns=col_names)
        # print(df)
        print(self.data)

    # def find(self, start_date=None, end_date=None, departure=None, arrival=None):
    #     connt = pyodbc.connect(SQL)
    #     cursor = connt.cursor()
    #     if start_date is None:
    #         cursor.execute(
    #             "select * from TICKET where Departure = ? and Arrival = ?", departure, arrival)
    #     else:
    #         if end_date is None:
    #             end_date = start_date
    #         delta = end_date - start_date   # returns timedelta

    #         for i in range(delta.days + 1):
    #             day = start_date + timedelta(days=i)
    #             if departure is None and arrival is None:
    #                 cursor.execute(
    #                     "select * from TICKET where Date = ?", day.strftime('%Y-%m-%d'))
    #             else:
    #                 cursor.execute("select * from TICKET where Date = ? and Departure = ? and Arrival = ?",
    #                                day.strftime('%Y-%m-%d'), departure, arrival)
    #     self.set_data(cursor.fetchall())

    def find(self, start_date=None, end_date=None, departure=None, arrival=None):
        connt = pyodbc.connect(SQL)
        cursor = connt.cursor()
        if start_date is None:
            cursor.execute(
                "select * from TICKET where Departure = ? and Arrival = ?", departure, arrival)
        else:
            if end_date is None:
                end_date = start_date
            cursor.execute(
                "select * from TICKET where Date >= ? and Date <= ? and Departure = ? and Arrival = ?", start_date, end_date, departure, arrival)
        col_names = ['Date', 'No', 'Type', 'Departure', 'Arrival', 'DepartureTime',
                     'ArrivalTime', 'Business', 'SkyBoss', 'Deluxe', 'Eco', 'Updated']
        df = pd.DataFrame(np.array(cursor.fetchall()), columns=col_names)
        # self.set_data(df)
        return df
        

    def find_cheapest_ticket(self, start_date=None, end_date=None, departure=None, arrival=None):
        col_names = ['Date', 'No', 'Type', 'Departure', 'Arrival', 'DepartureTime',
                     'ArrivalTime', 'Business', 'SkyBoss', 'Deluxe', 'Eco', 'Updated']
        df = self.find(start_date=start_date, end_date=end_date,
                       departure=departure, arrival=arrival)
        df = pd.DataFrame(np.array(self.get_data()), columns=col_names)
        
        def get_info_min(df): #return những records của giá min
            list_features = ['Business','SkyBoss','Deluxe','Eco']
            temp = df[list_features]
            val_min = temp.min(axis = 1)
            return df.loc[val_min[val_min == val_min.min()].index]
        return get_info_min(df)
        # print(df.min())


# f = FindThroughDatabase()
# # f.find(date=None,departure='SGN',arrival='VDH')
# print(f.find(start_date=start_date,end_date=end_date,departure='SGN',arrival='HAN'))
# print(f.find_cheapest_ticket(start_date=start_date,end_date=end_date,departure='SGN',arrival='HAN'))
