import sys
import random
import numpy as np
import yaml
import math

if len(sys.argv) == 5:
	NDsystems = int(sys.argv[1])
	mix = int(sys.argv[2])
	H_index = int(sys.argv[3])
	avg_house = int(sys.argv[4])
elif len(sys.argv) == 4:
	NDsystems = int(sys.argv[1])
	mix = int(sys.argv[2])
	H_index = int(sys.argv[3])
	avg_house = 5000
elif len(sys.argv) == 3:
	NDsystems = int(sys.argv[1])
	mix = int(sys.argv[2])
	H_index = 2
	avg_house = 5000
elif len(sys.argv) == 2:
	NDsystems = int(sys.argv[1])
	mix = 0
	H_index = 2
	avg_house = 5000
elif len(sys.argv) == 1:
	NDsystems = 1
	mix = 0
	H_index = 2
	avg_house = 5000


AgentType = 'IDSO' 
Name = '1' 
HouseController = 'smart_controller'

f1 = open('loadobjects.txt', 'r')

def genphaseslist(ph):
	res_list = []
	ph = ph.replace("\"","")
	ph = ph.replace(";","")
	for i in ph:
		if i == 'A' or i == 'B' or i == 'C':
			res_list.append(i)
	return res_list


objects = {}
objname = ''

lines_string = f1.readlines()

for i in lines_string:
	t = i.split()
	if len(t) != 0:
		if t[0] == 'object':
			objname = t[1]
			objects[objname] = {}
		if t[0] == 'name':
			objects[objname]['name'] = t[1].replace(";","")
		if t[0] == 'phases':
			objects[objname]['phases'] = t[1].replace(";","")
			objects[objname]['phases_list'] = genphaseslist(objects[objname]['phases'])
			objects[objname]['no_houses'] = {k: 0 for k in objects[objname]['phases_list']}
			objects[objname]['house_mix'] = [[0,0] for k in objects[objname]['no_houses']]
		if t[0] == 'voltage_A':
			objects[objname][ 'voltage_A'] = t[1].replace(";","")
		if t[0] == 'voltage_B':
			objects[objname][ 'voltage_B'] = t[1].replace(";","")
		if t[0] == 'voltage_C':
			objects[objname][ 'voltage_C'] = t[1].replace(";","")
		if t[0] == 'constant_power_A':
			objects[objname][ 'constant_power_A'] = t[1].replace(";","")
		if t[0] == 'constant_power_B':
			objects[objname][ 'constant_power_B'] = t[1].replace(";","")
		if t[0] == 'constant_power_C':
			objects[objname][ 'constant_power_C'] = t[1].replace(";","")
		if t[0] == 'constant_current_A':
			objects[objname][ 'constant_current_A'] = t[1].replace(";","")
		if t[0] == 'constant_current_B':
			objects[objname][ 'constant_current_B'] = t[1].replace(";","")
		if t[0] == 'constant_current_C':
			objects[objname][ 'constant_current_C'] = t[1].replace(";","")
		if t[0] == 'constant_impedance_A':
			objects[objname][ 'constant_impedance_A'] = t[1].replace(";","")
		if t[0] == 'constant_impedance_B':
			objects[objname][ 'constant_impedance_B'] = t[1].replace(";","")
		if t[0] == 'constant_impedance_C':
			objects[objname][ 'constant_impedance_C'] = t[1].replace(";","")
		if t[0] == 'nominal_voltage':
			objects[objname][ 'nominal_voltage'] = t[1].replace(";","")
		if t[0] == '}':
			objname = ''

NumNodes = 0
TotalHouses = 0
for objname,objdata in objects.items():
	NumNodes = NumNodes + len(objects[objname]['phases_list'])
	for ph in objdata['phases_list']:
		no_houses = 0
		for k, v in objdata.items():
			nom_volt = float(objdata['nominal_voltage'])
			if k == 'constant_power_' + ph:
				no_houses = no_houses + math.ceil(math.sqrt(complex(v).real* complex(v).real+ complex(v).imag*complex(v).imag)/avg_house)
				#print('no_houses:', no_houses, flush = True)
			if k == 'constant_current_' + ph:
				no_houses = no_houses + math.ceil(abs((nom_volt)*complex(v))/avg_house)
				#print('no_houses:', no_houses, flush = True)
			if k == 'constant_impedance_' + ph:
				no_houses = no_houses + math.ceil(abs((nom_volt*nom_volt)/complex(v))/avg_house)
				#print('no_houses:', no_houses, flush = True)
		objects[objname]['no_houses'][ph] = no_houses
		TotalHouses = TotalHouses + no_houses

print('TotalHouses:', TotalHouses)
print('Nodes:', NumNodes, flush = True)

TH = '_' + str(TotalHouses) + '_'
housetype = ["Small_Poor_Poor", "Normal_Normal_Normal", "Large_Good_Good"]
feeder = 'feeder123_'
glm = '.glm'

# attributes related to HVAC 
cooling_COP = [3.5, 3.8, 4.1]
over_sizing_factor = [0.0, 0.1, 0.2]

# attributes related to size [Small Normal Large]
ceiling_height = [8, 8, 8]
number_of_stories = [1, 1, 2]
aspect_ratio = [1.5, 1.5, 1.5]
floor_area = [864, 1350, 2352]; 

# attributes related to thermal integrity [Poor Normal Good]
mass_internal_gain_fraction = [0.5, 0.5, 0.5]
mass_solar_gain_fraction = [0.5, 0.5, 0.5]
glass_type = ['GLASS', 'GLASS', 'LOW_E_GLASS'] 
glazing_layers = ['TWO', 'TWO', 'THREE']
airchange_per_hour = [1.5, 1, 0.5] 
Rroof = [19, 30, 48] 
Rdoors = [3, 3, 11] 
Rfloor = [4, 19, 30] 
Rwall = [11, 11, 22] 
window_frame = ['ALUMINIUM', 'THERMAL_BREAK', 'INSULATED']
#Rwindows = [0.79, 1.23, 3.26] #[Poor Normal Good]

# attributes related to interior-exterior types [Poor Normal Good]
exterior_ceiling_fraction = [1, 1, 1]
exterior_floor_fraction = [1, 1, 1]
exterior_wall_fraction = [1, 1, 1]
glazing_treatment = ['REFL', 'REFL', 'HIGH_S']
interior_surface_heat_transfer_coeff = [1.46, 1.46, 1.46]
interior_exterior_wall_ratio = [1.5, 1.5, 1.5]
total_thermal_mass_per_floor_area = [4.5, 4.0, 3.5]
number_of_doors = [1, 2, 4]
window_exterior_transmission_coefficient = [1.0, 0.6, 0.6]
window_wall_ratio = [0.15, 0.15, 0.15]


for objname,objdata in objects.items():
	objects[objname]['house_mix'] = {j : [H_index-1 for i in range(v)] for j,v in objects[objname]['no_houses'].items()}

feeder_json = 'runHouseholds_' + str(TotalHouses) + '.bat'
f3 = open(feeder_json,'w')

housedata = {}
realpowerdata = {}
hvacdata = {}

auction_datayaml = {}
auction_datayaml['name'] = AgentType + '_' + Name 
auction_datayaml['time_delta'] = '1s'
auction_datayaml['broker'] = 'tcp://localhost:5570'
auction_datayaml['values'] = {}
auction_datayaml['values']['WPDAM'] = {'topic': 'ames/DailyLMP', 'default': 1}
auction_datayaml['values']['WPRTM'] = {'topic': 'ames/RTLMP', 'default': 1}

for k in range(NDsystems):
	auction_datayaml['values']['distribution_load#'+'gridlabdSimulator'+str(k+1)] = {'topic': 'gridlabdSimulator'+str(k+1)+'/distribution_load', 'default': 0.0}
	auction_datayaml['values']['distribution_energy#'+'gridlabdSimulator'+str(k+1)] = {'topic': 'gridlabdSimulator'+str(k+1)+'/distribution_energy', 'default': 0.0}


f = open('IEEE123.glm', 'r')
lines_string = f.readlines()

for i in range(NDsystems):
	feeder_glm = 'IEEE123Modified' + str(NDsystems) + glm
	f2 = open(feeder_glm,'w')

	for i in lines_string:
		print(i, file=f2)

	print('object fncs_msg {', file=f2)
	print('     name gridlabdSimulator1;', file=f2)
	print('     parent network_node;', file=f2)
	print('     configure '+ 'IEEE123Modified' + str(NDsystems)+'_FNCS_Config.txt;', file=f2)
	print('    option "transport:hostname localhost, port 5570";', file=f2)
	print('}', file=f2)
	
	for objname,objdata in objects.items():
		data = {'node': {'name' : '', 'phases': '', 'voltage_A': '', 'voltage_B': '', 'voltage_C': '', 'nominal_voltage': 0.0},
		'transformer':{'name' : '', 'phases': '', 'from': '', 'to' : '', 'configuration':''},
		'triplex_node_1' : {'name' : '', 'phases' : '', 'nominal_voltage': 0.0},
		'triplex_line' : {'name' : '', 'phases':'', 'from' : '', 'to':'', 'length': '', 'configuration': ''},
		'triplex_node_2' : {'name' : '', 'phases' : '', 'nominal_voltage': 0.0},
		'triplex_meter' : {'name' : '', 'parent' : '', 'groupid': '', 'phases':'', 'nominal_voltage':0.0},
		'house' : {'name' : '', 'parent' : ''}
		}
		for key,val in objdata.items():
			if key == 'name' or key == 'phases' or key == 'voltage_A' or key == 'voltage_B' or key == 'voltage_C' or key == 'nominal_voltage':
				data['node'][key] = val
		
		print('object node:'+data['node']['name']+ ' {', file=f2)
		for k,v in data['node'].items():
			if k == 'name':
				print(k, 'n'+str(v) + ';', file=f2)
			else:
				print(k, str(v) + ';', file=f2)
		print("}", file=f2)
		
		val = objdata['phases_list']
		for ph in val:
			data['transformer']['name'] = 'center_tap_' + str(data['node']['name']) + str(ph)
			data['triplex_node_1']['name'] = 'triplex_node_' + str(data['node']['name']) + str(ph)
			data['transformer']['phases'] = str(ph) + 'S'
			data['transformer']['from'] = 'n'+ str(data['node']['name'])
			data['transformer']['to'] = data['triplex_node_1']['name']
			data['transformer']['configuration'] = str(ph) + 'S_config'
			data['triplex_node_1']['phases'] = str(ph) + 'S'
			data['triplex_node_1']['nominal_voltage'] = 120
			
			for key, val in data.items():
				if key == 'triplex_node_1':
					print('object triplex_node {', file=f2)
					for k,v in val.items():
						print(k, str(v) + ';', file=f2)
					print("}", file=f2)
				if key == 'transformer':
					print('object ' + key + ' {', file=f2)
					for k,v in val.items():
						print(k, str(v) + ';', file=f2)
					print("}", file=f2)

			HouseNo = objects[objname]['no_houses'][ph]
			for j in range(HouseNo):
				data['triplex_line']['name'] = 'triplex_line_' + str(data['node']['name']) + str(ph) + '_' + str(j+1)
				data['triplex_node_2']['name'] = 'triplex_node_' + str(data['node']['name']) + str(ph)+ '_' + str(j+1)
				data['triplex_meter']['name'] = 'triplex_meter_' + str(data['node']['name'])+ str(ph) + '_' + str(j+1)
				house_index = str(data['node']['name'])+ str(ph) + '_' + str(j+1)
				data['house']['name'] = 'house_'+ house_index
				if i ==0:
					print('start /b cmd /c python ' + HouseController + '.py input/controller_registration_'+data['house']['name']+'_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/'+data['house']['name']+'.log 2^>^&1', file = f3)
				
				for k in range(NDsystems):
					auction_datayaml['values']['RealPowerkWh#' + 'gridlabdSimulator' + str(k+1) + '#' + data['house']['name']] = {'topic' : 'gridlabdSimulator' + str(k+1) + '/' + data['house']['name']+'/realPowerkWh', 'default' : 0.0}
					# auction_datayaml['values']['PowerkW#' + 'gridlabdSimulator' + str(k+1) + '#' + data['house']['name']] = {'topic' : 'gridlabdSimulator' + str(k+1) + '/' + data['house']['name']+'/realPowerkW', 'default' : 0.0}
					auction_datayaml['values']['hvac_load#' + 'gridlabdSimulator' + str(k+1) + '#' + data['house']['name']] = {'topic' :'gridlabdSimulator' + str(k+1) + '/' + data['house']['name']+'/hvac_load', 'default' : 0.0}
				
				details = {'topic':'controller_'+data['house']['name']+'_thermostat_controller/TransactiveAgentOutput', 'default': {"controller":{data['house']['name']:{"pistar":{"propertyType":"double","propertyUnit":"none","propertyValue":0.0},"P":{"propertyType":"double","propertyUnit":"none","propertyValue":0.0},"P_ON":{"propertyType":"double", "propertyUnit": "none", "propertyValue": 0.0},"state":{"propertyType":"string","propertyUnit":"none","propertyValue":"ON"}}}}}
				auction_datayaml['values'][data['house']['name']] = details
				
				data['triplex_line']['phases'] = str(ph) + 'S'
				data['triplex_line']['from'] = data['triplex_node_1']['name']
				data['triplex_line']['to'] = data['triplex_node_2']['name']
				data['triplex_line']['length'] = '100 ft'
				data['triplex_line']['configuration'] = 'triplex_line_configuration_1'
				
				data['triplex_node_2']['phases'] = str(ph) + 'S'
				data['triplex_node_2']['nominal_voltage'] = 120
				
				
				data['triplex_meter']['parent'] = data['triplex_node_2']['name']
				data['triplex_meter']['groupid'] = 'triplex_node_meter'+ str(data['node']['name']) + str(ph)
				data['triplex_meter']['phases'] = str(ph) + 'S'
				data['triplex_meter']['nominal_voltage'] = 120
				
				data['house']['parent'] = data['triplex_meter']['name']
				for key, val in data.items():
					if key == 'triplex_node_2':
						print('object triplex_node {', file=f2)
						for k,v in val.items():
							print(k, str(v) + ';', file=f2)
						print("}", file=f2)
					if key == 'triplex_line' or key == 'triplex_meter':
						print('object ' + key + ' {', file=f2)
						for k,v in val.items():
							print(k, str(v) + ';', file=f2)
						print("}", file=f2)
					if key == 'house':
						print('object ' + key + ' {', file=f2)
						for k,v in val.items():
							print(k, str(v) + ';', file=f2)
						
						rand_param = round(random.uniform(68,76),2)
						rand_param = 72
						print('air_temperature ' + str(rand_param) + ';', file=f2)
						print('mass_temperature ' + str(rand_param) + ';', file=f2)
						print('heating_system_type ', end='', file=f2)
						x=np.random.random_sample()
						if x<=1:
							print('GAS;',file=f2)
						elif x>=0.7112 and x<0.8722:
							print('HEAT_PUMP;',file=f2)
						else:
							print('RESISTANCE;',file=f2)
							
						print('cooling_system_type ', end='',file=f2)
						if x<=1:
							if x <= 1:
								print('ELECTRIC;',file=f2)
							else:
								print('NONE;',file=f2)
						
						print('fan_type ONE_SPEED;',file=f2)						
						print('thermostat_control NONE;', file=f2)
						
						RN = random.uniform(0,1)
						print('system_mode COOL;', file=f2)

						house_mix = objects[objname]['house_mix'][ph]
						if mix == 1:
							rand_house = int(random.uniform(0,3))
						else:
							rand_house = house_mix[j]
						#print('rand_house: '+str(rand_house))
						
						# attributes related to HVAC [L M H]
						print('cooling_COP ' + str(cooling_COP[rand_house]) +';', file=f2)
						print('over_sizing_factor ' + str(over_sizing_factor[rand_house]) +';', file=f2)
						
						
						# attributes related to size [Small Normal Large]
						print('ceiling_height ' + str(ceiling_height[rand_house]) +';', file=f2)
						print('number_of_stories ' + str(number_of_stories[rand_house]) +';', file=f2)
						print('aspect_ratio ' + str(aspect_ratio[rand_house]) +';', file=f2)
						print('floor_area ' + str(floor_area[rand_house])+';', file=f2)
						
						# attributes related to thermal integrity [Poor Normal Good]
						print('mass_internal_gain_fraction ' + str(mass_internal_gain_fraction[rand_house]) +';', file=f2)
						print('mass_solar_gain_fraction ' + str(mass_solar_gain_fraction[rand_house]) +';', file=f2)
						print('glass_type ' + str(glass_type[rand_house]) +';', file=f2)
						print('glazing_layers ' + str(glazing_layers[rand_house]) +';', file=f2)
						print('airchange_per_hour ' + str(airchange_per_hour[rand_house]) +';', file=f2)
						print('Rroof ' + str(Rroof[rand_house]) +';', file=f2)
						print('Rdoors ' + str(Rdoors[rand_house]) +';', file=f2)
						print('Rfloor ' + str(Rfloor[rand_house]) +';', file=f2)
						print('Rwall ' + str(Rwall[rand_house]) +';', file=f2)
						#print('Rwindows ' + str(Rwindows[rand_house]) +';', file=f2)
						print('window_frame ' + str(window_frame[rand_house]) +';', file=f2)

						# attributes related to interior-exterior types [Poor Normal Good]
						print('exterior_ceiling_fraction ' + str(exterior_ceiling_fraction[rand_house]) +';', file=f2)
						print('exterior_floor_fraction ' + str(exterior_floor_fraction[rand_house]) +';', file=f2)
						print('exterior_wall_fraction ' + str(exterior_wall_fraction[rand_house]) +';', file=f2)
						print('glazing_treatment ' + str(glazing_treatment[rand_house]) +';', file=f2)
						print('interior_surface_heat_transfer_coeff ' + str(interior_surface_heat_transfer_coeff[rand_house]) +';', file=f2)
						print('interior_exterior_wall_ratio ' + str(interior_exterior_wall_ratio[rand_house]) +';', file=f2)
						print('total_thermal_mass_per_floor_area ' + str(total_thermal_mass_per_floor_area[rand_house]) +';', file=f2)
						print('number_of_doors ' + str(number_of_doors[rand_house]) +';', file=f2)
						print('window_exterior_transmission_coefficient ' + str(window_exterior_transmission_coefficient[rand_house]) +';', file=f2)
						print('window_wall_ratio ' + str(window_wall_ratio[rand_house]) +';', file=f2)
						
						rand_param = int(random.uniform(-1000,1000))
						
						
						print('object occupantload {', file=f2)
						print('number_of_occupants 1;' , file=f2)
						print('occupancy_fraction 1.0;' , file=f2)
						print('};', file=f2)
						
						print('object ZIPload {', file=f2)
						print('name lights_' + house_index + ";", file=f2)
						print('schedule_skew ' + str(rand_param) + ";", file=f2)
						print('base_power LIGHTS*2;', file=f2)
						print('current_fraction 0;', file=f2)
						print('impedance_fraction 1;', file=f2)
						print('power_fraction 0;', file=f2)
						print('current_pf 0;', file=f2)
						print('impedance_pf 1;', file=f2)
						print('power_pf 0;', file=f2)
						print('heat_fraction 0.8;', file=f2)
						print('};', file=f2)
						
						x2=np.random.random_sample()
						if x2<=1:
							print('object ZIPload {', file=f2)
							print('name clotheswasher_' + house_index + ";", file=f2)
							print('schedule_skew ' + str(rand_param) + ";", file=f2)
							print('base_power CLOTHESWASHER*1;', file=f2)
							print('current_fraction 0;', file=f2)
							print('impedance_fraction 0;', file=f2)
							print('power_fraction 1;', file=f2)
							print('current_pf 0.97;', file=f2)
							print('impedance_pf 0.97;', file=f2)
							print('power_pf 0.97;', file=f2)
							print('heat_fraction 0.8;', file=f2)
							print('};', file=f2)
						
						x3=np.random.random_sample()
						if x3<=1:
							print('object ZIPload {', file=f2)
							print('name refrigerator_' + house_index + ";", file=f2)
							print('schedule_skew ' + str(rand_param) + ";", file=f2)
							print('base_power REFRIGERATOR*1;', file=f2)
							print('current_fraction 0;', file=f2)
							print('impedance_fraction 0;', file=f2)
							print('power_fraction 1;', file=f2)
							print('current_pf 0.97;', file=f2)
							print('impedance_pf 0.97;', file=f2)
							print('power_pf 0.97;', file=f2)
							print('heat_fraction 0.8;', file=f2)
							print('};', file=f2)
						
						x4=np.random.random_sample()
						
						if x4<=1:
							print('object ZIPload {', file=f2)
							print('name dryer_' + house_index + ";", file=f2)
							print('schedule_skew ' + str(rand_param) + ";", file=f2)
							print('base_power DRYER*1;', file=f2)
							print('current_fraction 0.1;', file=f2)
							print('impedance_fraction 0.8;', file=f2)
							print('power_fraction 0.1;', file=f2)
							print('current_pf 0.9;', file=f2)
							print('impedance_pf 1.0;', file=f2)
							print('power_pf 0.9;', file=f2)
							print('heat_fraction 0.8;', file=f2)
							print('};', file=f2)
						
						x5=np.random.random_sample()
						
						if x5<=1:
							print('object ZIPload {', file=f2)
							print('name freezer_' + house_index + ";", file=f2)
							print('schedule_skew ' + str(rand_param) + ";", file=f2)
							print('base_power FREEZER*1;', file=f2)
							print('current_fraction 0;', file=f2)
							print('impedance_fraction 0;', file=f2)
							print('power_fraction 1;', file=f2)
							print('current_pf 0.97;', file=f2)
							print('impedance_pf 0.97;', file=f2)
							print('power_pf 0.97;', file=f2)
							print('heat_fraction 0.8;', file=f2)
							print('};', file=f2)

						x6=np.random.random_sample()
						if x6<=1:
							print('object ZIPload {', file=f2)
							print('name range_' + house_index + ";", file=f2)
							print('schedule_skew ' + str(rand_param) + ";", file=f2)
							print('base_power RANGE*1;', file=f2)
							print('current_fraction 0;', file=f2)
							print('impedance_fraction 1;', file=f2)
							print('power_fraction 0;', file=f2)
							print('current_pf 0;', file=f2)
							print('impedance_pf 1;', file=f2)
							print('power_pf 0;', file=f2)
							print('heat_fraction 0.8;', file=f2)
							print('};', file=f2)

						print('object ZIPload {', file=f2)
						print('name microwave_' + house_index + ";", file=f2)
						print('schedule_skew ' + str(rand_param) + ";", file=f2)
						print('base_power MICROWAVE*1;', file=f2)
						print('current_fraction 0;', file=f2)
						print('impedance_fraction 0;', file=f2)
						print('power_fraction 1;', file=f2)
						print('current_pf 0.97;', file=f2)
						print('impedance_pf 0.97;', file=f2)
						print('power_pf 0.97;', file=f2)
						print('heat_fraction 0.8;', file=f2)
						print('};', file=f2)
						
						print('}', file=f2)

with open( './YAMLFiles/' + AgentType + '.yaml', 'w') as outfile: 
    yaml.dump(auction_datayaml, outfile, default_flow_style=False)