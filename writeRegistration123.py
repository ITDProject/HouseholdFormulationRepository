import numpy as np
def set_window_shgc(glazing_layers, glazing_treatment, window_frame):
	glazing_shgc = 0
	if (glazing_layers == 'ONE'):
		if (glazing_treatment == 'CLEAR'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.86
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.75
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.64
		elif (glazing_treatment == 'ABS'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.73
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.64
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.54
		elif (glazing_treatment == 'REFL'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.31
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.28
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.24
	elif (glazing_layers == 'TWO'):
		if (glazing_treatment == 'CLEAR'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.76
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.67
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.67
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.57
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.57
		elif (glazing_treatment == 'ABS'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.62
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.55
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.55
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.46
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.46
		elif (glazing_treatment == 'REFL'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.29
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.27
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.27
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.22
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.22
		elif (glazing_treatment == 'LOW_S'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.41
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.37
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.37
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.31
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.31
		elif (glazing_treatment == 'HIGH_S'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.70
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.62
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.52
	elif (glazing_layers == 'THREE'):
		if (glazing_treatment == 'CLEAR'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.68
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.60
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.60
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.51
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.51
		elif (glazing_treatment == 'ABS'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.34
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.31
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.31
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.26
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.26
		elif (glazing_treatment == 'REFL'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.34
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.31
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.31
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.26
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.26
		elif (glazing_treatment == 'LOW_S'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.27
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.25
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.25
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.21
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.21
		elif (glazing_treatment == 'HIGH_S'):
			if (window_frame == 'NONE'):
				glazing_shgc = 0.62
			elif (window_frame == 'ALUMINIUM'):
				glazing_shgc = 0.55
			elif (window_frame == 'THERMAL_BREAK'):
				glazing_shgc = 0.55
			elif (window_frame == 'WOOD'):
				glazing_shgc = 0.46
			elif (window_frame == 'INSULATED'):
				glazing_shgc = 0.46
	#print(glazing_shgc)
	return glazing_shgc

def set_window_Rvalue(glass_type, glazing_layers, window_frame):
	if (glass_type == 'LOW_E_GLASS'):
		if (glazing_layers == 'TWO'):
			if (window_frame == 'NONE'):
				Rg = 1.0/0.30
			elif (window_frame == 'ALUMINIUM'):
				Rg = 1.0/0.67
			elif (window_frame == 'THERMAL_BREAK'):
				Rg = 1.0/0.47
			elif (window_frame == 'WOOD'):
				Rg = 1.0/0.41
			elif (window_frame == 'INSULATED'):
				Rg = 1.0/0.33
		elif (glazing_layers == 'THREE'):
			if (window_frame == 'NONE'):
				Rg = 1.0/0.27
			elif (window_frame == 'ALUMINIUM'):
				Rg = 1.0/0.64
			elif (window_frame == 'THERMAL_BREAK'):
				Rg = 1.0/0.43
			elif (window_frame == 'WOOD'):
				Rg = 1.0/0.37
			elif (window_frame == 'INSULATED'):
				Rg = 1.0/0.31
	elif (glass_type == 'GLASS'):
		if (glazing_layers == 'ONE'):
			if (window_frame == 'NONE'):
				Rg = 1.0/1.04
			elif (window_frame == 'ALUMINIUM'):
				Rg = 1.0/1.27
			elif (window_frame == 'THERMAL_BREAK'):
				Rg = 1.0/1.08
			elif (window_frame == 'WOOD'):
				Rg = 1.0/0.90
			elif (window_frame == 'INSULATED'):
				Rg = 1.0/0.81
		if (glazing_layers == 'TWO'):
			if (window_frame == 'NONE'):
				Rg = 1.0/0.48
			elif (window_frame == 'ALUMINIUM'):
				Rg = 1.0/0.81
			elif (window_frame == 'THERMAL_BREAK'):
				Rg = 1.0/0.60
			elif (window_frame == 'WOOD'):
				Rg = 1.0/0.53
			elif (window_frame == 'INSULATED'):
				Rg = 1.0/0.44
		elif (glazing_layers == 'THREE'):
			if (window_frame == 'NONE'):
				Rg = 1.0/0.31
			elif (window_frame == 'ALUMINIUM'):
				Rg = 1.0/0.67
			elif (window_frame == 'THERMAL_BREAK'):
				Rg = 1.0/0.46
			elif (window_frame == 'WOOD'):
				Rg = 1.0/0.40
			elif (window_frame == 'INSULATED'):
				Rg = 1.0/0.34
	else:
		Rg = 2.0
	Rg = round(Rg, 8)
	#print(Rg)
	return Rg

def writeRegistration123 (filename, N):
	import json
	import re
	import os
	import shutil

	NDsystems = N
	AgentType = 'DSO'
	marketName = "1" 
	DSOMsgName = "DSO_1"
	
	folderName = "input"
	ip = open (filename + ".glm", "r")
	if not os.path.exists("input"):
		os.makedirs(folderName)
	else:
		shutil.rmtree("input") # delete the existing input folder in case there are data not needed
		os.makedirs(folderName)
	op_auction = open (folderName + "/" + AgentType + "_registration.json", "w") 
	

	# market data:
	unit = "kW"
	periodMarket = 300
	initial_price = 12

	# house data:
	air_temperature = 72 # np.random.uniform (68, 76) 
	
	# Assign empty dictionary
	controllers = {}
	auctions = {}
	 
	ip.seek(0,0)
	inFNCSmsg = False
	inHouses = False
	endedHouse = False
	isELECTRIC = False
	
	houseName = ""
	FNCSmsgName = ""
	
	# Obtain controller dictionary based on house numbers
	for line in ip:
		lst = line.split()
		if len(lst) > 1:
			if lst[1] == "house":
				inHouses = True
			# Check fncs_msg object:
			if lst[1] == "fncs_msg":
				inFNCSmsg = True
			# Check for ANY object within the house, and don't use its name:
			if inHouses == True and lst[0] == "object" and lst[1] != "house":
				endedHouse = True
#				print('  ended on', line)
			# Check FNCS_msg object name
			if inFNCSmsg == True:
				if lst[0] == "name":
					FNCSmsgName = lst[1].strip(";")
					inFNCSmsg = False
			# Check house object with controller inside
			if inHouses == True:
				if lst[0] == "name" and endedHouse == False:
					houseName = lst[1].strip(";")
				if lst[0] == "cooling_system_type":
					if (lst[1].strip(";") == "ELECTRIC"):
						isELECTRIC = True
				if lst[0] == "air_temperature":
					Ta = float(lst[1].strip(";"))
				if lst[0] == "mass_temperature":
					Tm = float(lst[1].strip(";"))
				if lst[0] == "system_mode":
					system_mode = lst[1].strip(";")
				if lst[0] == "cooling_COP":
					cooling_COP = float(lst[1].strip(";"))
				if lst[0] == "over_sizing_factor":
					OSF = float(lst[1].strip(";"))
				if lst[0] == "ceiling_height":
					h = float(lst[1].strip(";"))
				if lst[0] == "number_of_stories":
					n = int(lst[1].strip(";"))
				if lst[0] == "aspect_ratio":
					R = float(lst[1].strip(";"))
				if lst[0] == "floor_area":
					A = float(lst[1].strip(";"))
				if lst[0] == "mass_internal_gain_fraction":
					fi = float(lst[1].strip(";"))
				if lst[0] == "mass_solar_gain_fraction":
					fs = float(lst[1].strip(";"))
				if lst[0] == "glass_type":
					glass_type = lst[1].strip(";")
				if lst[0] == "glazing_layers":
					glazing_layers = lst[1].strip(";")
				if lst[0] == "airchange_per_hour":
					I = float(lst[1].strip(";"))
				if lst[0] == "Rroof":
					Rc = float(lst[1].strip(";"))
				if lst[0] == "Rdoors":
					Rd = float(lst[1].strip(";"))
				if lst[0] == "Rfloor":
					Rf = float(lst[1].strip(";"))
				if lst[0] == "Rwall":
					Rw = float(lst[1].strip(";"))
				if lst[0] == "window_frame":
					window_frame = lst[1].strip(";")
				if lst[0] == "exterior_ceiling_fraction":
					ECR = float(lst[1].strip(";"))
				if lst[0] == "exterior_floor_fraction":
					EFR = float(lst[1].strip(";"))
				if lst[0] == "exterior_wall_fraction":
					EWR = float(lst[1].strip(";"))
				if lst[0] == "glazing_treatment":
					glazing_treatment = lst[1].strip(";")
				if lst[0] == "interior_surface_heat_transfer_coeff":
					hs = float(lst[1].strip(";"))
				if lst[0] == "interior_exterior_wall_ratio":
					IWR = float(lst[1].strip(";"))
				if lst[0] == "total_thermal_mass_per_floor_area":
					mf = float(lst[1].strip(";"))
				if lst[0] == "number_of_doors":
					nd = int(lst[1].strip(";"))
				if lst[0] == "window_exterior_transmission_coefficient":
					WET = float(lst[1].strip(";"))
				if lst[0] == "window_wall_ratio":
					WWR = float(lst[1].strip(";"))
		elif len(lst) == 1:
			if inHouses == True: 
				inHouses = False
				endedHouse = False
				if isELECTRIC == True:
					controller_name = houseName + "_thermostat_controller"
					controllers[controller_name] = {}
					mu_random = 1 # change it to random function
					SHGCNom = set_window_shgc(glazing_layers, glazing_treatment, window_frame) 
					Rg = set_window_Rvalue(glass_type, glazing_layers, window_frame) 
					controllers[controller_name]['controller_information'] = {'marketName': marketName, 'houseName': houseName} 
					controllers[controller_name]['market_information'] = {'retail_price': initial_price} 
					controllers[controller_name]['house_information'] = {'Tbliss': 72, 'mu': mu_random, \
					'Ta': Ta, 'Tm': Tm, 'system_mode': system_mode, 'cooling_COP': cooling_COP,'OSF': OSF, \
					'h':h, 'n':n, 'R':R, 'A':A, 'fi':fi, 'fs':fs, 'I':I, 'Rc':Rc, 'Rd':Rd, 'Rf':Rf, 'Rw':Rw, \
					'ECR':ECR, 'EFR':EFR, 'EWR':EWR, 'hs':hs, 'IWR':IWR, 'mf':mf, 'nd':nd, 'WET':WET, 'WWR':WWR,\
					'Rg': Rg, 'SHGCNom':SHGCNom}
					isELECTRIC = False

	# Write market dictionary
	auctions[marketName] = {}
	auctions[marketName]['market_information'] = {'market_id': 1, 'period': periodMarket} 
	# obtain controller information for market:
	controllers_names = []
	controllers_Tbliss = []
	controllers_mu = []
	for key, value in controllers.items(): # Add all controllers
		controllers_names.append(key)
		controllers_Tbliss.append(controllers[key]['house_information']['Tbliss'])
		controllers_mu.append(controllers[key]['house_information']['mu'])
	auctions[marketName]['controller_information'] = {'name': controllers_names, 'pistar': [0 for i in range(len(controllers))], 'state': ["COOL" for i in range(len(controllers))], 'Tbliss': controllers_Tbliss, 'mu': controllers_mu}

	# Write file for controller registration
	for key, value in controllers.items(): # Process each controller
		controllerDict = {}
		houseName = controllers[key]['controller_information']['houseName']
		MeterName = 'triplex_meter' + houseName.split('house')[1]
		TriplexNodeName = 'triplex_node' + houseName.split('house')[1]
		singleControllerReg = {}
		singleControllerReg = {}
		singleControllerReg = {}
		singleControllerReg['agentType'] = "controller"
		singleControllerReg['agentName'] = key
		singleControllerReg['timeDelta'] = 1 
		singleControllerReg['broker'] = "tcp://localhost:5570"
		# publications
		publications = {}
		# publications['pistar'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}
		# publications['P'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 1}
		# publications['state'] = {'propertyType': 'string', 'propertyUnit': 'none', 'propertyValue': 'BS_UNKNOWN'}
		singleControllerReg['publications'] = publications
		# subscriptions
		subscriptions = {}
		auction = {}
		marketName = controllers[key]['controller_information']['marketName'] # Retrieve market name fro controller input information
		auction[marketName] = {}
		auction[marketName]['retail_price'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}
		subscriptions[AgentType] = auction 
		singleControllerReg['subscriptions'] = subscriptions
		# Values recieved from house
		values = {}
		controllerDict['Dsystem'] = ['' for i in range(NDsystems)]
		for k in range(NDsystems):
			values['fan_power#'+ 'gridlabdSimulator' + str(k+1)] = {'topic': "gridlabdSimulator" + str(k+1) + "/" + houseName + "/fan_power", 'default': 0, 'type': 'double', 'list': 'false'}
			
			controllerDict['Dsystem'][k] = "gridlabdSimulator" + str(k+1)
			
			values['system_mode#'+ 'gridlabdSimulator' + str(k+1)] = {'topic':  "gridlabdSimulator" + str(k+1) + "/" + houseName + "/system_mode", 'default': 0.9, 'type': 'double', 'list': 'false'}
			
			values['Qi#'+ 'gridlabdSimulator' + str(k+1)] = {'topic':  "gridlabdSimulator" + str(k+1) + "/" + houseName + "/Qi", 'default': 0.9, 'type': 'double', 'list': 'false'}
			values['solar_gain#'+ 'gridlabdSimulator' + str(k+1)] = {'topic':  "gridlabdSimulator" + str(k+1) + "/" + houseName + "/solar_gain", 'default': 0.9, 'type': 'double', 'list': 'false'}
			values['RH#'+ 'gridlabdSimulator' + str(k+1)] = {'topic': "gridlabdSimulator" + str(k+1)  + "/" + houseName + "/outdoor_rh", 'default': 0, 'type': 'double', 'list': 'false'}
			values['outdoor_temperature#'+ 'gridlabdSimulator' + str(k+1)] = {'topic': "gridlabdSimulator" + str(k+1)  + "/" + houseName + "/outdoor_temperature", 'default': 0.9, 'type': 'double', 'list': 'false'}
			values['VActual#'+ 'gridlabdSimulator' + str(k+1)] = {'topic': "gridlabdSimulator" + str(k+1)  + "/" + MeterName + "/voltage_12", 'default': 120, 'type': 'double', 'list': 'false'}
			
		singleControllerReg['values'] = values
		controllerDict['registration'] = singleControllerReg
		# Input data
		controllerDict['initial_values'] = controllers[key]
		# Write the controller into one json file:
		filename = folderName + "/controller_registration_" + key + ".json"
		op_controller = open(filename, "w")
		json.dump(controllerDict, op_controller)
		op_controller.close()
		
	# Write file for auction registration
	auctionReg = {}
	auctionReg['agentType'] = "auction"
	auctionReg['agentName'] = list(auctions.items())[0][0]
	auctionReg['timeDelta'] = 1 
	auctionReg['broker'] = "tcp://localhost:5570"
	publications = {}
	publications['controller']= {}
	for key, value in controllers.items():
		publications['controller'][key]={}
		publications['controller'][key]['retail_price'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}

	auctionReg['publications'] = publications
	subscriptions = {}
	controller = {}
	auctionDict = {}
	marketName = auctionReg['agentName'] # Retrieve market name fro controller input information
	for key, value in controllers.items():
		if controllers[key]['controller_information']['marketName'] == marketName:
			singleControllerReg = {}
			singleControllerReg[key] = {}
			singleControllerReg[key]['pistar'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}
			singleControllerReg[key]['P'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}
			singleControllerReg[key]['P_ON'] = {'propertyType': 'double', 'propertyUnit': 'none', 'propertyValue': 0.0}
			singleControllerReg[key]['state'] = {'propertyType': 'string', 'propertyUnit': 'none', 'propertyValue': 'OFF'}
			controller[key] = singleControllerReg[key]
	subscriptions['controller'] = controller   
	auctionReg['subscriptions'] = subscriptions
	# Values received from GridLAB-D
	values = {}
	#values['refload'] = {'topic': "gridlabdSimulator1/distribution_load", 'default': '0', 'type': 'complex', 'list': 'false'}
	auctionReg['values'] = values

	auctionDict['registration'] = auctionReg 
	# Input data
	auctionDict['initial_values'] = auctions[marketName]
	json.dump(auctionDict, op_auction) 
	
	# Close files
	ip.close()
	op_auction.close()

	return auctions, controllers

