#!/usr/bin/python
from __future__ import division
import math             
import numpy as np
from multiprocessing import Pool

# define calculate function
def Wq_cal(frame):
    Wq_frame, sinsum = [0]*bin_num, [0]*bin_num
    point = points[frame]
    for i in range(N_tot):
        p1 = point[i]
        for j in range(i+1, N_tot):
            p2 = point[j]
            rij = math.sqrt(pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2)+pow(p1[3]-p2[3],2))
            for k in range(bin_num):
                q = dq*(k+1)
                sinsum[k] = sinsum[k] + math.sin(q*rij)/(q*rij)
    for i in range(bin_num):
        Wq_frame[i] = sinsum[i]/N_tot
    return Wq_frame

# definite varibles
nframe = 10
qmax = 14
dq = 0.02
bin_num = int(qmax/dq)

# read all the points
with open('intraCF.xyz', 'r') as f:
    lines = f.readlines()
N_tot = int(lines[0])
points = []
part_num = [0]*nframe
for i in range(nframe):
    m = (N_tot+2)*i+2
    n = m+N_tot
    point = []
    for line in lines[m:n]:
        l = line.split()
        l[0] = str(l[0])
        l[1] = float(l[1])
        l[2] = float(l[2])
        l[3] = float(l[3])
        point.append(l)
        part_num[i] += 1
    points.append(point)

# multiprocess to calculate Sq for each frame
frames = []
for i in range(nframe):
    frames.append(i)
mp = Pool(processes=10)
Wq_all = mp.map(Wq_cal, frames)
mp.close()
mp.join()

Wq = []
for bin_i in range(bin_num):
    Wq_i = []
    for i in range(nframe):
        Wq_i.append(Wq_all[i][bin_i])
    Wq.append(Wq_i)

with open('intraCF.dat','w') as f:
    for bin_i in range(bin_num):
        Wq_aver = np.mean(Wq[bin_i])
        Wq_std = np.std(Wq[bin_i], ddof=1)
        print >> f, (bin_i+1)*dq, Wq_aver*2+1.0, Wq_std