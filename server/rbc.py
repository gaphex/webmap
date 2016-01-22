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
            'currency': 1,
			'prod': prod,
			'address': address,
			'tel': i.find('span', {'id': 'tel'}).getText(),
			'metro': i.find('span', {'id': 'metro'}).getText(),
			'time': i.find('td', {'class': 'time'}).getText(),
			'sum': i.find('td', {'class': 'sum'}).getText(),
			'long': long,
			'lat': lat
		})
rbc_url ='http://quote.rbc.ru/cgi-bin/front/content/cash_currency_rates/?sortf=DT_LAST_PUBLICATE&sortd=DESC&city=1&currency=2&summa=1&period=60&pagerLimiter=500&pageNumber=1'

page = urllib2.urlopen(rbc_url).read()
soup = BeautifulSoup(page)
table = soup.find("tbody", { "id" : "tableBody" })
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
            'currency': 2,
			'prod': prod,
			'address': address,
			'tel': i.find('span', {'id': 'tel'}).getText(),
			'metro': i.find('span', {'id': 'metro'}).getText(),
			'time': i.find('td', {'class': 'time'}).getText(),
			'sum': i.find('td', {'class': 'sum'}).getText(),
			'long': long,
			'lat': lat
		})
max_buy_dollar = max(float(x['pok']) for x in banks if x[u'currency'] == 1)
max_buy_euro = max(float(x['pok']) for x in banks if x[u'currency'] == 2)
min_buy_dollar = min(float(x['pok']) for x in banks if x[u'currency'] == 1)
min_buy_euro = min(float(x['pok']) for x in banks if x[u'currency'] == 2)
max_sell_dollar = max(float(x['prod']) for x in banks if x[u'currency'] == 1)
max_sell_euro = max(float(x['prod']) for x in banks if x[u'currency'] == 2)
min_sell_dollar = min(float(x['prod']) for x in banks if x[u'currency'] == 1)
min_sell_euro = min(float(x['prod']) for x in banks if x[u'currency'] == 2)
for bank in banks:
    if bank[u'currency'] == 1: # dollar
        bank['color'] = '#%02x%02x%02x' % (255, int(255*(0.2 * (max_buy_dollar - float(bank['pok'])) / (max_buy_dollar - min_buy_dollar) + 0.8 * (max_sell_dollar - float(bank['prod'])) / (max_sell_dollar - min_sell_dollar))), 64)
    else:
        bank['color'] = '#%02x%02x%02x' % (255, int(255*(0.2 * (max_buy_euro - float(bank['pok'])) / (max_buy_euro - min_buy_euro) + 0.8 * (max_sell_euro - float(bank['prod'])) / (max_sell_euro - min_sell_euro))), 64)
with open(banks_fname, 'wb') as outfile:
	json.dump(banks, outfile)
with open(loc_fname, 'wb') as outfile:
	json.dump(loc, outfile)