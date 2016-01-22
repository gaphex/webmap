# -*- coding: utf-8 -*-
import urllib2
from urllib import urlencode
from bs4 import BeautifulSoup
import json
import os

def geocode_yandex(name):
	url ='https://geocode-maps.yandex.ru/1.x/?' + \
							urlencode({'format': 'json', \
                                       'kind': 'house', \
                                       'geocode': 'Москва, '+name.encode('utf8')})
	jsonresp = urllib2.urlopen(url).read()
	resp = json.loads(jsonresp)
	longlat = resp[u'response'][u'GeoObjectCollection'][u'featureMember'][0][u'GeoObject'][u'Point'][u'pos']
	return longlat

banks_fname = 'banks.json'
loc_fname = 'loc.json'
rbc_url ='http://quote.rbc.ru/cgi-bin/front/content/cash_currency_rates/?sortf=DT_LAST_PUBLICATE&sortd=DESC&city=1&currency=3&summa=1&period=60&pagerLimiter=500&pageNumber=1'

page = urllib2.urlopen(rbc_url).read()
soup = BeautifulSoup(page)
table = soup.find("tbody", { "id" : "tableBody" })
banks = []
loc = {}
if os.path.isfile(loc_fname):
	with open(loc_fname, 'rb') as f:
		loc = json.loads(f.read())

for i in table.find_all('tr'):
	address = i.find('span', {'id': 'address'}).getText()
	if address not in loc:
		loc[address] = geocode_yandex(address)
	long, lat = loc[address].split(' ')
	pok, prod = i.find('td', {'class': 'pok'}).getText(), i.find('td', {'class': 'prod'}).getText()
	if pok == u'' or prod == u'':
		continue
	banks.append({
			'title': i['title'],
			'pok': pok,
			'prod': prod,
			'address': address,
			'tel': i.find('span', {'id': 'tel'}).getText(),
			'metro': i.find('span', {'id': 'metro'}).getText(),
			'time': i.find('td', {'class': 'time'}).getText(),
			'long': long,
			'lat': lat
		})
crs = [float(x['prod'].replace(',','.')) for x in banks]
min_crs = min(crs)
max_crs = max(crs)
for bank in banks:
	bank['color'] = '#%02x%02x%02x' % (255, int(255*((max_crs - float(bank['prod'])) / (max_crs - min_crs))), 64)
with open(banks_fname, 'wb') as outfile:
	json.dump(banks, outfile)
with open(loc_fname, 'wb') as outfile:
	json.dump(loc, outfile)