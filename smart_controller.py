'''
main file of the hvac_controller object, mainly used for assigning data read from input
'''
 
# import from library or functions
import csv
import fncs
import sys
import json

from hvac_controller import hvac_controller

if len(sys.argv) == 4:
	filename = sys.argv[1]
	tmax = int(sys.argv[2])
	deltaT = int(sys.argv[3])
elif len(sys.argv) == 1:
	tmax = 2 * 24 * 3600
	deltaT = 300
else:
	print ('usage: python fncsPYPOWER.py [rootname StartTime tmax dt]')
	sys.exit()

lp = open(filename).read()
controllerDict = json.loads(lp)

# ====================Initialize simulation time step and duration===============   
min_len = 60 # in s
hour_len = 3600 # in s
day_len = 24* hour_len # in s

# Create controller object:
controller_obj =  hvac_controller(controllerDict,tmax,deltaT)

time_granted = 0 # time variable for checking the retuned time from FNCS
timeSim= 0
flag1 = 1
falg2 = 1

# Start simulation for each time step:
while (time_granted < tmax):
	# =================Simulation for each time step ============================================ 
				
	print('', flush = True)
	print('time_granted:', time_granted, flush = True) 
	controller_obj.day = int(time_granted / day_len)

	# Initialization when time = 0
	if time_granted == 0:
		controller_obj.initController()

	if time_granted % deltaT == 0:
		flag1 = 1

	#Subscribe values from GLD
	if time_granted != 0:
		events = fncs.get_events()
		for key in events:
			title = key.decode()
			value = fncs.get_value(key).decode()
			controller_obj.subscribeGLD(title,value,time_granted)
			if flag1 == 1:	
				flag2 = 1
			
		# calculating pistar
		if flag1 == 1 and flag2 == 1:
			print('', flush = True)
			print('time:', time_granted, 'calculating pistar...', flush = True)
			controller_obj.CalPiStar(time_granted)	
			flag1 = 0
			flag2 = 0
	
	# Subscrib values from FNCS broker (or csv file here)
	if time_granted != 0:
		fncs_sub_value_String = ''
		fncs_sub_value_unicode = (fncs.agentGetEvents()).decode()
		if fncs_sub_value_unicode != '':
			fncs_sub_value_String = json.loads(fncs_sub_value_unicode)
			controller_obj.subscribeVal(fncs_sub_value_String,time_granted)

			
	# Sync process
	if time_granted % deltaT == 0:
		controller_obj.sync(time_granted)

	# Advancing time and updating day, hour and minute:
	if (time_granted < (timeSim)) :
		time_granted = fncs.time_request(timeSim)
	else:
		timeSim = timeSim + deltaT
		time_granted = fncs.time_request(timeSim)
		controller_obj.day = int(time_granted / day_len)
	
	controller_obj.prevday = controller_obj.day
	#print('************************************************', flush=True)

# finalize fncs	
print ('finalizing FNCS', flush=True)
fncs.finalize()