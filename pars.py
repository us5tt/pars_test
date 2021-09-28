# Скрапінг сайта: https://auto.ria.com/
# Шукає нові авто по марках: https://auto.ria.com/uk/newauto/
# Наприклад: https://auto.ria.com/uk/newauto/marka-mercedes-benz/
# Після пошуку зберігає у файл parsResult.csv


import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import sqlite3

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
	'accept': '*/*'
	}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r


def get_pages_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('span', class_='mhide')
	if pagination:
		return int(pagination[-1].get_text())
	else:
		return 1


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('a', class_='proposition_link')
	#    print(items)
	
	cars = []
	for item in items:
		cars.append(
			{
				'title': item.find('span', class_='link').get_text(strip=True),
				'usd_price': item.find('span', class_='size22').get_text(),
				'city': item.find('span', class_='item region').get_text(),
				#'link': item.find('section', class_='proposition').find('a', class_='proposition_link').get('href'),
				}
			)
	
	return cars


def save_file(items, path):
	with open(path, 'w', encoding='utf8', newline='') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow(['Марка', 'Ціна в $', 'Місто'])
		for item in items:
			writer.writerow([item['title'], item['usd_price'], item['city']])


def parse():
	URL = input('Введіть URL: ')
	URL = URL.strip()
	html = get_html(URL)
	if html.status_code == 200:
		cars = []
	 
		pages_count = get_pages_count(html.text)
		for page in range(1, pages_count + 1):
			print(f'Скрапінг сторінки {page} а всього {pages_count}...')
			html = get_html(URL, params={'page': page})
			cars.extend(get_content(html.text))
			#print(html.text)
			FILE = 'parseResult' + '.csv'
			save_file(cars, FILE)
		
		print(f'Найдено {len(cars)} машин')
		
 		print(cars)
		
#		conn = sqlite3.connect('parsdb.db')
#		cursor = conn.cursor()
		
#		cursor.executemany('INSERT INTO parsetitems(title, usb_price, city, description) VALUES (?, ?, ?, ?)', cars)
#		conn.commit()
#		conn.close()
		
	else:
		print('Error')


parse()
