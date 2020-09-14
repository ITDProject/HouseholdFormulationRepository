Installation Instructions

1. Install Python

	Python can be installed using any of the following choices:

	Choice 1: Install Python using the Anaconda Distribution, available for downloading from https://www.anaconda.com/distribution/ Check https://docs.anaconda.com/anaconda/install/windows/ for installation instructions.

	Choice 2: Install Python using the Miniconda installer following the instructions given at https://conda.io/miniconda.html Note: Pay particular attention to how the conda package manager is used to install various required modules such as numpy.

	Choice 3: Install standard Python from https://www.python.org/ . The optional ‘pip’ is needed to install modules such as numpy.

	Note: The current study used the Miniconda installer from https://docs.conda.io/en/latest/miniconda.html to install Python (V3) at the location C:Miniconda3

	Add C:/Miniconda3 to path (python.exe is located at C:Miniconda3) to recognize Python from cmd (or powershell) else only conda prompt knows Python.

	Add C:/Miniconda3/Scripts and C:Miniconda3/Library/bin to use conda to install packages.

	Verify installation using "Python --version" command prompt.

	Verify access to pip and conda (by typing pip/conda).

	To install modules, use 'pip install ModuleName' or 'conda install ModuleName'.

	To uninstall modules, use 'pip uninstall ModuleName' or 'conda uninstall ModuleName'.

	Note: For “version” command line prompts, Python requires the use of a double hyphen “- -version”.

2. Install GridLAB-D with FNCS as prerequisite by following the instructions at http://gridlab-d.shoutwiki.com/wiki/Building_GridLAB-D_on_Windows_with_MSYS2#Building_GridLAB-D_from_Source
