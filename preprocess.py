import pandas as pd

def preprocess_data(filename):
    data = pd.read_csv(filename)
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    print(data.columns)
    for column in data.columns:
        for ind in range(0,len(data[column])):
            if data[column][ind] == 'T' or data[column][ind]=="M":
                if column in ['PREC','SNF']:
                    print("got")
                    data[column] = data[column].replace("T", 0.0)
                    data[column] = data[column].replace("M", 0)
                if column =='MAXTEMP':
                    t = int(data['TEMP'][ind]) * 2 / int(data['MINTEMP'][ind])
                    data[column][ind] = t
                    print(data[column][ind], t)
                if column =='MINTEMP':
                    data[column][ind] = int(data['TEMP'][ind]) * 2 / int(data['MAXTEMP'][ind])

    data.drop(columns=['TEMP'], inplace=True)
    # cn= data.columns[0]
    # data.drop(columns=[cn], inplace=True)
    data.to_csv(f'final_{filename}')

city = 'coloradosprings'
preprocess_data(f'{city}_merged_weather_data.csv')
