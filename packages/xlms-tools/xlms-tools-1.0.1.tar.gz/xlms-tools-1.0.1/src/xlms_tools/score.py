# This file is part of the xlms-tools package
#
# Copyright (c) 2023 - Topf Lab, Centre for Structural Systems Biology
# Hamburg, Germany.
#
# This module was developed by:
#   Karen Manalastas-Cantos    <karen.manalastas-cantos AT cssb-hamburg.de>

from Bio.PDB import *
from xlms_tools.depth import *
from xlms_tools.parsers import *
from xlms_tools.visualization import *
import numpy as np
import time


def scoremodel(ptr, cxcptr, xlmslist, weights, pdbfile, modelnum, visdir, linker):
    scores = {}
    
    # open pdbfile
    print ("MODEL:", pdbfile)
    start = time.time()
    maxdist = maxCAdist(pdbfile)
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pdbfile[:-4], pdbfile)
    
    # make pseudobond file to show crosslinks
    g, m, b = createpb(pdbfile, visdir)
    
    # compute residue depths
    depths, _ = computedepth(structure)
    maxdep = max(depths.values())

    # score each link
    totalmlweight = 0
    totalxlweight = 0
    ndepviols = 0
    ndistviols = 0
    for link, weight in zip(xlmslist, weights):
        if len(link) < 4:
            chainids = link[1]
            totalmlweight += weight
        else:
            chainids = link[1]+link[3]
            totalxlweight += weight
        curscore, depviol, distviol = scorelink(link, structure, modelnum, g, m, b, cxcptr, depths=depths, maxdep=maxdep, maxdist=maxdist, linker=linker)
        if depviol:
            ndepviols += 1
        if distviol:
            ndistviols += 1
            
        if weight != 0:
            curscore *= weight
        if curscore != None:
            if chainids in scores:
                scores[chainids].append(curscore)
            else:
                scores[chainids] = [curscore]
    
    # close pseudobond files
    g.close()
    m.close()
    b.close()

    intraxlscores = []
    interxlscores = []
    mlscores = []
    avexlscore = 0
    nxls = 0
    
    for key in scores:
        if len(key) == 1:
            mlscores += scores[key]
        else:
            nxls += len(scores[key])
            avexlscore += sum(scores[key])
            if key[0] == key[1]: #intraxl
                intraxlscores.append((key[0], sum(scores[key])/len(scores[key])))
            else:
                interxlscores.append((key, sum(scores[key])/len(scores[key])))
    intraxlscores.sort()
    interxlscores.sort()
            
    ## print results
    ptr.write(f'{os.path.basename(pdbfile)[:-4]}\t')
    if len(mlscores) > 0:
        if totalmlweight == 0:
            ptr.write(f'{sum(mlscores)/len(mlscores):.3f}\t')
        else:
            ptr.write(f'{sum(mlscores)/totalmlweight:.3f}\t')
    else:
        ptr.write('--\t')
    for _, score in intraxlscores:
    	ptr.write(f'{score:.3f}\t')
    for _, score in interxlscores:
    	ptr.write(f'{score:.3f}\t')
    
    ptr.write(f'{ndepviols}\t')
    ptr.write(f'{ndistviols}\t')

    if nxls > 0:
        if totalxlweight == 0:
            ptr.write(f'{avexlscore/nxls:.3f}')
        else:
            ptr.write(f'{avexlscore/totalxlweight:.3f}')            
    ptr.write('\n')
    
    print (f"-- Computing XLP/MP scores: {time.time()-start:.3f}s")
    
    if nxls > 0:
        if totalxlweight == 0:
            return avexlscore/nxls
        else:
            return avexlscore/totalxlweight
    elif len(mlscores) > 0:
        if totalmlweight == 0:
            return sum(mlscores)/len(mlscores)
        else:
            return sum(mlscores)/totalmlweight

def scorelink(link, structure, modelid, gptr, mptr, bptr, cxcptr, depths=None, maxdep=None, maxdist=None, linker=None):
    score = 0
    depthviol = False
    distviol = False
    
    if len(link) == 2:   # is a monolink
        if depths != None:
            pos = link[1]+':'+str(link[0])
            if pos in depths:
                score = monolinkscore(depths[pos], maxdep)
            else:   # monolink not in pdb
                return None, depthviol, distviol
            
            # add visualization of monolink to ChimeraX command file
            cxcptr.write(f'show #{modelid}/{pos} atoms\n')
            if depths[pos] <= 6.25:
                cxcptr.write(f'color #{modelid}/{pos} blue atoms\n')
            else:
                cxcptr.write(f'color #{modelid}/{pos} red atoms\n')
                depthviol = True
                
    else: # is a crosslink
        if structure[0][link[1]].has_id(link[0]) and structure[0][link[3]].has_id(link[2]):
            atom1 = structure[0][link[1]][link[0]]["CA"]
            atom2 = structure[0][link[3]][link[2]]["CA"]
            dist = atom1 - atom2
        else:   # crosslink not in pdb
            return None, depthviol, distviol

        if (depths != None): # use depth info if available, else just use euclidean distance
            tag1 = link[1]+':'+str(link[0])
            tag2 = link[3]+':'+str(link[2])
            if (tag1 in depths) and (tag2 in depths):            
                score = crosslinkscore(dist, maxdist, dep1=depths[tag1], dep2=depths[tag2], maxdep=maxdep, linker=linker)
                #score = crosslinkscore(dist, maxdist, linker=linker)
            else:
                score = crosslinkscore(dist, maxdist, linker=linker)
        else:
            score = crosslinkscore(dist, maxdist, linker=linker)
        
        # print into pseudobond file for visualization
        gthresh, maxdist = distancethresholds(linker) 
        if dist <= gthresh:
            gptr.write(f'#{modelid}/{link[1]}:{link[0]}@ca #{modelid}/{link[3]}:{link[2]}@ca\n')
        elif dist <= maxdist:
            mptr.write(f'#{modelid}/{link[1]}:{link[0]}@ca #{modelid}/{link[3]}:{link[2]}@ca\n')
        else:
            bptr.write(f'#{modelid}/{link[1]}:{link[0]}@ca #{modelid}/{link[3]}:{link[2]}@ca\n')
            distviol = True

    return score, depthviol, distviol

def distancethresholds(linker):
    # for BS3/DSS, to add more later
    good = 21
    maxdist = 33
    return good, maxdist
        
def monolinkprob(depth):
    tagcoefs = np.array([1.20875756e+03, 5.31961163e+00, 6.43465155e-04])
    lyscoefs = np.array([4.44470936e+02, 4.65135510e+00, 1.69863402e-03])
    if func(depth, *lyscoefs) > 0:
        return func(depth, *tagcoefs)/func(depth, *lyscoefs)
    else:
        return 0

def func(x, a, b, c):
    return (a * (x**-b)) + c


mlcutoff = 15   # residue depth cutoff for monolinks

def monolinkscore(depth, maxdepth):
    
    score = monolinkprob(depth)
    if depth >= mlcutoff:
        score = -(depth/maxdepth)
    return score
    
def edprob(dist, linker = 'BS3/DSS'):
        
    if linker == 'BS3/DSS':    # default situation, BS3 or DSS
        mu = 16.3
        std = 6.9
        return 1/(1+np.exp(0.33*dist-7))    # this is the best from the benchmark
    elif linker == 'DSSO':
        mu = 15.4
        std = 7.3
        return 1/(1+np.exp(0.33*dist-5.75))    # fitted to DSSO distribution
    else:
        print ("No information about linker. Using distance distribution for BS3/DSS")
        mu = 16.3
        std = 6.9
        return 1/(1+np.exp(0.33*dist-7))    # this is the best from the benchmark
        
def crosslinkscore(dist, maxdist, dep1=None, dep2=None, maxdep=None, linker='BS3/DSS'):
    xlcutoff = {'BS3/DSS':33}
    
    if dep1 == None:
        score = edprob(dist, linker=linker)
        if dist > xlcutoff[linker]: # apply distance penalty
            score = -(dist/maxdist)
    else:
        score = monolinkprob(dep1)*monolinkprob(dep2)*edprob(dist, linker=linker)
        if dep1 >= mlcutoff:
            score = -dep1/(4*maxdep)
        if dep2 >= mlcutoff:
            score = -dep2/(4*maxdep)
        if dist > xlcutoff[linker]:
            score = -dist/(2*maxdist)
    return score