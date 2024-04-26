import joblib
import datetime
import requests
import pandas as pd
from datetime import timedelta
import csv 
import sys
import os
# Redirect warnings to null device
sys.stderr = open(os.devnull, 'w')

def update_data(city):
    filename = pd.read_csv(f'final_{city}_merged_weather_data.csv')
    csv_cols = filename.columns
    station_names = {"denver":"72565003017", "boulder":"72053300160", "fortcollins":"72476994035","coloradosprings":"72466093037"}
    stationNumber = station_names[city.lower()]
    today = datetime.date.today()
    year = today.year
    url = f"https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/{stationNumber}.csv"
    response = requests.get(url)
    res = response.text.split("\n")
    keys = res[0].split(",")
    values = res[-2].split(",")
    last_date = values[1].strip('"')
    l_date = filename['DATE'].iloc[-1]
    date1 = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(l_date, "%d-%m-%Y")
    d = (date1-date2).days
    count = 0
    # print(d)
    for i in range (d-1,-1,-1):
        values = res[-2-i].split(",")
        # print(values)
        values[5] = values[5]+values[6]
        del values[6]
        data = dict(list(zip(keys,values)))
        cleanedData = dict()
        for key,value in data.items():
            clean_key = key.strip('"')
            clean_value = value.strip('"')
            cleanedData[clean_key] = clean_value
        # print(cleanedData)
        curr_date = cleanedData['DATE']
        # print(curr_date)
    # filename = pd.read_csv(f'final_{city}_merged_weather_data.csv')    ########
    # csv_cols = filename.columns
        snow_data_dict = {'denver':"052211",'boulder':"050848",'fortcollins':'053005','coloradosprings':'051778'}
        station_number_snow = snow_data_dict[city] #Denver
    # to_submit_date = today-timedelta(days = 2)
    # # print(to_submit_date)
        curr_date = datetime.datetime.strptime(curr_date, '%Y-%m-%d')
        to_submit_date = curr_date.strftime('%Y-%m-%d')
        # print(to_submit_date)
        url1 = f"https://data.rcc-acis.org/StnData?sid={station_number_snow}&sdate={to_submit_date}&edate={to_submit_date}&elems=maxt,mint,pcpn,snow&output=csv"
        # print(url)
        response1 = requests.get(url1)
        res1 = response1.text.split('\n')
        snow_data_values = res1[-2].split(',')
        snow_data_keys = ['MAXTEMP', 'MINTEMP', 'PREC','SNF']
        del snow_data_values[0]
        # print(snow_data_values)
        snow_data = dict(list(zip(snow_data_keys,snow_data_values)))
    # # print("hellllllllllllllllo",snow_data_values)
    # # print(cleanedData)
        append_values = dict()
        for col in csv_cols:
            if col != 'TEMP':
                if col in list(cleanedData.keys()):
                    if col =='DATE':
                        original_date = datetime.datetime.strptime(cleanedData['DATE'], "%Y-%m-%d")
                        check_date_str = original_date.strftime("%Y-%m-%d")
                        new_date_str = original_date.strftime("%d-%m-%Y")
                        append_values[col]=new_date_str
                        # print(new_date_str)
                    else:
                        append_values[col]=cleanedData[col]
        final_data = append_values.update(snow_data)
        # print(append_values)
        append_values['TEMP'] = cleanedData['TEMP']
        for key,value in append_values.items():
            dt = 0
            # print(key,value)
            if(key=='PREC' and (value == 'T' or value == 'M')):
                append_values[key] = 0.0
            if(key=='SNF' and (value == 'T' or value == 'M')):
                append_values[key] = 0
            if(key=='MAXTEMP' and value == 'M'):
                if (append_values['TEMP']=='M' or append_values['MINTEMP']=='M'):
                    dt = append_values['DATE']
                    append_values.clear()
                    break
                else:
                    append_values[key] = int(append_values['TEMP'])*2 /int(append_values['MINTEMP'])
            if(key=='MINTEMP' and value == 'M'):
                if (append_values['TEMP']=='M' or append_values['MAXTEMP']=='M'):
                    dt = append_values['DATE']
                    append_values.clear()
                    break
                else:
                    append_values[key] = int(append_values['TEMP'])*2 /int(append_values['MAXTEMP'])
            # print(dt, key)
        if (len(append_values)>0):
            del append_values['TEMP']
            # if(dt==0):
            #     print("hiiii")
            data1 = list(append_values.values())
            # print(data1)
            # with open(f'finall_{city}_merged_weather_data.csv','a',newline='') as file:
            with open(f'final_{city}_merged_weather_data.csv','a',newline='') as file:
                writer = csv.writer(file)
                count +=1
                file.seek(0, 2) 
                if file.tell() == 0:  
                    writer.writeheader()  
                
                writer.writerow(data1)

        
    filename = pd.read_csv(f'final_{city}_merged_weather_data.csv')
    filename['DATE'] = pd.to_datetime(filename['DATE'])
    filename.set_index('DATE', inplace=True)
    params = filename.columns
    for p in params:
        test =   filename[p].iloc[-count:]
        model = joblib.load(f'final_{city}_{p}.joblib')
        model.update(test)
        


# city = 'fortcollins'
# update_data(city.lower())