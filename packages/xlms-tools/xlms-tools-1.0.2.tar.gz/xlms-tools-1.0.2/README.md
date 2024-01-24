# xlms-tools

## Description
xlms-tools is a set of command line tools to apply crosslinking mass spectrometry (XL-MS) data to protein structure models.


## Setting up xlms-tools
xlms-tools can be installed directly from PyPI, as follows:
```bash
$ pip install xlms-tools
```
Or alternatively, by downloading or cloning this repository, and running the following from the project directory:
```bash
$ pip install dist/xlms_tools-1.0.2-py3-none-any.whl
```

## Using xlms-tools
Currently, xlms-tools can be run in two modes. The first is to score how well a protein structure model agrees with XL-MS data, which is specified as a list crosslinks and monolinks derived from a XL-MS experiment. The second mode is to compute the depths of individual residues in protein structures.

### To score how well a protein structure agrees with XL-MS data
1. First, format crosslinks and monolinks into a text file with the following format:
```bash
98|A|147|A 5.1		#
72|A|161|A 4.3		# crosslinks: <residue # of a>|<chain of a>|<res#, b>|<chain, b> <occupancy>
72|A|180|A 2.7		#
35|A 1.9	#		
137|A 5.3	# monolinks: <residue # of a>|<chain of a> <occupancy>
97|A 2.6	#
```
where each line corresponds to either a crosslink or a monolink. Optionally, a numerical value can be appended at the end of each line, corresponding to the occupancy of each individual monolink or crosslink. For a detailed discussion on occupancy, please refer to the paper.

2. Score protein structure model/s:
To compute the crosslink (XLP) and monolink probability (MP) scores of one or more protein structures, execute the following in the command line:

```bash
$ xlms-tools -m score -l [list of crosslinks and/or monolinks] [PDB file/s] --name [name of run]
```

Example files can be found in the tests/ directory. You can navigate to the tests/ directory and run the scoring, as follows:
```bash
$ xlms-tools -m score -l xlms_data_qtv.txt model_1.pdb --name withoccupancy_m1 #score model_1.pdb
$ xlms-tools -m score -l xlms_data_qtv.txt model_*pdb --name withoccupancy_all #score all models
```

3. The outputs include (a) a tab-separated (.tsv) file containing the scores, which can be viewed using a spreadsheet editor, as well as (b) a ChimeraX command (.cxc) file, which can be executed by double-clicking the .cxc file (given a working installation of ChimeraX). In the ChimeraX visualization, crosslinks and monolinks are color-coded: blue means that the spanning distance of the crosslink, or the residue depth of the monolinked residue, are well within the cutoff, red stands for a maximum distance violation (for crosslinks) or a maximum depth violation (for monolinks), while yellow is within the cutoff, but approaching it. The distance cutoffs are currently only defined for BS3/DSS, but will be expanded in future releases.

	<img src="./imgs/chimerax.png">


### To compute residue depths in a protein structure
1. Run the following command:
```bash
$ xlms-tools -m depth [PDB file/s]
```
Example files can be found in the tests/ directory. You can navigate to the tests/ directory and run the depth computations, as follows:
```bash
$ xlms-tools -m depth model_1.pdb #compute residue depths for model_1.pdb
$ xlms-tools -m depth model_*pdb #compute residue depths for all models
```

2. Each line of the output file (.depth file) corresponds to one residue 
```bash
# format: <residue number>:<chain>	<amino acid>	<residue depth in Å>
A:26	LYS	4.317777777777779	
A:27	LEU	4.608300983124843
A:28	VAL	5.739574753218949
A:29	VAL	8.684474490011493
A:30	ALA	8.926983412282244
A:31	THR	8.0268463237516
A:32	ASP	6.0348264453008715
A:33	THR	4.487608873498731
A:34	ALA	4.371281572999748
A:35	PHE	5.2527378512712275
A:36	VAL	5.226420625104608
A:37	PRO	6.844806528409208
...
```
 
## Citations
When using xlms-tools, please cite:
Manalastas-Cantos, K., Adoni, K. R., Pfeifer, M., Märtens, B., Grünewald, K., Thalassinos, K., & Topf, M. (2024). Modeling flexible protein structure with AlphaFold2 and cross-linking mass spectrometry. Molecular & Cellular Proteomics. https://doi.org/10.1016/j.mcpro.2024.100724
