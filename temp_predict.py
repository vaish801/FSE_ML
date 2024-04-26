import pandas as pd
from pmdarima import auto_arima

def temp_predict(filename):
    finall = pd.read_csv(filename, usecols=['DATE','TEMP'])
    finall['DATE'] = pd.to_datetime(finall['DATE'])
    finall.set_index('DATE', inplace=True)
    train = finall.iloc[:-10]
    test = finall.iloc[-10:]
    # train_y=finall.iloc[:-6,-1]
    # test_y=finall.iloc[-6:,-1]
    # train_x=finall.iloc[:-6,1:-1]
    # test_x=finall.iloc[-6:,1:-1]
    # print(train_x,train_y)
    model=auto_arima(train,seasonal = True,m = 12,trace= True)
    model.fit(train)
    forecast = model.predict(n_periods=10)
    # forecast_index = pd.date_range(start=finall.index[-1], periods=10 + 1, freq='D')
    # forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=['Forecast'])
    print(forecast)

temp_predict('final_denver_merged_weather_data.csv')
