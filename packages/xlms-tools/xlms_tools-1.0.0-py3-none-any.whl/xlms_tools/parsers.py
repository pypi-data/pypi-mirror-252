# This file is part of the xlms-tools package
#
# Copyright (c) 2023 - Topf Lab, Centre for Structural Systems Biology
# Hamburg, Germany.
#
# This module was developed by:
#   Karen Manalastas-Cantos    <karen.manalastas-cantos AT cssb-hamburg.de>

from Bio.PDB import *
import numpy as np

def extractCAcoordsfrompdb(pdbfile):
    parser = PDBParser()
    structure = parser.get_structure("test", pdbfile)
    CAcoords = np.zeros(3)
    residues = structure.get_residues()
    nres = 0
    for res in residues:
        if res.has_id("CA"):
            atom = np.asarray(res["CA"].get_coord())
            CAcoords = np.concatenate((CAcoords, atom), axis=0)
            nres += 1        
    CAcoords = np.reshape(CAcoords[3:], (nres,3))
    return CAcoords

def maxCAdist(pdbfile):
    coords = extractCAcoordsfrompdb(pdbfile)
    distmat = distancematrix(coords, coords)
    return distmat.max()
    
def distancematrix(a, b):
    distmat = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=-1)
    return distmat

def getxllist(xlmslist):
    xllist = []
    chainlist = []
    scores = []
    with open(xlmslist, 'r') as f:
        for ln in f:
            link, chains, score = parseline(ln.strip())
            #print ('parse', link, chains, score)
            if link not in xllist:
                xllist.append(link)
                scores.append(score)
            if chains not in chainlist:
                chainlist.append(chains)
    return xllist, chainlist, scores
    
def parseline(line):
    score = 0
    tmp = line.split()
    if len(tmp) > 1:    #if there's a score
        score = float(tmp[1])
        buf = tmp[0].split('|')
    else:
        buf = line.split('|')
        
    if len(buf) == 2:
        return (int(buf[0]), buf[1]), buf[1], score
    else:
        tmp = [(int(buf[0]), buf[1]), (int(buf[2]), buf[3])]
        tmp.sort(key=lambda tup: tup[1])
        return (tmp[0][0], tmp[0][1], tmp[1][0], tmp[1][1]), tmp[0][1]+tmp[1][1], score
