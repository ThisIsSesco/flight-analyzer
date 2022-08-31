import requests
from bs4 import BeautifulSoup
import time
from random import randint
import pandas as pd
from datetime import datetime

dates = []
cities = []
for x in range(2):
   date_entry = input('Enter a date (do it in YYYY-MM-DD format please)')
   year, month, day = map(int, date_entry.split('-'))
   dates.append(str(datetime(year, month, day)))


city_dep = input("Enter the three letter code for the city you're leaving (e.g. Toronto = YTO)")
cities.append(city_dep)
city_arr = input("Enter the three letter code for the city you're arriving in (e.g. Miami = MIA)")
cities.append(city_arr)

rand_time = randint(5, 10)
ua_string = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
url = 'https://www.kayak.com/flights/' + city_dep + '-' + city_arr + '/' + dates[0] + '/' + dates[1] + '?sort=bestflight_a'
# https://www.kayak.com/flights/YTO-MIA/2022-09-24/2022-10-01?sort=bestflight_a
response = requests.get(url, headers=ua_string)
time.sleep(randint(5, 10))
html = response.text
soup = BeautifulSoup(html, features='lxml')
time.sleep(randint(5, 10))
flights = soup.find_all('div', {'class': 'Base-Results-HorizonResult Flights-Results-FlightResultItem phoenix-rising '
                                        'get-in-formation extra-vertical-spacing hover-actions get-in-formation '
                                        'sleek rp-contrast'})
flight_info = []
for i in flights:
   time.sleep(randint(3, 5))
   p = int(i.find('span', class_='price-text').text.replace('$', '').replace(',', '').strip())
   air = i.find('div', {'class': 'bottom'}).text
   dep_time = []
   arr_time = []
   flight_meridiem = []
   airline = []
   stops = []
   for j in i.find_all('span', {'class': 'depart-time base-time'}, limit=2):
       dep_time.append(j.text.strip())
   for k in i.find_all('span', {'class': 'arrival-time base-time'}, limit=2):
       arr_time.append(k.text.strip())
   for m in i.find_all('span', {'class': 'time-meridiem meridiem'}, limit=4):
       flight_meridiem.append(m.text.strip())
   for n in i.find_all('div', {'class': 'bottom'}, limit=2):
       airline.append(n.text.strip())
   for o in i.find_all('span', {'class': 'stops-text'}):
       if o.text.strip() != 'nonstop':
           temp = o.text
           temp += i.find_next('span', {'class': 'js-layover'}).text
           stops.append(temp.strip())
       else:
           stops.append(o.text.strip())
   _dep = (dep_time[0] + flight_meridiem[0] + '-' + arr_time[0] + flight_meridiem[1]).strip()
   _arr = (dep_time[1] + flight_meridiem[2] + '-' + arr_time[1] + flight_meridiem[3]).strip()
   print(p)
   print(_dep)
   print(_arr)
   print(air)
   fly = {
       'Price': p,
       'Departure Flight': _dep,
       'Departure Stops': stops[0],
       'Return Flight': _arr,
       'Return Stops': stops[1],
       'Airline':  air
   }
   flight_info.append(fly)
   # test

df = pd.DataFrame(flight_info)
df.to_excel('flight_data.xlsx', index=False)
print('done')

