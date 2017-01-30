# python bigValleyLearningLM2.py 1 500 550 new

import sys
import os
import time

os.chdir(sys.path[0])

sys.path.append('./bvSimFiles') # Add location of python prototype to path

from bvSimLearning import *

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

## SET PARAMETERS

# number of tests for each epoch (these are averaged together before saving as a single line)
##you can turn on saving at the end of testLife() to save a separate .csv with each run in it
tests = int(sys.argv[1]) # default is 3
#max number of years for each epoch
years = int(sys.argv[2]) # default is 500

# number of simulations to run in total before the the program quits
reps = int(sys.argv[3]) # default is 5
### NOTE: IF STARTING ANEW, it will run 500 dumb reps 
#### and THEN start the prescribed number of learning reps

# either give it 'new' to start over or the ID code of a past trial to continue
if sys.argv[4] == 'new':
  simID = id_generator(3)
  print('STARTING ANEW ')
else:
  simID = sys.argv[4]

#
file_name = 'testData/' + str(tests) + 'x' + str(years) + 'SIMS-LM2-' + simID +'.csv'
print(file_name)

#wolf stats
we = 150 #300
wr = 200 #400
wf = 10 #20

#rabbit stats
re = 35 #70
rr = 50 #100
rf = 5 #10

#numbers of each critter
wn = 3
rn = 16
gn = 25
dn = 10

######## PARAMETERS FOR LOADING DATA AND MODELING
simCols = ['tests','years','firstExt', 'firstExtSTD', 'deadWorld', 'deadWorldSTD', 'id',
      'wolfEn',
      'wolfRe',
      'wolfFa',
      'rabbitEn',
      'rabbitRe',
      'rabbitFa',
      'wolfNum',
      'rabbitNum',
      'grassNum',
      'debrisNum']
yList = ['firstExt']
xList = ['wolfEn',
          'wolfRe',
          'wolfFa',
          'rabbitEn',
          'rabbitRe',
          'rabbitFa',
          'wolfNum',
          'rabbitNum',
          'grassNum',
          'debrisNum']

#################
## RUN THE SIM ##
#################

########
# IF STARTING ANEW, run 500 dumb reps before fitting the initial model
########
if sys.argv[4] == 'new':
    for i in range(0, 500):
        # set parameters for this run
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
        runSim(file_name,
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
              endOnExtinction = True)
    # set starting params for learning
    newStartingParams = [we,wr,wf,re,rr,rf,wn,rn,gn,dn,]
else:
    previousDF = pd.read_csv(file_name, header = None, names = simCols)
    newStartingParams = previousDF.iloc[-1][xList].tolist()

#########
# IF CONTINUING A PREVIOUS RUN, or once the intitial 500 have run,
# RUN THE LEARNING SIM
#########

for i in range(0, reps):
    # set previous starting params from the newStartingParams from the last run
    previousParams = newStartingParams
    # re-learn the starting parameters
    adjustments = learnParamsLM(file_name,
        previousParams[0],
        previousParams[1],
        previousParams[2],
        previousParams[3],
        previousParams[4],
        previousParams[5],
        previousParams[6],
        previousParams[7],
        previousParams[8],
        previousParams[9],
        xList,
        yList,
        simCols,
        incremental = True) ### THIS IS THE MAIN DIFFERENCE BETWEEN LM1 AND LM2

    # if we've reached successful stasis (10 in a row that hit 500)
    if adjustments[0] == 'END':
        print('$$$$$$$$$\n$$$$$$$$$\nSUCCESSFUL STASIS!!!')
        print('ran for ' + str(adjustments[1]) + ' years\n$$$$$$$$$\n$$$$$$$$$')
        break

    # adjust previousParams and set as newStartingParams
    newStartingParams = np.array(previousParams) + np.array(adjustments)

    # FINISH RE-LEARNING, print note
    print('%%%%%%%%\n%%%%%%%%\nRESET STARTING PARAMETERS.\nAdjustments:')
    print(adjustments)
    #print(newStartingParams)
    print('%%%%%%%%\n%%%%%%%%\n')
    #print('continuing in ...')
    #print('5'); time.sleep(1); print('4'); time.sleep(1); print('3'); time.sleep(1); print('2'); time.sleep(1); print('1'); time.sleep(1)

    # set parameters for this run
    wolfEn = max(newStartingParams[0], 100) # minimum of 100
    wolfRe = max(newStartingParams[1], round((wolfEn * 1.1), 0)) # minimum of wolfEn * 1.1
    wolfFa = max(newStartingParams[2], 5) # minimum of 5

    rabbitEn = max(newStartingParams[3], 25) # minimum of 25
    rabbitRe = max(newStartingParams[4], round((rabbitEn * 1.1), 0)) # minimum of rabbitEn * 1.1
    rabbitFa = max(newStartingParams[5], 5) # minimum of 5

    # minumum of 1 for each of these
    wolfNum = int(max(newStartingParams[6], 1))
    rabbitNum = int(max(newStartingParams[7], 1))
    grassNum = int(max(newStartingParams[8], 1))
    debrisNum = int(max(newStartingParams[9], 1))


    # RUN THIS ITERATION
    runSim(file_name,
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
          endOnOverflow = True)
    print(adjustments)

# ONCE WE REACHED SUCCESS, RUN A BIG ONE
# set parameters for this run
wolfEn = max(newStartingParams[0], 100) # minimum of 100
wolfRe = max(newStartingParams[1], round((wolfEn * 1.1), 0)) # minimum of wolfEn * 1.1
wolfFa = max(newStartingParams[2], 5) # minimum of 5

rabbitEn = max(newStartingParams[3], 25) # minimum of 25
rabbitRe = max(newStartingParams[4], round((rabbitEn * 1.1), 0)) # minimum of rabbitEn * 1.1
rabbitFa = max(newStartingParams[5], 5) # minimum of 5

# minumum of 1 for each of these
wolfNum = int(max(newStartingParams[6], 1))
rabbitNum = int(max(newStartingParams[7], 1))
grassNum = int(max(newStartingParams[8], 1))
debrisNum = int(max(newStartingParams[9], 1))

runSim(file_name,
      tests,
      5000,
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
      endOnOverflow = False,
      saveYearStats = True)
