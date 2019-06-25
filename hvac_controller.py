import warnings
import sys
import json
import fncs
import math
import random

# Class definition
class hvac_controller:

	# ====================Define instance variables ===================================
	def __init__(self, controllerDict,tmax,deltaT):
		# Obtain the registration data and initial values data
		agentRegistration = controllerDict['registration']
		agentInitialVal = controllerDict['initial_values']
		self.dayMax = int(tmax/(24*3600) + 1) #21
		
		# Initialize the variables
		self.market = { 'retail_price': -1}
		self.house = { } 
		self.controller = {'name': 'none', 'marketName': 'none', 'houseName': 'none', 'houseTag': 'none', 'setpoint': 'none', 'bid_id': 'none', 'deadband': 0, 'period': -1,  'setpoint0': -1, 'time_off': sys.maxsize}
		self.controller['name'] = agentRegistration['agentName']
		self.controller['Dsystem'] = controllerDict['Dsystem']
		for k in range(len(self.controller['Dsystem'])):
			temp = controllerDict['Dsystem'][k]
			self.house[temp] = {}
			
			# from auctionDict initial_values
			self.house[temp]['Tbliss'] = agentInitialVal['house_information']['Tbliss']
			self.house[temp]['mu'] = agentInitialVal['house_information']['mu']
			self.house[temp]['P'] = 0 # agentInitialVal['house_information']['P']
			self.house[temp]['P_ON'] = 0 # agentInitialVal['house_information']['P']
			self.house[temp]['db'] = 4 # agentInitialVal['house_information']['db']
			self.house[temp]['theta'] = 10 # agentInitialVal['house_information']['theta']
			
			# House initial conditions 
			self.house[temp]['systemmode'] = agentInitialVal['house_information']['system_mode']
			self.house[temp]['Ta'] = agentInitialVal['house_information']['Ta']
			self.house[temp]['Tm'] = agentInitialVal['house_information']['Tm']
			
			# House base structure parameters 
			self.house[temp]['cooling_COP'] = agentInitialVal['house_information']['cooling_COP']
			self.house[temp]['OSF'] = agentInitialVal['house_information']['OSF']
			self.house[temp]['h'] = agentInitialVal['house_information']['h']
			self.house[temp]['n'] = agentInitialVal['house_information']['n']
			self.house[temp]['R'] = agentInitialVal['house_information']['R']
			self.house[temp]['A'] = agentInitialVal['house_information']['A']
			self.house[temp]['fI'] = agentInitialVal['house_information']['fi']
			self.house[temp]['fS'] = agentInitialVal['house_information']['fs']
			self.house[temp]['I'] = agentInitialVal['house_information']['I']
			self.house[temp]['Rc'] = agentInitialVal['house_information']['Rc']
			self.house[temp]['Rd'] = agentInitialVal['house_information']['Rd']
			self.house[temp]['Rf'] = agentInitialVal['house_information']['Rf']
			self.house[temp]['Rw'] = agentInitialVal['house_information']['Rw']
			self.house[temp]['ECR'] = agentInitialVal['house_information']['ECR']
			self.house[temp]['EFR'] = agentInitialVal['house_information']['EFR']
			self.house[temp]['EWR'] = agentInitialVal['house_information']['EWR']
			self.house[temp]['hs'] = agentInitialVal['house_information']['hs']
			self.house[temp]['IWR'] = agentInitialVal['house_information']['IWR']
			self.house[temp]['mf'] = agentInitialVal['house_information']['mf']
			self.house[temp]['nd'] = agentInitialVal['house_information']['nd']
			self.house[temp]['WET'] = agentInitialVal['house_information']['WET']
			self.house[temp]['WWR'] = agentInitialVal['house_information']['WWR']
			
			# House derived but read from house controller 
			self.house[temp]['Rg'] = agentInitialVal['house_information']['Rg']
			self.house[temp]['SHGCNom'] = agentInitialVal['house_information']['SHGCNom']
			
			# House default values 
			self.house[temp]['DuctPressureDrop'] = 0.5
			self.house[temp]['LatCoolFrac'] = 0.3
			self.house[temp]['VNominal'] = 240
			self.house[temp]['CDT'] = 96.982; #degF # Change for diff location 
			self.house[temp]['HDT'] = -9.938; #degF # Change for diff location 
			self.house[temp]['DCT'] = 75; #degF
			self.house[temp]['DHT'] = 70; #degF
			self.house[temp]['CoolSupplyAirTemp'] = 50 #degF
			self.house[temp]['HeatSupplyAirTemp'] = 150 #degF
			self.house[temp]['DPS'] = 195 # RP doc
			
			# House forced terms 
			self.house[temp]['RH'] = 0
			self.house[temp]['Qs'] = 0
			self.house[temp]['QiTotal'] = 0
			self.house[temp]['QiHVAC'] = 0
			self.house[temp]['To'] = 0
			self.house[temp]['VActual'] = 240
			
			# House derived parameters
			self.house[temp]['Ca'] = 0
			self.house[temp]['Cm'] = 0
			self.house[temp]['Hm'] = 0
			self.house[temp]['Ua'] = 0
			self.house[temp]['DesCoolCap'] = 3000
			self.house[temp]['fan_design_airflow'] = 0
			
			
			# House parameter initialization  - values will be given after the first time step, thereforely here set as default zero values
			self.house[temp]['prevTa'] = self.house[temp]['Ta']
			self.house[temp]['TaCaseOFF'] = 72.5
			self.house[temp]['TaCaseON'] = 68.5
			self.house[temp]['TmCaseOFF'] = 72.5
			self.house[temp]['TmCaseON'] = 68.5
			self.house[temp]['pistar'] = 0
			self.house[temp]['realPowerWh'] = 0 
			self.house[temp]['PrevRealPowerWh'] = 0
			
			#Overall welfare parameters:
			self.house[temp]['welfareparams'] = {}
			for i in range(self.dayMax):
				self.house[temp]['welfareparams'][i] = {'theta': self.house[temp]['theta'], 'lumpsum' : 0.0, 'EC':[], 'Discomfort':[]} #welfare parameters
			self.house[temp]['welfareparams'][0]['theta'] = self.house[temp]['theta']
			
			#Overwriting initialized value
			self.house[temp]['mu'] = 1
			self.house[temp]['theta'] = 20
		
		self.house['h2'] = 0.1 # util/(min-degF^2)
		
		# Read and assign initial values from agentInitialVal
		# controller information
		self.controller['marketName'] = agentInitialVal['controller_information']['marketName']
		self.controller['houseName'] = agentInitialVal['controller_information']['houseName']

		# market information - Market registration information
		self.market['name'] = self.controller['marketName']
		self.market['retail_price'] = 0 #agentInitialVal['market_information']['retail_price']
		
		self.deltaT = deltaT # in secs
		self.day = 0
		self.prevday = 0

		# Generate agent publication dictionary
		self.fncs_publish = {
		'controller': {
		self.controller['name']: {
		'pistar': {'propertyType': 'double', 'propertyUnit': '', 'propertyValue': 0.0},
		'P': {'propertyType': 'double', 'propertyUnit': '', 'propertyValue': 0.0},
		'P_ON': {'propertyType': 'double', 'propertyUnit': '', 'propertyValue': 0.0},
		'state': {'propertyType': 'string', 'propertyUnit': '', 'propertyValue': 'BS_UNKNOWN'}
		}
		}
		}
		self.fncs_publish['controller'][self.controller['name']]['pistar'] = 9
		self.fncs_publish['controller'][self.controller['name']]['P'] = 3
		self.fncs_publish['controller'][self.controller['name']]['P_ON'] = 3
		self.fncs_publish['controller'][self.controller['name']]['state'] == "OFF"
		# Registrate the agent
		agentRegistrationString = json.dumps(agentRegistration)
		fncs.agentRegister(agentRegistrationString.encode('utf-8'))
		print('agent registration is done', flush = True)

	# ====================Rearrange object based on given initial values======================
	def initController(self):
		print('Initialized house controller',flush = True)

		for k in range(len(self.controller['Dsystem'])):
			temp = self.controller['Dsystem'][k]
			VNominal = self.house[temp]['VNominal']
			cooling_COP = self.house[temp]['cooling_COP']
			OSF = self.house[temp]['OSF']
			A = self.house[temp]['A']
			n = self.house[temp]['n']
			I = self.house[temp]['I']
			Rc = self.house[temp]['Rc']
			Rd = self.house[temp]['Rd']
			Rf = self.house[temp]['Rf']
			Rw = self.house[temp]['Rw']
			Rg = self.house[temp]['Rg']
			mf = self.house[temp]['mf']
			nd = self.house[temp]['nd']
			WET = self.house[temp]['WET']
			SHGCNom = self.house[temp]['SHGCNom']
			h = self.house[temp]['h']
			R = self.house[temp]['R']
			ECR = self.house[temp]['ECR']
			EFR = self.house[temp]['EFR']
			EWR = self.house[temp]['EWR']
			IWR = self.house[temp]['IWR']
			WWR = self.house[temp]['WWR']
			fi = self.house[temp]['fI']
			fs = self.house[temp]['fS'] 
			hs = self.house[temp]['hs']
			
			LatCoolFrac = self.house[temp]['LatCoolFrac']
			DuctPressureDrop = self.house[temp]['DuctPressureDrop']
			CDT = self.house[temp]['CDT']
			HDT = self.house[temp]['HDT']
			DCT = self.house[temp]['DCT']
			DHT = self.house[temp]['DHT']
			CoolSupplyAirTemp = self.house[temp]['CoolSupplyAirTemp']
			HeatSupplyAirTemp = self.house[temp]['HeatSupplyAirTemp']
			DPS = self.house[temp]['DPS']
			
			# GLD-determined parameters
			K = 3412 # units - Btu/[hr-kW], conversion factor to convert kW to Btu/hr;
			o = (0.117/ (745.7 * 0.42) ) * 8
			q = 745.7/(8 * 0.88)
			air_density = 0.0735;
			air_heat_capacity = 0.2402;
			A1d = 3.0 * 78.0 / 12.0
			
			Awt = 2*n*h*(1+R)*math.sqrt(A/(n*R))
			Ac = (A/n) * ECR
			Af = (A/n) * EFR
			Ad = nd * A1d
			Ag = WWR * Awt * EWR
			Aw = EWR * Awt - Ad - Ag
			
			VHa = air_density * air_heat_capacity;
			
			# print('Rc, Rd, Rf, Rg, Rw, I', Rc, Rd, Rf, Rg, Rw, I, flush = True)
			
			Ca = 3 * VHa * A * h # 3 VHa A h
			Cm = A * mf - 2 * VHa * A * h
			Hm = hs * ((Awt-Ag-Ad) + Awt*IWR + (Ac*n)/ECR)
			Ua = Ac/Rc + Af/Rf + Ag/Rg + Aw/Rw  + Ad/Rd + VHa*A*h*I
			
			DIG = 167.09 * math.pow(A,0.442)
			SHGC = Ag * SHGCNom * WET
			
			# print('SHGCNom, WET, OSF, LatCoolFrac',SHGCNom, WET, OSF,LatCoolFrac, flush = True)
			
			DCP = (1.0 + OSF) * (1.0 + LatCoolFrac) * ((Ua) * (CDT - DCT) + DIG + (DPS * SHGC));
			DesCoolCap = math.ceil(DCP/6000) * 6000
			
			DesignHeatCapacity = (1.0 + OSF) * (Ua) * (DHT - HDT);
			round_value = (DesignHeatCapacity) / 10000.0;
			DesignHeatCapacity = math.ceil(round_value) * 10000.0;
			DesignHeatAirflow = (DesignHeatCapacity/ ((HeatSupplyAirTemp- DHT) * VHa)) * (1/60)
			DesignCoolAirflow = (DesCoolCap / ((1.0 + LatCoolFrac) * ((DCT - CoolSupplyAirTemp) * VHa))) * (1/60)
			if DesignHeatAirflow > DesignCoolAirflow:
				fan_design_airflow = round(DesignHeatAirflow,2)
			else:
				fan_design_airflow = round(DesignCoolAirflow,2)
			E = fan_design_airflow
			
			# print('Ca, Cm, Hm, Ua calculated ', Ca, Cm, Hm, Ua, flush=True)
			# print('DesCoolCap, fan_design_airflow calculated ', DesCoolCap, E, flush=True)
			
			D = DuctPressureDrop * E
			P_FAN = round(math.ceil(o * D) * q,3) / 1000 # kW
			FanPow = P_FAN * K # Btu/hr
			
			# print('FanPow, P_FAN',DuctPressureDrop, FanPow, P_FAN,flush = True)
			
			# House derived parameters
			self.house[temp]['Ca'] = Ca
			self.house[temp]['Cm'] = Cm
			self.house[temp]['Hm'] = Hm
			self.house[temp]['Ua'] = Ua
			self.house[temp]['DesCoolCap'] = DesCoolCap
			self.house[temp]['P_FAN'] = P_FAN
			self.house[temp]['FanPow'] = FanPow
			
		print('',flush = True)

	# ====================extract float from string ===============================
	def get_num(self,fncs_string):
		return float(''.join(ele for ele in fncs_string if ele.isdigit() or ele == '.'))

	def get_number(self,value):
		#print('value:', value, flush=True)
		return float(''.join(ele for ele in value if ele.isdigit() or ele == '.' or ele == '-'))

	def get_complex_number(self,value):
		return complex(''.join(ele for ele in value if ele.isdigit() or ele == '.' or ele == '-' or ele == 'j' or ele == '+'))

	# ====================Obtain values from the broker ===========================
	def subscribeGLD(self, title, value,time_granted):
		if title.startswith('hvac_load'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('hvac_load#'+ self.controller['Dsystem'][k]):
					print('value:', value, 'P:', self.get_number(value), flush = True)
					#self.house[self.controller['Dsystem'][k]]['P'] = round(self.get_number(value),3)
					self.house[self.controller['Dsystem'][k]]['systemmode'] = "OFF"
					if self.get_number(value)!=0:
						self.house[self.controller['Dsystem'][k]]['systemmode'] = "COOL"
						# self.house[self.controller['Dsystem'][k]]['P_ON'] = round(self.get_number(value),3)
		if title.startswith('solar_gain'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('solar_gain#'+ self.controller['Dsystem'][k]):
					#print('Qs:', value, self.get_number(value), flush = True)
					self.house[self.controller['Dsystem'][k]]['Qs'] = self.get_number(value)
		if title.startswith('internal_gain'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('internal_gain#'+ self.controller['Dsystem'][k]):
					#print('QiTotal:', value, self.get_number(value), flush = True)
					self.house[self.controller['Dsystem'][k]]['QiTotal'] = self.get_number(value)
		if title.startswith('heat_cool_gain'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('heat_cool_gain#'+ self.controller['Dsystem'][k]):
					#print('QiHVAC:', value, self.get_number(value), flush = True)
					self.house[self.controller['Dsystem'][k]]['QiHVAC'] = self.get_number(value)
		if title.startswith('RH'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('RH#'+ self.controller['Dsystem'][k]):
					#print('RH:', value, self.get_number(value), flush = True)
					self.house[self.controller['Dsystem'][k]]['RH'] = self.get_number(value)
		if title.startswith('outdoor_temperature'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('outdoor_temperature#'+ self.controller['Dsystem'][k]):
					#print('To:', value, self.get_number(value), flush = True)
					self.house[self.controller['Dsystem'][k]]['To'] = self.get_number(value)
		if title.startswith('VActual'):
			for k in range(len(self.controller['Dsystem'])):
				if title.startswith('VActual#'+ self.controller['Dsystem'][k]):
					#print('VActual:', value, self.get_complex_number(value), round(abs(self.get_complex_number(value)),4), flush = True)
					self.house[self.controller['Dsystem'][k]]['VActual'] = round(abs(self.get_complex_number(value)),4)

	def CalPiStar(self,time_granted):
		for k in range(len(self.controller['Dsystem'])):
			# Rg = self.house[self.controller['Dsystem'][k]]['Rg']
			RH = self.house[self.controller['Dsystem'][k]]['RH']
			Qs = self.house[self.controller['Dsystem'][k]]['Qs']
			QiTotal = self.house[self.controller['Dsystem'][k]]['QiTotal']
			QiHVAC = self.house[self.controller['Dsystem'][k]]['QiHVAC']
			Qi = QiTotal - QiHVAC
			To = self.house[self.controller['Dsystem'][k]]['To']
			VActual = self.house[self.controller['Dsystem'][k]]['VActual']
			 
			Ta = self.house[self.controller['Dsystem'][k]]['Ta']
			Tm = self.house[self.controller['Dsystem'][k]]['Tm']
			
			TB = self.house[self.controller['Dsystem'][k]]['Tbliss']
			mu = self.house[self.controller['Dsystem'][k]]['mu']
			h2 = self.house['h2']
			deltaT = self.deltaT
			
			# GLD-determined parameters 
			VBase = 240
			K = 3412 # units - Btu/[hr-kW], conversion factor to convert kW to Btu/hr;
			fAC = 0.0
			
			FP = 0.8 #(unit free)
			FC = 0.0 #(unit free) 
			FZ = 0.2 #(unit free)
			a = 1.48924533 #(unit free);
			b = 0.00514995 # (1/oF);
			c = -0.01363961 #(unit free);
			d = 0.01066989 # (1/oF);
			e = 0.1 # (unit free)
			f = 1.0 #(unit free)
			g = 4.0 #(unit free)
			m = 10.0 #(unit free)
			
			fi = self.house[self.controller['Dsystem'][k]]['fI']
			fs = self.house[self.controller['Dsystem'][k]]['fS']
			cooling_COP = self.house[self.controller['Dsystem'][k]]['cooling_COP']
			LatCoolFrac = self.house[self.controller['Dsystem'][k]]['LatCoolFrac']
			VNominal = self.house[self.controller['Dsystem'][k]]['VNominal']
			Ca = self.house[self.controller['Dsystem'][k]]['Ca']
			Cm = self.house[self.controller['Dsystem'][k]]['Cm']
			Hm = self.house[self.controller['Dsystem'][k]]['Hm']
			Ua = self.house[self.controller['Dsystem'][k]]['Ua']
			DesCoolCap = self.house[self.controller['Dsystem'][k]]['DesCoolCap']
			P_FAN = self.house[self.controller['Dsystem'][k]]['P_FAN']
			FanPow = self.house[self.controller['Dsystem'][k]]['FanPow']
			
			# parameters that vary with time 
			VoltageFactorN = VActual/VNominal
			VoltageFactorB = VActual/VBase
			VoltageAdj = FP + FC * VoltageFactorB + FZ * VoltageFactorB * VoltageFactorB
			VF = FP + FC * VoltageFactorN + FZ * VoltageFactorN * VoltageFactorN
			LCF = e + LatCoolFrac / (f +  math.exp(g - m * RH/100) )
			DesCoolCapAdj = DesCoolCap * (a - b * To)
			cooling_COPAdj = cooling_COP / (c + d * To)
			
			P_HVAC = DesCoolCapAdj * VF / (K * cooling_COPAdj)
			HVACPow = VoltageAdj * DesCoolCapAdj / (1+LCF)
			
			PTotal = round( P_HVAC+P_FAN, 3)
			QiHVACCal = - HVACPow + FanPow
			
			# print('PTotal Cal: ', PTotal, flush=True)
			# print('VActual, RH, Qs, Qi, QiTotal, QiHVAC', VActual, RH, round(Qs,2), round(Qi,2), round(QiTotal,2), round(QiHVAC,2), flush = True )
			# print('QiHVAC, QiHVACCal:', round(QiHVAC,2), round(QiHVACCal,2), flush = True) 
			# print('h2, mu:', h2, mu, flush=True)
			
			# pistar calculation
			h2delT = h2 * deltaT/60 # utils/(min-degF^) * min
			K11 = 2 * h2delT * (1 - fAC) / (mu * Ca)
			K21 =  Hm/Ca
			K22 =  Ua/Ca
			K4 = (1-fAC) / (2 * Ca)
			
			# vary with time
			K12_Fan = (HVACPow - FanPow) /PTotal 
			K3 = ((1-fs) * Qs + (1-fi) * Qi)/Ca
			pistar = round(K11*K12_Fan * ( (Ta - TB) + K21*(Tm - Ta)*deltaT/3600+ K22*(To - Ta)*deltaT/3600+ K3*deltaT/3600 - K4*(HVACPow - FanPow)*(deltaT/3600) ), 2)
			
			print('To, Tm, Ta : ', To, round(Tm,2), round(Ta,2), 'pistar:', pistar, flush = True)
			#print('K11:', round(K11,6), 'K12_Fan: ', round(K12_Fan,2), 'K21:', round(K21,2), 'K22:', round(K22,2), 'K31:', round(K31,2), 'K41:', round(K41,2), 'K41*QiHVACCal:', round(K41*QiHVACCal,2), flush = True)
			
			TaCaseOFF = (1- (deltaT/3600) * ((Ua+Hm)/Ca)) * Ta + (deltaT/3600) * (Hm/Ca) * Tm + (deltaT/3600) * (Ua/Ca) * To + (deltaT/3600) * (1/ Ca) *((1-fs)*Qs +(1-fi)*Qi)
			TaCaseON = (1- (deltaT/3600) * ((Ua+Hm)/Ca)) * Ta + (deltaT/3600) * (Hm/Ca) * Tm + (deltaT/3600) * (Ua/Ca) * To + (deltaT/3600) * (1/ Ca) *((1-fs)*Qs +(1-fi)*Qi) + (deltaT/3600) * (1/Ca) * (1-fAC) * QiHVACCal
			pistarCheck = h2delT * ((TaCaseOFF-TB)*(TaCaseOFF-TB) - (TaCaseON-TB)*(TaCaseON-TB)) / (mu * PTotal * (deltaT/3600))
			TmCaseOFF = (deltaT/3600) * Hm/Cm * Ta + (1- (deltaT/3600) * Hm/Cm) * Tm + (deltaT/3600) * (1/ Cm) *(fs*Qs +fi*Qi);
			TmCaseON = (deltaT/3600) * Hm/Cm * Ta + (1- (deltaT/3600) * Hm/Cm) * Tm + (deltaT/3600) * (1/ Cm) *(fs*Qs +fi*Qi) + (deltaT/3600) * (1/Cm) * fAC * QiHVACCal
			print('TaCaseOFF, TaCaseON, TmCaseOFF, TmCaseON, pi*Check:', round(TaCaseOFF,2) , round(TaCaseON,2), round(TmCaseOFF,2) , round(TmCaseON,2), round(pistarCheck,2), flush = True)  
			
			self.house[self.controller['Dsystem'][k]]['pistar'] = pistar
			self.house[self.controller['Dsystem'][k]]['TaCaseOFF'] = TaCaseOFF
			self.house[self.controller['Dsystem'][k]]['TaCaseON'] = TaCaseON
			self.house[self.controller['Dsystem'][k]]['TmCaseOFF'] = TmCaseOFF
			self.house[self.controller['Dsystem'][k]]['TmCaseON'] = TmCaseON
			
			systemmode = self.house[self.controller['Dsystem'][k]]['systemmode']
			#print('systemmode', systemmode, flush=True)
			if systemmode == 'COOL':
				self.fncs_publish['controller'][self.controller['name']]['state'] = "MayRunON"
				self.fncs_publish['controller'][self.controller['name']]['P'] = PTotal
			else:
				self.fncs_publish['controller'][self.controller['name']]['state'] = "MayRunOFF"
				self.fncs_publish['controller'][self.controller['name']]['P'] = 0
			
			self.fncs_publish['controller'][self.controller['name']]['pistar'] = pistar
			self.fncs_publish['controller'][self.controller['name']]['P_ON'] = PTotal
			
		fncs_publishString = json.dumps(self.fncs_publish)
		print('publishing:',  fncs_publishString, flush = True)
		fncs.agentPublish(fncs_publishString)

	# ====================Obtain values from the broker ===========================
	def subscribeVal(self, fncs_sub_value_String,time_granted):

		# Update market and house information at this time step from subscribed key values:
		#print('day:', self.day, 'prev day:', self.prevday, flush=True)
		if "DSO" in fncs_sub_value_String:
			for k in range(len(self.controller['Dsystem'])):
				self.market['retail_price'] = fncs_sub_value_String['DSO'][self.market['name']]['retail_price']
				
				retail_price = self.market['retail_price']
				pistar = self.house[self.controller['Dsystem'][k]]['pistar']	
				systemmode = self.house[self.controller['Dsystem'][k]]['systemmode']
				
				print('time:', time_granted, 'retail price:', retail_price, 'pistar:', pistar, 'systemmode:', systemmode, flush=True)
				if retail_price > pistar: #retail_price > pistar
					#print('pi* is below retail_price: setting Cool OFF for the house', flush = True)
					systemmode = "OFF"
					self.fncs_publish['controller'][self.controller['name']]['state'] = "OFF"
					self.house[self.controller['Dsystem'][k]]['Ta'] = self.house[self.controller['Dsystem'][k]]['TaCaseOFF'] 
					self.house[self.controller['Dsystem'][k]]['Tm'] = self.house[self.controller['Dsystem'][k]]['TmCaseOFF'] 
				elif retail_price <= pistar:
					#print('pi* is above retail_price: setting Cool ON for the house', flush = True)
					systemmode = "COOL"
					self.fncs_publish['controller'][self.controller['name']]['state'] = "COOL"
					self.house[self.controller['Dsystem'][k]]['Ta'] = self.house[self.controller['Dsystem'][k]]['TaCaseON']
					self.house[self.controller['Dsystem'][k]]['Tm'] = self.house[self.controller['Dsystem'][k]]['TmCaseON'] 
				
				##########        Alternative bid function ##########
				
				# theta = self.house[self.controller['Dsystem'][k]]['theta']
				# TB = self.house[self.controller['Dsystem'][k]]['Tbliss']
				# db = self.house[self.controller['Dsystem'][k]]['db']
				# Ta = self.house[self.controller['Dsystem'][k]]['Ta']
				# pistarH = round(theta * (Ta - TB) / db,2)
				# pistar = pistarH
				# if Ta >= TB + db:
					# systemmode = "COOL"
					# self.fncs_publish['controller'][self.controller['name']]['state'] = "COOL"
					# self.house[self.controller['Dsystem'][k]]['Ta'] = self.house[self.controller['Dsystem'][k]]['TaCaseON']
					# self.house[self.controller['Dsystem'][k]]['Tm'] = self.house[self.controller['Dsystem'][k]]['TmCaseON'] 
				# elif TB - db >= Ta:
					# systemmode = "OFF"
					# self.fncs_publish['controller'][self.controller['name']]['state'] = "OFF"
					# self.house[self.controller['Dsystem'][k]]['Ta'] = self.house[self.controller['Dsystem'][k]]['TaCaseOFF']  
					# self.house[self.controller['Dsystem'][k]]['Tm'] = self.house[self.controller['Dsystem'][k]]['TmCaseOFF']
				# elif retail_price > pistar:
					# systemmode = "OFF"
					# self.fncs_publish['controller'][self.controller['name']]['state'] = "OFF"
					# self.house[self.controller['Dsystem'][k]]['Ta'] = self.house[self.controller['Dsystem'][k]]['TaCaseOFF']  
					# self.house[self.controller['Dsystem'][k]]['Tm'] = self.house[self.controller['Dsystem'][k]]['TmCaseOFF']
				# else:
					# systemmode = "COOL"
					# self.fncs_publish['controller'][self.controller['name']]['state'] = "COOL"
					# self.house[self.controller['Dsystem'][k]]['Ta'] = self.house[self.controller['Dsystem'][k]]['TaCaseON']
					# self.house[self.controller['Dsystem'][k]]['Tm'] = self.house[self.controller['Dsystem'][k]]['TmCaseON'] 
				
				self.house[self.controller['Dsystem'][k]]['systemmode'] = systemmode
				print('setting pistar to:', pistar, flush = True)	
				print('sending systemmode: ',systemmode)
				publish_key = self.controller['Dsystem'][k] + '_system_mode'
				#print('publish_key:', publish_key, flush = True)
				fncs.publish(publish_key, systemmode)


	# ==================================Sync content===========================
	def sync(self, time_granted):
		print('sync: time: ', time_granted, flush=True)
		# fncs_publishString = json.dumps(self.fncs_publish)
		# print('time publishing fncs_publishString: ', time_granted, fncs_publishString, flush = True)
		# fncs.agentPublish(fncs_publishString)