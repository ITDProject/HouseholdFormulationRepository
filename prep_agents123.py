#	Copyright (C) 2017 Battelle Memorial Institute
import sys
import json
from writeRegistration123 import writeRegistration123
NDsystems = int(sys.argv[2])
auctions, controllers = writeRegistration123(sys.argv[1], NDsystems)

print ("launch_agents.sh executes", 2 + len (controllers), "processes")

want_logs = False

if want_logs:
	prefix = "(export FNCS_FATAL=NO && export FNCS_LOG_STDOUT=yes && exec"
else:
	prefix = "(export FNCS_FATAL=NO && exec"
suffix_auc = "&> auction.log &)"
suffix_gld = "&> gridlabd.log &)"

metrics = sys.argv[1]

for i in range(NDsystems):
	op = open(sys.argv[1] +"_FNCS_Config.txt", "w")
	print ("publish \"commit:network_node.distribution_load -> distribution_load\";", file=op)
	print ("publish \"commit:network_node.distribution_real_energy -> distribution_energy\";", file=op)
	for key, value in controllers.items():
		arg = value['controller_information']['houseName']
		MeterArg = 'triplex_meter' + arg.split('house')[1]
		TriplexNodeArg = 'triplex_node' + arg.split('house')[1]
		
		print ("publish \"commit:" + arg + ".system_mode -> " + arg + "/system_mode\";", file=op)
		
		print ("publish \"commit:" + arg + ".Qi -> " + arg + "/Qi\";", file=op)
		print ("publish \"commit:" + arg + ".solar_gain -> " + arg + "/solar_gain\";", file=op)
		print ("publish \"commit:" + arg + ".outdoor_temperature -> " + arg + "/outdoor_temperature\";", file=op)
		print ("publish \"commit:" + arg + ".outdoor_rh -> " + arg + "/outdoor_rh\";", file=op)
		print ("publish \"commit:" + MeterArg + ".voltage_12 -> " + MeterArg + "/voltage_12\";", file=op)
		
		print ("publish \"commit:" + arg + ".hvac_load -> " + arg + "/hvac_load\";", file=op)
		
		print ("subscribe \"precommit:" + arg + ".system_mode <- controller_" + key + "/gridlabdSimulator"+str(i+1)+"_system_mode\";", file=op)
		houseNumber = arg.split("_")
	op.close()