import glob
from datetime import datetime,timedelta
import pandas as pd
import joblib
import re
import warnings
warnings.filterwarnings('ignore')
import sys
import os
# Redirect warnings to null device
sys.stderr = open(os.devnull, 'w')

def predict_parameters(city,end_date):
    # warnings.simplefilter("ignore")
    # models = []
    warnings.filterwarnings("ignore", message="No supported index is available", category=UserWarning)
    city = city.lower()
    today_date = datetime.today().strftime('%d-%m-%Y')
    # t_date = datetime.strptime(today_date,'%d-%m-%Y').date()
    # tomorrow = t_date+ timedelta(days = 1)
    filename = pd.read_csv(f'final_{city}_merged_weather_data.csv')
    date2 = filename['DATE'].iloc[-1]
    date1 = datetime.strptime(today_date, '%d-%m-%Y')
    date2 = datetime.strptime(date2, '%d-%m-%Y')
    date3 = datetime.strptime(end_date, '%d-%m-%Y')
    tom = date2 + timedelta(days = 1)
    difference = abs((date1 - date2).days)
    difference2 = abs((date3-date1).days) 
    d= difference+difference2
    models = glob.glob(f"final_{city}*.joblib")
    date_range = pd.date_range(start=tom, end=date3, normalize=True)
    forecasts = dict()
    formatted_dates = [date.strftime('%d-%m-%Y') for date in date_range]
    for model in models:
        loadmodel=joblib.load(model)

        predictions=pd.Series(loadmodel.predict(n_periods=d))  #, index = date_range
        match = re.search(r'_([A-Za-z0-9]+)\.', model)
        param = match.group(1)
        forecasts[param] = list(predictions)
    # print(forecasts)
    data_of_days = dict()
    for i in range(0,len(formatted_dates)):
        vals = dict()
        for key,value in forecasts.items():
            vals[key] = value[i]
            # print( vals)
        data_of_days[str(formatted_dates[i])] = vals
    # print(data_of_days)
    for key,val in data_of_days.items():
        # for key1,val1 in data_of_days[key].items():
        if (data_of_days[key]['VISIB'] <= 0.25 and data_of_days[key]['WDSP'] >= 35 and data_of_days[key]['SNF'] >= 18 and data_of_days[key]['MAXTEMP']<= 10):
            return 'Blizzard Warning',key
        if (data_of_days[key]['VISIB'] <= 4 and data_of_days[key]['WDSP'] >= 10 and data_of_days[key]['SNF'] >= 6 and data_of_days[key]['MINTEMP']<= 32):
            return 'Snowstorm Warning',key
        if ( data_of_days[key]['SNF'] <= 2 and data_of_days[key]['SNF']>= 0.5 and data_of_days[key]['MAXTEMP']<= 42):
            return 'Snow Flurries Warning',key
        if (data_of_days[key]['WDSP'] >= 25 and data_of_days[key]['MINTEMP']<= -2):
            return 'Wind Chills Warning',key
        if ( data_of_days[key]['MAXTEMP']>= 90):
            return 'Heat Waves Warning',key
        if (data_of_days[key]['WDSP'] >= 40 ):
            return 'High Winds Warning',key
    
    return 'No Extreme Weather Conditions'
            # print(key1)

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
# predict_parameters("boulder","30-04-2024")


# warnings.simplefilter("ignore")