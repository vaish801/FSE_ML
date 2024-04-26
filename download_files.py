import glob
import os
import requests
from datetime import datetime
import pandas as pd


def get_data_noaa(city):
    stationNumber= {'denver':'72565003017', 'boulder':'72053300160','fortcollins':'72476994035','coloradosprings':'72466093037'}
    os.makedirs(f'{city}_data', exist_ok=True)
    os.chdir(f'{city}_data')
    for year in range(2000,2025):
        url = f"https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/{stationNumber[city.lower()]}.csv"
        response = requests.get(url)

        if response.status_code == 200:
            with open(f"{year}_{stationNumber[city.lower()]}.csv", "wb") as f:
                f.write(response.content)
            print("File downloaded successfully.")
        else:
            print("Failed to download the file. Status code:", response.status_code)
    csv_files = glob.glob(f"*{stationNumber[city]}.csv")
    df_concat = pd.concat([pd.read_csv(f) for f in csv_files ], ignore_index=True)
    df_concat.to_csv(f"{city}_weather_data.csv", index=False)


def get_data_rcc(city):
    stationNumber = {'denver':'052211','boulder':'050848','fortcollins':'053005','coloradosprings':'051778'}
    date = datetime.today()
    print(date)
    print(type(date))
    url = f"https://data.rcc-acis.org/StnData?sid={stationNumber[city.lower()]}&sdate=2000-01-01&edate={date.date()}&elems=maxt,mint,pcpn,snow&output=csv"
    response = requests.get(url)
    print(url)
    res = response.text.split("\n")
    indexes = list()
    for d in range(0,len(res)-1):
        doc = res[d].split(',')
        if doc.count('M')>2:
            indexes.append(doc[0])
    for i in indexes:
        for d in res:
            if i in d:
                res.remove(d)
    res_str = '\n'.join(res)
    if not os.path.isdir(f"rcc_{stationNumber[city]}"):
        os.mkdir(f"rcc_{stationNumber[city]}")
    if response.status_code == 200:
        with open(f"./rcc_{stationNumber[city]}/{city}_snowfall_data.csv", "w") as f:
            f.write(res_str)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Status code:", response.status_code)

    

city = 'fortcollins'
# get_data_noaa(city)
# get_data_rcc(city)


