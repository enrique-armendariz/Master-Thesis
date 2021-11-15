# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import sys
import urllib.request
import time
import csv
from bs4 import BeautifulSoup
import string
import decimal
from datetime import datetime

class CrawlingBlockApi(object):
	"""docstring for CrawlingBlockApi"""
	def __init__(self, address, pages, filename):
		self.address = address
		self.pages = pages
		self.filename = filename

	def get_blockinfo(self):
		f = open(self.filename, 'w', newline= '', encoding='utf-8')
		wr = csv.writer(f)
		wr.writerow(['tx', 'block', 'time', 'input_BTC', 'output_BTC', 'inputs', 'outputs'])
		self.address = self.address +'?&offset' + '=' #입금주소
		for i in range(0, self.pages + 1):
			url = 'https://blockchain.info/rawaddr/'
			offset = i * 50
			url = url + self.address + str(offset)
			print(url)
			req = urllib.request.urlopen(url)
			res = req.read().decode()
			data = json.loads(res)
			txs = data["txs"]
			for j in txs:
				inputs = j["inputs"]
				out = j["out"]
				t_hash = j["hash"]
				t_time = datetime.utcfromtimestamp(int(j["time"])).strftime('%Y-%m-%d %H:%M:%S')
				block = j["block_height"]
				input_addr = []
				input_price = []
				output_addr = []
				output_price = []
				total_inputs = 0
				total_outputs = 0
				input_text = ''
				output_text = ''
				'''
				if len(inputs) > 1:
					continue
				'''
				for k in range(len(inputs)):
					#print(inputs[k]["prev_out"]["addr"])
					print(inputs[k]["prev_out"]["value"])
					try:
						input_addr.append(inputs[k]["prev_out"]["addr"])
					except:
						input_addr.append(' ')
					input_price.append(inputs[k]["prev_out"]["value"])
					total_inputs = total_inputs + int(inputs[k]["prev_out"]["value"])
				#print(total_inputs)
				for t in range(len(out)):
					#print(out[t]["addr"])
					try:
						output_addr.append(out[t]["addr"])
					except:
						output_addr.append(' ')
					output_price.append(out[t]["value"])
					total_outputs = total_outputs + int(out[t]["value"])
				total_inputs = round(decimal.Decimal(total_inputs) * decimal.Decimal(0.00000001), 8)
				total_outputs = round(decimal.Decimal(total_outputs) * decimal.Decimal(0.00000001), 8)

				for in_t in range(len(input_addr)):
					input_price[in_t] = round(decimal.Decimal(input_price[in_t]) * decimal.Decimal(0.00000001), 8)
					input_text = input_text + '{address: "' + input_addr[in_t] + '", BTC: "' + str(input_price[in_t]) +' BTC"}'
					if in_t != len(input_addr) - 1:
						input_text = input_text + ', '
				for out_t in range(len(output_addr)):
					output_price[out_t] = round(decimal.Decimal(output_price[out_t]) * decimal.Decimal(0.00000001), 8)
					output_text = output_text +  '{address: "' + output_addr[out_t] + '", BTC: "' + str(output_price[out_t]) +' BTC"}'
					if out_t != len(output_addr) - 1:
						output_text = output_text + ', '
				print(input_text)
				wr.writerow([t_hash, block, t_time, total_inputs, total_outputs, '[' + input_text + ']', '[' + output_text + ']'])
			time.sleep(15)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	address = input('Enter Address: ')
	page = int(input('Enter Pages: '))
	filename = input('Enter the .csv file name: ')
	a = CrawlingBlockApi(address, page, filename)
	a.get_blockinfo()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
