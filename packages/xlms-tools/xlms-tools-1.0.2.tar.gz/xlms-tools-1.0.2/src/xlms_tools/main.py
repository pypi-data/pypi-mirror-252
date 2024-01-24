# This file is part of the xlms-tools package
#
# Copyright (c) 2023 - Topf Lab, Centre for Structural Systems Biology
# Hamburg, Germany.
#
# This module was developed by:
#   Karen Manalastas-Cantos    <karen.manalastas-cantos AT cssb-hamburg.de>

import argparse
import os.path
import os
import time
from xlms_tools.score import *
from xlms_tools.depth import outputdepth
from xlms_tools.printing import *
from xlms_tools.visualization import *

def main():
    parser = argparse.ArgumentParser(description='Score protein structures by their concordance with crosslinking mass spectrometry (XL-MS) data')
    parser.add_argument('pdb', metavar='PDB', type=str, nargs='+',
                    help='PDB file/s of protein')
    parser.add_argument('-m', '--mode', type=str, choices=['score', 'depth', 'sim'], default='score',
                    help='score: compute model score with respect to XL-MS data; depth: compute residue depths; sim: simulate crosslinks and monolinks')
    parser.add_argument('-s','--score', type=str, choices=['old', 'new'], default='new',
                    help='old: use Total Residue Depth (RD) for monolinks; Matched and      Nonaccessible Crosslinks (MNXL) for crosslinks; \nnew: use Monolink Probability (MP) for monolinks, Crosslink Probability (XLP) for crosslinks')
    parser.add_argument('-l', '--list', type=str,
                    help='[score mode only] list of crosslinks and monolinks')
    parser.add_argument('-r', '--recov', type=str,
                    help='[sim mode only] recovery rate for crosslink/monolink simulation')
    parser.add_argument('--linker', type=str, choices=['BS3/DSS'], default='BS3/DSS',
                    help='Crosslinking reagent used')
    parser.add_argument('--name', type=str, default='',
                    help='Run name. Output files will use this as a base filename')
    parser.add_argument('--color', type=str, default='lightgray',
                    help='color name or hexcode recognizable by ChimeraX, to color the protein in visualization')

    args = parser.parse_args()


    printsoftwareheader()

    if args.mode == 'score':
        print ('Scoring models...')
        start = time.time()
    
        xllist, chains, scores = getxllist(args.list)
    
        # write .cxc for chimerax visualization
        if len(args.name) > 0:
            visdir = args.name
        else:
            visdir = os.path.basename(args.list)[:-4]
        if not os.path.exists(visdir):
            os.mkdir(visdir)
        cxcptr = printcxc(args.pdb, visdir=visdir, color=args.color)

        # open score output file
        f = openscorefile(chains, outname=visdir+"_scores")
    
        bestmodel = ""
        bestscore = -1000
        for i,model in enumerate(args.pdb):
            iscore = scoremodel(f, cxcptr, xllist, scores, model, i+1, visdir, args.linker)
            if iscore > bestscore:
                bestscore = iscore
                bestmodel = model
        f.close()
        cxcptr.close()
    
        print ("\n***\n\nBEST SCORING MODEL:", bestmodel)
        print (f"XLP/MP scores are in {visdir}_scores.tsv")
        print (f"Open {visdir}.cxc with ChimeraX to visualize the models with crosslinks")
        print (f"Total time elapsed: {time.time()-start:.3f}s\n")    

    elif args.mode == 'depth':
        for i in args.pdb:
            outputdepth(i)
    else:
        print("Mode '", args.mode, "' not yet supported")

    print("\nIf you use xlms-tools, please cite:")
    print("Manalastas-Cantos, K., Adoni, K. R., Pfeifer, M., Märtens, B., Grünewald, K., Thalassinos, K., & Topf, M. (2024). Modeling flexible protein structure with AlphaFold2 and cross-linking mass spectrometry. Molecular & Cellular Proteomics. https://doi.org/10.1016/j.mcpro.2024.100724\n")

if __name__ == '__main__':
    main()