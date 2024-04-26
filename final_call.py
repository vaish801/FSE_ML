import updateData
import parameters_prediction
import re

city = 'Denver'
end_date = '28-04-2024'
clean_city = re.sub(r'[^a-zA-Z]', '', city)
updateData.update_data(clean_city.lower())
results = parameters_prediction.predict_parameters(clean_city.lower(), end_date)
print(results)