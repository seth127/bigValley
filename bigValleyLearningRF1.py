# python bigValleyLearningRF1.py 1 500 5 random extinct

import sys
import os

os.chdir(sys.path[0])

sys.path.append('./bvSimFiles') # Add location of python prototype to path

from bvSimLearning import *

######
## SET PARAMETERS

# number of tests for each epoch (these are averaged together before saving as a single line)
##you can turn on saving at the end of testLife() to save a separate .csv with each run in it
t = int(sys.argv[1]) # default is 3
#max number of years for each epoch
y = int(sys.argv[2]) # default is 500

# number of epochs to run
reps = int(sys.argv[3]) # default is 5

# end on first extinction?
extinct = (sys.argv[4] == 'extinct') | (sys.argv[5] == 'extinct')

# use params exactly on each rep? (vs. slightly randomizing each rep)
exact = (sys.argv[4] == 'exact') | (sys.argv[5] == 'exact')

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
    tests = t
    years = y

    #define your life forms
    if exact == True:
      wolfEn = we
      wolfRe = wr
      wolfFa = wf

      rabbitEn = re
      rabbitRe = rr
      rabbitFa = rf

      wolfNum = wn
      rabbitNum = rn
      grassNum = gn
      debrisNum = dn
    else: # if not 'exact', slightly randomize the starting values for each repitition of sim
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
    runSimLearningRF1('testData/' + str(tests) + 'x' + str(years) + 'SIMS-RF1.csv',
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
          endOnExtinction = extinct)