# xlms-tools

## Description
xlms-tools is a set of command line tools to apply crosslinking mass spectrometry (XL-MS) data to protein structure models.

## Setting up xlms-tools
After downloading or cloning this repository, download dependencies by running the following from the project directory:
```bash
$ pip3 install -r requirements.txt
```

## Using xlms-tools
Currently, xlms-tools can be run in two modes. The first is to score how well a protein structure model agrees with XL-MS data, specified as a list crosslinks and monolinks derived from a XL-MS experiment.


### To score how well a protein structure agrees with XL-MS data
1. Format crosslinks and monolinks into a text file with the following format:


2. Score protein structure model/s:
```bash
$ python xlms-tools.py -m score -l [list of crosslinks and/or monolinks] [PDB file]
```

## Citations
When using xlms-tools, please cite:
Manalastas-Cantos, K. et al. (2023) Modeling flexible protein structure with AlphaFold2 and cross-linking mass spectrometry. BioRxiv. https://doi.org/10.1101/2023.09.11.557128 
