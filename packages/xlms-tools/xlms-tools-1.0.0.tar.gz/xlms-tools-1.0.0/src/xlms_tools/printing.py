# This file is part of the xlms-tools package
#
# Copyright (c) 2023 - Topf Lab, Centre for Structural Systems Biology
# Hamburg, Germany.
#
# This module was developed by:
#   Karen Manalastas-Cantos    <karen.manalastas-cantos AT cssb-hamburg.de>

def printsoftwareheader():
    print("\n\033[1mxlms-tools\033[0m: a software suite for modeling protein structures\n            with crosslinking mass spectrometry data\n")

def openscorefile(chainlist, outname="xlms-scores"):
    g = open(outname+".tsv", "w")
    
    # parse xldatafile for columns
    intraxl = [i[0] for i in chainlist if len(i) == 2 and i[0]==i[1]]
    interxl = [i for i in chainlist if len(i) == 2 and i[0]!=i[1]]                
    intraxl.sort()
    interxl.sort()
    
    ## print header
    g.write(f'model\tmlscore\t')
    for i in intraxl:
        g.write(f'xl_{i}\t')
    for i in interxl:
        g.write(f'xl_{i}\t')
    g.write(f'#depth_violations\t')
    g.write(f'#max_distance_violations\t')
    g.write('ave_xl\n')
    
    return g