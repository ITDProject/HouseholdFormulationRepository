# HouseholdFormulationRepository

The code/data in this repository are provided in support of Ref. [1], below, prepared as part of our Integrated Transmission and Distribution (ITD) project. Details about this project can be found at http://www2.econ.iastate.edu/tesfatsi/ITDProjectHome.htm

The developers of the code are Swathi Battula and Leigh Tesfatsion, with early assistance from Rohit Reddy Takkala.

[1] Swathi Battula, Leigh Tesfatsion, and Zhaoyu Wang (2020),  "A Customer-Centric Approach to Bid-Based Transactive Energy System Design,” *IEEE Transactions on Smart Grid* 11(6), pp. 4996-5008. DOI: 10.1109/TSG.2020.3008611. Working paper available at: https://lib.dr.iastate.edu/econ_workingpapers/75

Currently, the code provided in this repository is only supported on a Windows operating system.

Installation Instructions:

1. Install Python
    
   Python can be installed using any of the following choices:
    
   Choice 1: Install Python using the Anaconda Distribution, available for downloading from https://www.anaconda.com/distribution/
   Check https://docs.anaconda.com/anaconda/install/windows/ for installation instructions. 

   Choice 2: Install Python using the Miniconda installer following the instructions given at https://conda.io/miniconda.html 
   Note: Pay particular attention to how the conda package manager is used to install various required modules such as numpy. 

   Choice 3: Install standard Python from https://www.python.org/ . The optional ‘pip’ is needed to install modules such as numpy.
	
   Note: The current study used the Miniconda installer from https://docs.conda.io/en/latest/miniconda.html to install Python (V3) at the location 	
   C:\Miniconda3

   Add C:/Miniconda3 to path (python.exe is located at C:\Miniconda3) to recognize Python from cmd (or powershell) else only conda prompt knows Python.
	
   Add C:/Miniconda3/Scripts and C:Miniconda3/Library/bin to use conda to install packages.

   Verify installation using "Python --version" command prompt.  
	
   Verify access to pip and conda (by typing pip/conda).
	
   To install modules, use 'pip install ModuleName' or 'conda install ModuleName'.
	
   To uninstall modules, use 'pip uninstall ModuleName' or 'conda uninstall ModuleName'.

   Note: For “version” command line prompts, Python requires the use of a double hyphen “- -version”.

2. Install GridLAB-D with FNCS as prerequisite by following the instructions at
   http://gridlab-d.shoutwiki.com/wiki/Building_GridLAB-D_on_Windows_with_MSYS2#Building_GridLAB-D_from_Source


Steps involved in execution:

1. Generate distribution system feeder populated with households with the choice of 'Household Type' by executing the following:

   python IEEE123_glm_yaml_bat_writer.py NDistSys Mix Type
   
   The above commands depend on the following user-specified parameters: 
   
   NDistSys - The number of distribution systems that are handled by the IDSO
   
   Mix - Represents if the chosen households are a mix of different structure types or single structure type;
   
   Mix is set to 0: A single structure type, set by input parameter 'Type' described below, is chosen to populate the distribution system feeder;
   
   Mix is set to 1: A mix of structure types Low, Medium, High are used to populate the distribution system feeder;
	 
   Type - Represents household's structure quality type; 
   
   Set Type to 1 for Low Structure Quality Type;
   
   Set Type to 2 for Medium Structure Quality Type;
   
   Set Type to 3 for High Structure Quality Type;
   
   (Example usage: python IEEE123_glm_yaml_bat_writer.py 1 0 2)
    
2. Generate required additional files by executing the following command:
   
   python prep_agents123.py FileName NDistSys 
   
   The above commands depend on the following user-specified parameters: 
   
   FileName - The name of the distribution feeder generated in the above step (do not include .glm extension)
   
   NDistSys - The number of distribution systems that are handled by the IDSO
   
   (Example usage: python prep_agents123.py IEEEModified1 1)  
    		
   Outcomes: FNCS configuration txt file and json registration files for IDSO and households.
   FNCS configuration txt file contains needed input information for configuring GridLAB-D subscriptions and publications. IDSO json file contains needed input information for the IDSO and Household json file contains household specific information (household attributes).
	
3. Set the following parameters in the runIDSO.bat
   
   NDay - Number of days the simulation needs to be carried out
   
   NHour - Number of additional hours the simulation needs to be carried out after the simulation is run for NDay
   
   deltaT - Length (seconds) of each control-step of the Five-Step TES design
   
   NoOfHouses - Number of households connected to the distribution system feeder
   
   NDSystems - Number of distribution systems monitored by the IDSO
   
   C - Choose an appropriate case; 
   
   Set C to 0 for generating test case outcomes with a flat retail price. Also set FRP(cents/kWh) to user specified retail price 
   
   Set C to 1 for generating test case outcomes for 'Test Case 2: IDSO Peak Load Reduction Capabilities'. Also set PL(kW) and TPLR(kW) to user specified values
   
   Set C to 2 for generating test case outcomes for 'Test Case 3: IDSO Load Matching Capabilities'. Also set RefLoad
   
   apidir - Set the path of HouseholdFormulationRepository folder to this parameter
	
4. Run all the distribution system processes by executing the following command:
   runIDSO.bat
