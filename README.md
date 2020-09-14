# HouseholdFormulationRepository

Currently, this repository is only supported on Windows Operating System.

Steps involved in execution:

	1. Generate distribution system feeder populated with households with the choice of 'Household Type' by executing the following command
		python IEEE123_glm_yaml_bat_writer.py NDistSys Mix Type
		The above commands depend on the following user-specified parameters: 
			NDistSys - The number of distribution systems that are handled by the IDSO
			Mix - Represents if the chosen households are a mix of different structure types or single structure type
				0 - A single structure type, set by input parameter 'Type' described below, is chosen to populate the distribution system feeder. 
				1 - A mix of structure types Low, Medium, High are used to populate the distribution system feeder
			Type - Represents household's structure quality type; 
				1 - Low Structure Quality Type
				2 - Medium Structure Quality Type
				3 - High Structure Quality Type
		(Example: python IEEE123_glm_yaml_bat_writer.py 1 0 2)
    
	2. Generate required additional files by executing the following command
		python prep_agents123.py FileName NDistSys 
		The above commands depend on the following user-specified parameters: 
			FileName - The name of the distribution feeder generated in the above step (do not include .glm extension)
			NDistSys - The number of distribution systems that are handled by the IDSO
		(Example: python prep_agents123.py IEEEModified1 1)  
    		
		Outcomes: FNCS configuration file and json registration files for IDSO and households
			Generated FNCS configuration txt file is needed for object fncs of main .glm file
				It contains subscriptions and publish items
			Json files for IDSO and households
				IDSO json file contains needed input information for the IDSO 
				Household json file contains household specific information (household attributes)
	
	3. Set the following parameters in the runDSO.bat/runITD.bat
		NDay - Number of days the simulation needs to be carried out
		NHour - Number of additional hours the simulation needs to be carried out after the simulation is run for NDay
		deltaT - Length (seconds) of each control-step of the Five-Step TES design
		NoOfHouses - Number of households connected to the distribution system feeder
		NDsystems - Number of distribution systems monitored by the IDSO
		C - Choose an appropriate case; 
			Set C to 0 for generating test case outcomes with a flat retail price
				Also set FRP(cents/kWh) to user specified retail price 
			Set C to 1 for generating test case outcomes for 'Test Case 2: IDSO Peak Load Reduction Capabilities'
				Also set PL(kW) and TPLR(kW) to user specified values
			Set C to 2 for generating test case outcomes for 'Test Case 3: IDSO Load Matching Capabilities'
				Also set RefLoad
		apidir - Set the path of HouseholdFormulationRepository folder to this parameter
	
	4. Run all the distribution system processes by executing the following command
		runIDSO.bat
