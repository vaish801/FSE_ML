from pmdarima import auto_arima
import pandas as pd 
import joblib
import copy


def train_model(city):
    # filen = city.lower()
    # filename = f"final_{filen}_merged_weather_data.csv"
    df = pd.read_csv(f'final_{city}_merged_weather_data.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.set_index('DATE', inplace=True)
    cols = df.columns
    print(cols)
    for col in cols:
        if (col!='SNF' and col!='DATE'):
            print('oh')
            train = df[[col]]
            test = train.iloc[-6:]
            train = train.iloc[:-6]
            model=auto_arima(train,seasonal = True, trace= True)
            model.fit(train)
            forecast = model.predict(n_periods=len(test), X=test)
            print(col,'\n',forecast)
            model.update(test)
        else:
            X = copy.deepcopy(list(cols))
            X.remove('SNF')
            X = df[X]
            Y = df[col]
            train_y=Y.iloc[:-6]
            test_y=Y.iloc[-6:]
            train_x=X.iloc[:-6,:]
            test_x=X.iloc[-6:,:]
            # print(train_x,train_y)
            model=auto_arima(y=train_y,X=train_x,seasonal = True, trace= True)
            model.fit(train_y)
            forecast = model.predict(n_periods=len(test_y), X=test_x)
            print(forecast)
            model.update(test)
        joblib.dump(model, f'final_{city}_{col}.joblib')

city = "fortcollins"
city = city.lower()
# filename = f"final_{city}_merged_weather_data.csv"
# parameters = ["DEWP","VISIB","WDSP","MAXTEMP","MINTEMP","PREC","SNF"]
# for p in parameters:
train_model(city)

# train_model(filename, "SNF")