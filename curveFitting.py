#!/usr/bin/env python 

import requests 
import click
import pprint
import json
import panda as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

def get_data(x): 
	return requests.get('http://165.227.157.145:8080/api/do_measurement?x={}'.format(x)).json()['data']['y'] 

def get_interval(l): 
	results = [] 
	for item in l: 
		results.append([item, get_data(item)]) 
	return results 

def removeDuplicates(data):
	data = list(k for k,_ in itertools.groupby(data))
	for d in data:
		if not d[1]:
			d[1] = np.nan
	return data
	

def interpolate(l):
	not_nan = np.logical_not(np.isnan(l))
	indices = np.arange(len(l))
	interp = interp1d(indices[not_nan], l[not_nan])
	return interp(indices)

def fit(data):
	data = removeDuplicates(data)
	x = np.array([item[0] for item in data])
	y = np.array([item[1] for item in data])
	y = interpolate(y)

	fit_params = np.polyfit(x,y,4)
	plt.plot(x,y, 'bo', label='data')
	new_y = np.polyval(fit_params, x)
	plt.plot(x, new_y, 'r-', label='fit')

	items = ['{}x^{}'.format(str(round(fit_params[i], 2)), 4-i) for i in range(5)]
	formula = 'f(x) = {}'.format(' + '.join(items))
	print formula

	plt.title('Curve fitting\n'+formula, fontsize=12)
	plt.xlabel('x')
	plt.ylabel('f(x)')
	plt.legend(('data', 'fit'))
	plt.show()

def readFromFile(file):
	data = []
	jsonData = json.loads(file.read())['data']
	for entry in jsonData:
		data.append([entry['x'], entry['y']])
	return data

@click.command()
@click.option('--num_of_points', '-n', default=500, required=False, type=int, help='Number of required points.')
@click.option('--point_distance', '-d', default=1, required=False, type=float, help='Distance between points.')
@click.option('--num_of_requests', '-r', default=5, required=False, type=int, help='Number of required measurments.')
@click.option('--input_file', '-i', type=click.File('rb'), required=False, help='Path to the json file to read (insted of requesting the server interactively).')
def main(num_of_points, point_distance, num_of_requests, input_file):
	if input_file:
		data = readFromFile(input_file)
	else:
		gen_list = [i - (num_of_points // 2) for i in range(num_of_points + 1)]
		requested_list = []
		for i in range(num_of_requests):
			requested_list += gen_list

		requested_list = [a * point_distance for a in requested_list]
		requested_list.sort()

		data = get_interval(requested_list)

	fit(data)

if __name__ == '__main__':
	main()

