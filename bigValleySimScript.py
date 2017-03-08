# example call: python bigValleySimScript.py 500 5 plot

import sys
import os

os.chdir(sys.path[0])

sys.path.append('./bvSimFiles') # Add location of python prototype to path

from bvSim import *

######
## SET PARAMETERS

#max number of years for each epoch
y = int(sys.argv[1]) # default is 500

# number of epochs to run
reps = int(sys.argv[2]) # default is 5

# show plots each turn
plot = (sys.argv[3] == 'plot') # if you don't want to plot, just put 'no' as argv[4]


#wolf stats
we = 300
wr = 400
wf = 20

#rabbit stats
re = 70
rr = 100
rf = 10

#numbers of each critter
wn = 3
rn = 16
gn = 25
dn = 10

#####
## RUN THE SIM

for i in range(0, reps):
    #define test parameters
    tests = 1
    years = y

    #define your life forms
    wolfEn = int(we + (np.random.randn(1)[0] * 10))
    wolfRe = int(wr + (np.random.randn(1)[0] * 15))
    if wolfRe < wolfEn * 1.1:
      wolfRe = wolfEn * 1.1
    wolfFa = max(int(wf + (np.random.randn(1)[0] * 5)), 5) # minimum of 5

    rabbitEn = int(re + (np.random.randn(1)[0] * 10))
    rabbitRe = int(rr + (np.random.randn(1)[0] * 10))
    if rabbitRe < rabbitEn * 1.1:
      rabbitRe = rabbitEn * 1.1
    rabbitFa = max(int(rf + (np.random.randn(1)[0] * 5)), 5) # minimum of 5

    # minumum of 1 for each of these
    wolfNum = max(int(wn + (np.random.randn(1)[0] * 3)), 1)
    rabbitNum = max(int(rn + (np.random.randn(1)[0] * 5)), 1)
    grassNum = max(int(gn + (np.random.randn(1)[0] * 10)), 1)
    debrisNum = max(int(dn + (np.random.randn(1)[0] * 10)), 1)


    # RUN THE SIM
    runSim('testData/' + str(tests) + 'x' + str(years) + 'SIMS.csv',
          tests,
          years,
          wolfEn,
          wolfRe,
          wolfFa,
          rabbitEn,
          rabbitRe,
          rabbitFa,
          wolfNum,
          rabbitNum,
          grassNum,
          debrisNum,
          endOnExtinction = True,
          showPlot = plot)