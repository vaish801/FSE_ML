import pandas as pd
import os

# city_name = "boulder"
# city_name ="fort_collins"
# city_name = "aspen"
city_name = "coloradosprings"
stationNumber = {'denver':'052211','boulder':'050848','fortcollins':'053005','coloradosprings':'051778'}
folder1_name = f"{city_name}_data"
folder2_name = f"rcc_{stationNumber[city_name]}"
file_name1 = f"{city_name}_snowfall_data.csv"
file_name2 = f"{city_name}_weather_data.csv"


def merge_weather_data(folder1_name, folder2_name,file_name1, file_name2):
    weather_data = pd.read_csv(f"./{folder2_name}/{file_name1}")
    snowfall_data = pd.read_csv(f"./{folder1_name}/{file_name2}")
    weather_data['DATE'] = pd.to_datetime(weather_data['DATE'], format='%d-%m-%Y')
    snowfall_data['DATE'] = pd.to_datetime(snowfall_data['DATE'])
    # weather_data = pd.read_csv(f"./{folder_name}/{file_name1}")
    # snowfall_data = pd.read_csv(f"./{folder_name}/{file_name2}")

    final_weather_snowfall_data = pd.merge(snowfall_data, weather_data, how="inner", on=["DATE"])

    columns = ["DATE","TEMP","DEWP","VISIB","WDSP","MAXTEMP","MINTEMP","PREC","SNF"]
    final_weather_snowfall_data = final_weather_snowfall_data[columns]

    final_weather_snowfall_data.to_csv(f"{city_name.lower()}_merged_weather_data.csv")

merge_weather_data(folder1_name,folder2_name, file_name1, file_name2)