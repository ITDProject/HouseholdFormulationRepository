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
	print('IDSO Agent is Started', flush = True)
	
	# Read and assign initial values from agentInitialVal
	# Controller information
	controller['name'] = agentInitialVal['controller_information']['name']
	return 0

def initialize():
	global market, controller
	global filename, tmax, deltaT, NDsystems, Case
	global RefLoad
	global ts, timeSim, PL, TPLR, PriceCap, FlatRetailPrice, RetailPrice, kWpW, RDigit
	global NHour, min_len, hour_len, day_len, IML, day, hour, minute, prev_minute, prev_hour, prev_day
	global RealPower, json_data, WPDAM, Dsystem, distribution_load, hvac_load, controllerData, house_names
	global fncs_publish
	global PiPositive, PPositive, PiNegative, PNegative
	
	if len(sys.argv) == 33:
		filename = sys.argv[1]
		tmax = int(sys.argv[2])
		deltaT = int(sys.argv[3]) # simulation time interval in seconds, which usually the same as controller period
		NDsystems = int(sys.argv[4])
		Case = int(sys.argv[5])
		FRP = int(sys.argv[6])
		PL = int(sys.argv[7])
		TPLR = int(sys.argv[8])
		RefLoad = [0] * 24
		for i in range(9,33):
			RefLoad[i-9] = float(sys.argv[i])
		#print('RefLoad:', RefLoad)
	elif len(sys.argv) == 1:
		tmax = 2 * 24 * 3600
		deltaT = 300
		NDsystems = 2
		Case = 0
		FRP = 12
		PL = 5000
		TPLR = 500
		RefLoad = [4000] * 24
	else:
		print ('usage: python fncsPYPOWER.py [rootname StartTime tmax dt]')
		sys.exit()
	
	market = {'name': 'none', 'market_id': 1}
	controller = {'name': []}

	lp = open(filename).read()
	DSODict = json.loads(lp)
	initDSO(DSODict)

	#RefLoad = [1486.64, 1215.20, 1130.72, 1072.58, 1050.30, 1104.61, 1352.59, 2433.20, 2787.30, 2930.15, 3035.10, 
	#3044.68, 3209.91, 3158.23, 3400.21, 3371.56, 3228.67, 3223.73, 3338.49, 3070.58, 3091.66, 2702.38, 2629.82, 1861.52] 
	
	PiPositive = []
	PiNegative = []	
	PPositive = []
	PNegative = []
	
	ts = 0
	timeSim = 0
	
	PriceCap = 1000

	FlatRetailPrice = FRP		# cents/kWh
	RetailPrice = [FlatRetailPrice, 0]

	kWpW = 1000
	RDigit = 3

	NHour = 24
	min_len = 60 # in s
	hour_len = 3600 #100 # in s
	day_len = NHour* hour_len # in s

	IML = 5 # Minute length of Interval

	day = 0
	hour = 0
	minute = 0 
	prev_minute = 0
	prev_hour = 0
	prev_day = 0

	RealPower = {}
	json_data = {}
	json_data['RETPrice1'] = []
	json_data['RETPrice2'] = []
	json_data['dload'] = []

	WPDAM = [0.0 for i in range(24)]

	Dsystem = ['gridlabdSimulator'+str(k+1) for k in range(NDsystems)]
	distribution_load = dict((k, {0.0}) for k in Dsystem)
	hvac_load = dict((k, dict( (controller['name'][i].split('_thermostat_controller')[0], {'hvac_load_kW' : 0.0}) for i in range(len(controller['name'])) ) ) for k in Dsystem)
	controllerData = dict( (controller['name'][i].split('_thermostat_controller')[0], {'PiStar' : 0.0}) for i in range(len(controller['name'])) )
		
	house_names = []
	for i in range(len(controller['name'])):
		S = controller['name'][i].split('_thermostat_controller')
		house_names.append(S[0])

	for k in Dsystem:
		distribution_load[k] = 0

	# Generate agent publication dictionary
	fncs_publish = {'DSO': { market['name']: dict( (i, { 'retail_price': 0.0 }) for i in house_names)}}
	return 0

def subscribeValHVACOld(fncs_sub_value_String, FlatRetailPrice):
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
	
def subscribeValHVAC(fncs_sub_value_String, FlatRetailPrice):
	# Assign values to buyers
	P = []
	Pi = []
	PiPositive = []
	PiNegative = []
	PPositive = []
	PNegative = []
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
				
				# print('S, PiStar, P_ON, state:', S, PiStar, P_ON, state,flush=True)
				
				controllerData[S[0]]['PiStar'] = PiStar
				
				if 	PiStar >=0: 
					PiPositive.append(PiStar)
					PPositive.append(P_ON)
					Pi.append(PiStar)
					P.append(P_ON)
					if fncs_sub_value_String['controller'][controllerKeys[i]]['state'] == 'MayRunON':
						if PiStar >= FlatRetailPrice:
							FlatRateON = FlatRateON + P_ON
					elif fncs_sub_value_String['controller'][controllerKeys[i]]['state'] == 'MayRunOFF':
						if PiStar > FlatRetailPrice:
							FlatRateON = FlatRateON + P_ON
				else:	
					PiNegative.append(PiStar)
					PNegative.append(P_ON)
					Pi.append(PiStar)
					P.append(P_ON)
					
	if len(PiNegative) > 0:
			print('printing PiNegative list:', PiNegative, flush = True)
			print('printing PNegative list:', PNegative, flush = True)
	if len(PiPositive) > 0:
			print('printing PiPositive list:', PiPositive, flush = True)
			print('printing PPositive list:', PPositive, flush = True)
			
	return P, Pi, PNegative, PiNegative, PPositive, PiPositive, FlatRateON

def CalculateRetailPricePR(MaxON, P, Pi):
	CPVector = [0, 0]
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
	
	if CP>=0:
		CPVector[0] = CP	
	print('Retail price is set to:', CPVector[0], CPVector[1], flush = True)
	return CPVector


def CalculateRetailPriceLF(MaxON, P, Pi, PNegative, PiNegative, PPositive, PiPositive):
	CP = 0
	CPVector = [0, 0]
	LoadMet = 0
	P_sorted = []
	Pi_sorted = []
	PPositive_sorted = []
	PiPositive_sorted = []
	PNegative_sorted = []
	PiNegative_sorted = []
	
	if len(PiPositive) > 0:
		print('len(PiPositive) > 0')
		indexlist = []
		sortedlist = sorted(enumerate(PiPositive), key = lambda x: x[1])
		sortedlist_reverse = sorted(sortedlist, key = lambda x: x[1], reverse = True)
		
		#print('printing sorted list:', sortedlist, flush = True)
		#print('printing sorted_reverse list:', sortedlist_reverse, flush = True)
		
		for i in sortedlist_reverse:
			indexlist.append(i[0])
			PiPositive_sorted.append(i[1])
		
		for i in range(len(indexlist)):
			PPositive_sorted.append(PPositive[indexlist[i]])
			
		#print('printing index list:', indexlist, flush = True)
		if len(PiPositive_sorted) > 0:
			print('printing Pi_sorted list:', PiPositive_sorted, flush = True)
			print('printing P_sorted list:', PPositive_sorted, flush = True)
		
		P_sorted.extend(PPositive_sorted)
		Pi_sorted.extend(PiPositive_sorted)
	
	if len(PiNegative) > 0:
		indexlist = []
		sortedlist = sorted(enumerate(PiNegative), key = lambda x: x[1])
		sortedlist_reverse = sorted(sortedlist, key = lambda x: x[1], reverse = True)
		#print('printing sorted list:', sortedlist, flush = True)
		#print('printing sorted_reverse list:', sortedlist_reverse, flush = True)
		for i in sortedlist_reverse:
			indexlist.append(i[0])
			PiNegative_sorted.append(i[1])
			
		for i in range(len(indexlist)):
			PNegative_sorted.append(PNegative[indexlist[i]])
			
		#print('printing index list:', indexlist, flush = True)
		if len(PiNegative_sorted) > 0:
			print('printing Pi_sorted list:', PiNegative_sorted, flush = True)
			print('printing P_sorted list:', PNegative_sorted, flush = True)
			
		P_sorted.extend(PNegative_sorted)
		Pi_sorted.extend(PiNegative_sorted)

	print('printing P_sorted list:', P_sorted, flush = True)
	print('printing Pi_sorted list:', Pi_sorted, flush = True)
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
			if CP >= 0:
				CPVector[0] = CP
				CPVector[1] = 0
			else:
				if len(PiPositive_sorted) == 0:
					CPVector[0] = 0
				elif len(PiPositive_sorted) == 1:
					CPVector[0] = round(PiPositive_sorted[0],2)
				else:
					CPVector[0] = round(PiPositive_sorted[len(PiPositive_sorted)-1],2)
				CPVector[1] = CP
			print('Retail price is set to:', CPVector[0], CPVector[1], flush = True)
			return CPVector
	CP = round(CP,2)
	if CP >= 0:
		CPVector[0] = CP
		CPVector[1] = 0
	else:
		if len(PiPositive_sorted) == 0:
			CPVector[0] = 0
		elif len(PiPositive_sorted) == 1:
			CPVector[0] = round(PiPositive_sorted[0],2)
		else:
			CPVector[0] = round(PiPositive_sorted[len(PiPositive_sorted)-1],2)
		CPVector[1] = CP
	print('Retail price is set to:', CPVector[0], CPVector[1], flush = True)
	return CPVector

def publish_Price(value):
	for i in house_names:
		if controllerData[i]['PiStar'] >= 0:
			fncs_publish['DSO'][market['name']][i]['retail_price'] = value[0]
		else:
			fncs_publish['DSO'][market['name']][i]['retail_price'] = value[1]
	fncs_publishString = json.dumps(fncs_publish)
	print('fncs_publishString:',fncs_publishString)
	fncs.agentPublish(fncs_publishString)
	return 0

# extract float from string
def get_number(value):
	return float(''.join(ele for ele in value if ele.isdigit() or ele == '.'))


initialize()
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
				#print('S:',S)
				hvac_load[S[1]][S[2]]['hvac_load_kW']= float(valuesplit[0]) # in kW

			if title.startswith('distribution_load'):
				S = title.split('#')
				valuesplit = value.split(' ')
				z = complex(valuesplit[0].replace('i','j')) # in VA
				distribution_load[S[1]] = z.real # in W
				print('ts: ', ts, 'DL: ', distribution_load[S[1]], flush = True)

			if title.startswith('WPDAM'):
				print('printing WPDAM value vector ', value, flush = True)
				WPDAM_temp = value.split(',')
				for i in range(NHour):
					WPDAM[i] = get_number(WPDAM_temp[i])
				print('ts_dam: ',ts, 'printing WPDAM: ', WPDAM, flush = True)

			if title.startswith('WPRTM'):
				WPRTM = get_number(value)
				print('ts_rtm: ',ts, 'printing WPRTM: ', WPRTM, flush = True)


		#computing TotalNonHVACLoad
		if ts>0:
			SumHvacLoad = 0
			sumDLoad = 0
			for k in Dsystem:
				sumDLoad = sumDLoad + distribution_load[k]/kWpW # converting into kW from W
				for i in range(len(house_names)):
					SumHvacLoad = SumHvacLoad + hvac_load[k][house_names[i]]['hvac_load_kW']
			TotalNonHVACLoad = round(sumDLoad - SumHvacLoad,RDigit) # (kW - kW) -> TotalNonHVACLoad in kW
			print('ts:', ts, 'SumHvacLoad:', SumHvacLoad, 'sumDLoad:', sumDLoad, 'TotalNonHVACLoad:', TotalNonHVACLoad, flush = True)

		fncs_sub_value_unicode = (fncs.agentGetEvents()).decode()
		if fncs_sub_value_unicode != '':
			fncs_sub_value_String = json.loads(fncs_sub_value_unicode)
			print('fncs_sub_value_String:', fncs_sub_value_String) 
			if "controller" in fncs_sub_value_String:
				P, Pi, PNegative, PiNegative, PPositive, PiPositive, FlatRateON = subscribeValHVAC(fncs_sub_value_String, FlatRetailPrice)
				
				if day < 1:
					RetailPrice[0] = FlatRetailPrice
					RetailPrice[1] = FlatRetailPrice
				
				else:
					if Case == 1: 
						#--------  Peak Reduction Logic --------# 
						if (PL - TPLR - TotalNonHVACLoad - FlatRateON) >= 0 : 
							RetailPrice[0] = FlatRetailPrice
							RetailPrice[1] = FlatRetailPrice
						else: 
							MaxON = PL - TPLR - TotalNonHVACLoad
							print('ts:', ts, 'MaxON: ', MaxON)
							RetailPrice = CalculateRetailPricePR(MaxON, P, Pi)
							if RetailPrice[0] >= PriceCap:
								RetailPrice[0] = PriceCap
					elif Case == 2:
					#-------- Load Following Logic  ----------#
						MaxON = round(RefLoad[hour] - TotalNonHVACLoad,2)
						print('ts:', ts, 'MaxON: ', MaxON)
						RetailPrice = CalculateRetailPriceLF(MaxON, P, Pi, PNegative, PiNegative, PPositive, PiPositive)
					
					elif Case == 0:
						# Flat Retail Price
						RetailPrice[0] = FlatRetailPrice
						RetailPrice[1] = FlatRetailPrice
				
				print('ts:', ts, 'publishing RET price: ', RetailPrice[0], RetailPrice[1])
				publish_Price(RetailPrice)

		# dumping json data 
		if prev_day != day and day >= 1:
			print('plotdata ts: ', ts)
			outfile = open('plotfiles/plotdata' + '_D' + str(day-1) + '.json', 'w') 
			json.dump(json_data, outfile)
			outfile.close()
			json_data = {}
			json_data['dload'] = []
			json_data['RETPrice1'] = []
			json_data['RETPrice2'] = []

		# storing data in json format
		if ts>= deltaT: 
			if ts % deltaT ==0:
				json_data['dload'].append(round(sumDLoad,RDigit))
				json_data['RETPrice1'].append(round(RetailPrice[0],RDigit))
				json_data['RETPrice2'].append(round(RetailPrice[1],RDigit))

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

