import joblib
import pandas as pd
def update_model(city):
    # params = ['DEWP','VISIB', 'WDSP','MAXTEMP','MINTEMP','PREC','SNF']
    filename = pd.read_csv(f'final_{city}_merged_weather_data.csv')
    filename['DATE'] = pd.to_datetime(filename['DATE'])
    filename.set_index('DATE', inplace=True)
    params = filename.columns
    for p in params:
        test =   filename[p].iloc[-6:]
        model = joblib.load(f'final_{city}_{p}.joblib')
        model.update(test)
    
city = 'boulder'                             ######
update_model(city.lower())