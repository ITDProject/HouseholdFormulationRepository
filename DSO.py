#	Copyright (C) 2017 Battelle Memorial Institute
import json
import sys
import warnings
import csv
import fncs
import math
import cmath
import re

def initDSO(DSODict):
	agentRegistration = DSODict['registration']
	agentInitialVal = DSODict['initial_values']
	market['name'] = agentRegistration['agentName']
	print('Market:', market['name'], flush = True)
	
	# Read and assign initial values from agentInitialVal
	# Controller information
	controller['name'] = agentInitialVal['controller_information']['name']
	
	return 0


def subscribeValHVAC(fncs_sub_value_String, FlatRetailPrice):
	# Assign values to buyers
	P = []
	Pi = []
	FlatRateON = 0
	controllerKeys = list (fncs_sub_value_String['controller'].keys())
	#print('checking controllerKeys length', len(controllerKeys), flush = True)
	for i in range(len(controllerKeys)):
		for j in range(len(controller['name'])):
			if controller['name'][j] == controllerKeys[i]:
				S = controller['name'][j].split('_thermostat_controller')
				P_ON = fncs_sub_value_String['controller'][controllerKeys[i]]['P_ON']
				PiStar = fncs_sub_value_String['controller'][controllerKeys[i]]['pistar']
				state = fncs_sub_value_String['controller'][controllerKeys[i]]['state']
				#print('PiStar, P_ON, state:', PiStar, P_ON, state,flush=True)
				Pi.append(PiStar)
				P.append(P_ON)
				if fncs_sub_value_String['controller'][controllerKeys[i]]['state'] == 'MayRunON':
					if PiStar >= FlatRetailPrice:
						FlatRateON = FlatRateON + P_ON
				elif fncs_sub_value_String['controller'][controllerKeys[i]]['state'] == 'MayRunOFF':
					if PiStar > FlatRetailPrice:
						FlatRateON = FlatRateON + P_ON
	return P, Pi, FlatRateON

def CalculateRetailPricePR(MaxON, P, Pi):
	#print('printing Pi list:', Pi, flush = True)
	LoadMet = 0
	#[Pi_sorted, indexlist] = sort_prices(Pi)
	P_sorted = []
	Pi_sorted = []
	indexlist = []
	sortedlist = sorted(enumerate(Pi), key = lambda x: x[1])
	sortedlist_reverse = sorted(sortedlist, key = lambda x: x[1], reverse = True)
	#print('printing sorted list:', sortedlist, flush = True)
	#print('printing sorted_reverse list:', sortedlist_reverse, flush = True)
	for i in sortedlist_reverse:
		indexlist.append(i[0])
		Pi_sorted.append(i[1])
	if len(Pi_sorted) > 0:
		print('printing Pi_sorted list:', Pi_sorted, flush = True)
	for i in range(len(indexlist)):
		P_sorted.append(P[indexlist[i]])
	#print('printing P_sorted list:', P_sorted, flush = True)
	for i in range(len(P_sorted)):
		LoadMet = LoadMet + P_sorted[i]
		#print('LoadMet:', LoadMet, 'P_sorted[i]:', P_sorted[i], flush = True)
		CP = Pi_sorted[i]
		if LoadMet > MaxON:
			if i ==0:
				CP = Pi_sorted[0] + 0.1
				print('Retail price is set to:', CP, flush = True)
				return CP
			CP = Pi_sorted[i-1]
			print('Retail price is set to:', CP, flush = True)
			return CP
	print('Retail price is set to:', CP, flush = True)
	return CP


def CalculateRetailPriceLF(MaxON, P, Pi):
	LoadMet = 0
	P_sorted = []
	Pi_sorted = []
	indexlist = []
	sortedlist = sorted(enumerate(Pi), key = lambda x: x[1])
	sortedlist_reverse = sorted(sortedlist, key = lambda x: x[1], reverse = True)
	#print('printing sorted list:', sortedlist, flush = True)
	#print('printing sorted_reverse list:', sortedlist_reverse, flush = True)
	for i in sortedlist_reverse:
		indexlist.append(i[0])
		Pi_sorted.append(i[1])
	#print('printing index list:', indexlist, flush = True)
	if len(Pi_sorted) > 0:
		print('printing Pi_sorted list:', Pi_sorted, flush = True)
	for i in range(len(indexlist)):
		P_sorted.append(P[indexlist[i]])
	#print('printing P_sorted list:', P_sorted, flush = True)
	for i in range(len(P_sorted)):
		diff1 = round(abs(LoadMet - MaxON),2)
		LoadMet = LoadMet + P_sorted[i]
		diff2 = round(abs(LoadMet - MaxON),2)
		#print('diff1,diff2',diff1,diff2,flush=True)
		#print('LoadMet:', LoadMet, 'P_sorted[i]:', P_sorted[i], flush = True)
		CP = Pi_sorted[i]
		if LoadMet >= MaxON:
			if diff1 < diff2:
				if i ==0:
					CP = Pi_sorted[0] + 0.1
				else:
					CP = Pi_sorted[i-1] # Pi_sorted[i-1]
			else:
				CP = Pi_sorted[i]
			print('Retail price is set to:', CP, flush = True)
			CP = round(CP,2)
			return CP
	CP = round(CP - 0.1,2)
	print('Retail price is set to:', CP, flush = True)
	return CP

#def publish_publications(value, mode, index):
def publish_Price(value):
	fncs_publish['DSO'][market['name']]['retail_price'] = value
	fncs_publishString = json.dumps(fncs_publish)
	fncs.agentPublish(fncs_publishString)
	return 0

if len(sys.argv) == 5:
	filename = sys.argv[1]
	tmax = int(sys.argv[2])
	deltaT = int(sys.argv[3]) # simulation time interval in seconds(minutes), which usually the same as controller period
	NDsystems = int(sys.argv[4])
elif len(sys.argv) == 1:
	tmax = 2 * 24 * 3600
	deltaT = 300
	NDsystems = 2
else:
	print ('usage: python fncsPYPOWER.py [rootname StartTime tmax dt]')
	sys.exit()


market = {'name': 'none', 'market_id': 1}
controller = {'name': []}

lp = open(filename).read()
DSODict = json.loads(lp)
initDSO(DSODict)

PeakObserved = 4195 # MW
PeakReduction = 400	 # MW
PriceCap = 1000

FlatRetailPrice = 10		# cents/kWh
RetailPrice = FlatRetailPrice

kWpW = 1000
RDigit = 3

NHour = 24
min_len = 60 # in s
hour_len = 3600 #100 # in s
day_len = NHour* hour_len # in s

IML = 5 # Minute length of Interval
timeSim = 0
ts = 0

day = 0
hour = 0
minute = 0 
prev_minute = 0
prev_hour = 0
prev_day = 0

RealPower = {}
json_data = {}
json_data['RETPrice'] = []
json_data['dload'] = []
#json_data['hvac_load'] = []

RefLoad = [1899.29,
1792.03,
1566.57,
1696.24,
1606.87,
1517.90,
1823.37,
2484.20,
2762.14,
3170.54,
3247.16,
3366.41,
3625.23,
3623.31,
3725.34,
3661.67,
3398.37,
2738.75,
2457.10,
2325.78,
2450.20,
2622.42,
2327.48,
1901.81
] # Mix


Dsystem = ['gridlabdSimulator'+str(k+1) for k in range(NDsystems)]
hvac_load = dict((k, dict( (controller['name'][i].split('_thermostat_controller')[0], {'hvac_load_kW' : 0.0}) for i in range(len(controller['name'])) ) ) for k in Dsystem)

distribution_load = dict((k, {0.0}) for k in Dsystem)

house_names = []
for i in range(len(controller['name'])):
	S = controller['name'][i].split('_thermostat_controller')
	house_names.append(S[0])

for k in Dsystem:
	distribution_load[k] = 0

# Generate agent publication dictionary
fncs_publish = {'DSO': { market['name']: { 'retail_price': {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}}}}
fncs_publish['DSO'][market['name']]['retail_price'] = 10

fncs.initialize()


with warnings.catch_warnings():
	warnings.simplefilter("ignore") 
	while ts <= tmax:
		print ('ts: ',ts, flush = True)

		day = int(ts / day_len)# - ts % 2400 # day = 24*100s $ day_len = 2400s
		hour = int((ts - (day * day_len)) / hour_len)
		minute = int((ts - (day * day_len) - hour * hour_len)/min_len)
		interval = int(minute/IML)     # IML = 5


		events = fncs.get_events()

		#Receiving messages
		for key in events:
			title = key.decode()
			value = fncs.get_value(key).decode()

			if title.startswith('hvac_load'):
				S = title.split('#')
				valuesplit = value.split(' ')
				hvac_load[S[1]][S[2]]['hvac_load_kW']= float(valuesplit[0]) #get_number(value) # in kW

			if title.startswith('distribution_load'):
				S = title.split('#')
				valuesplit = value.split(' ')
				z = complex(valuesplit[0].replace('i','j')) # in VA
				distribution_load[S[1]] = z.real # in W
				print('ts: ', ts, 'DL: ', distribution_load[S[1]], flush = True)


		#computing TotalNonHVACLoad
		if ts>0: #ts % deltaT ==0 and ts!=0:
			SumHvacLoad = 0
			sumDLoad = 0
			for k in Dsystem:
				sumDLoad = sumDLoad + distribution_load[k]/kWpW # converting into kW from W
				for i in range(len(house_names)):
					SumHvacLoad = SumHvacLoad + hvac_load[k][house_names[i]]['hvac_load_kW']
			TotalNonHVACLoad = round(sumDLoad - SumHvacLoad,RDigit) # kW - kW -> TotalNonHVACLoad in kW
			print('TotalNonHVACLoad:', TotalNonHVACLoad, flush = True)

		fncs_sub_value_unicode = (fncs.agentGetEvents()).decode()
		if fncs_sub_value_unicode != '':
			fncs_sub_value_String = json.loads(fncs_sub_value_unicode)
			if "controller" in fncs_sub_value_String:
				P, Pi, FlatRateON = subscribeValHVAC(fncs_sub_value_String, FlatRetailPrice)
				
				#--------  Peak Reduction Logic --------# 
				# if (PeakObserved - PeakReduction - TotalNonHVACLoad - FlatRateON) >= 0 : 
					# RetailPrice = FlatRetailPrice
				# else: 
					# MaxON = PeakObserved - PeakReduction - TotalNonHVACLoad
					# print('ts:', ts, 'MaxON: ', MaxON)
					# RetailPrice = CalculateRetailPricePR(MaxON, P, Pi)
					# if RetailPrice >= PriceCap:
						# RetailPrice = PriceCap
				
				#-------- Load Following Logic  ----------#
				# MaxON = round(RefLoad[hour] - TotalNonHVACLoad,2)
				# print('ts:', ts, 'MaxON: ', MaxON)
				# RetailPrice = CalculateRetailPriceLF(MaxON, P, Pi)
				
				if day < 1:
					RetailPrice = FlatRetailPrice # ts/100 # RET[day][hour*min_len+minute]
				
				# overwriting for flat pricing
				RetailPrice = FlatRetailPrice
				
				print('ts:', ts, 'publishing RET price: ', RetailPrice)
				publish_Price(RetailPrice)

		# dumping json data 
		if prev_day != day and day >= 1: # previously # day > 2
			print('plotdata ts: ', ts)
			outfile = open('plotfiles/plotdata' + '_' + str(day-1) + '.json', 'w') 
			json.dump(json_data, outfile)
			outfile.close()
			json_data = {}
			#json_data['hvac_load'] = []
			json_data['dload'] = []
			json_data['RETPrice'] = []

		# storing data in json format
		if ts>= deltaT: #day >= 1: # previously day > 1
			if ts % deltaT ==0:
				#json_data['hvac_load'].append(round(SumHvacLoad,3)) # not converting into MW
				json_data['dload'].append(round(sumDLoad,RDigit))
				json_data['RETPrice'].append(round(RetailPrice,RDigit))

		prev_minute = minute
		prev_hour = hour
		prev_day = day

		if(ts < (timeSim + deltaT)) :
			ts = fncs.time_request(timeSim + deltaT)
		else:
			timeSim = timeSim + deltaT
			ts = fncs.time_request(timeSim + deltaT)

	print ('finalizing FNCS', flush=True)
	fncs.finalize()

