import pyodbc
SQL = "DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-SQP4F9T; Database=AIRPLANE_TICKET; Trusted_Connection=Yes"

def save_to_database(DATA):
    connt = pyodbc.connect(SQL)
    cursor = connt.cursor()
    for row in range(len(DATA)):
        date = DATA[row]['Date']
        no = DATA[row]['No']
        type = DATA[row]['Type']
        departure = DATA[row]['Departure']
        arrival = DATA[row]['Arrival']
        departureTime = DATA[row]['Departure Time']
        arrivalTime = DATA[row]['Arrival Time']
        business = DATA[row]['Prices']['Business']
        skyBoss = DATA[row]['Prices']['SkyBoss']
        deluxe = DATA[row]['Prices']['Deluxe']
        eco = DATA[row]['Prices']['Eco']
        updated = DATA[row]['Updated']
        print(updated)
        cursor.execute("select * from TICKET where (Date = ? and No = ? and Type = ? and Departure = ? and Arrival = ? and DepartureTime = ? and ArrivalTime = ?) and (Business is null or Business = ?) and (SkyBoss is null or SkyBoss = ?) and (Deluxe is null or Deluxe = ?) and (Eco is null or Eco = ?)",
                       date, no, type, departure, arrival, departureTime, arrivalTime, business, skyBoss, deluxe, eco)
        existing_record = cursor.fetchone()
        if existing_record:  # record exist -> update
            cursor.execute("update TICKET set Updated = ? where Date = ? and No = ? and Type = ? and Departure = ? and Arrival = ? and DepartureTime = ? and ArrivalTime = ? and (Business is null or Business = ?) and (SkyBoss is null or SkyBoss = ?) and (Deluxe is null or Deluxe = ?) and (Eco is null or Eco = ?)",
                          updated, date, no, type, departure, arrival, departureTime, arrivalTime, business, skyBoss, deluxe, eco)
            print('Updated to the database successfully')
        else:  # record not exist -> insert
            cursor.execute("insert into TICKET values (?,?,?,?,?,?,?,?,?,?,?,?)", date, no, type, departure, arrival, departureTime, arrivalTime, business, skyBoss, deluxe, eco, updated)
            print("Save to the database successfully")

            # continue
    cursor.commit()
    connt.close()


########################################################
# connt = pyodbc.connect(SQL)
# cursor = connt.cursor()
# # cursor.execute("delete from TICKET where Date = ?",'2023-10-01')
# # cursor.commit()
