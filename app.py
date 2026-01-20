import requests


api_key= 'c1e17822e800e0bf45c4560fc10fb2b2'

user_input=input("Enter city: ")

weather_data = requests.get(
    f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")

if weather_data.json()['cod']=='404':
    print('No City Found ')

else:
    weather = weather_data.json() ['weather'] [0] ['main']
    temp= round(weather_data.json()['main'] ['temp'])

    print(f"The Weather in {user_input} is: {weather}")
    print(f"The Temperature in {user_input} is:{temp}°F")

