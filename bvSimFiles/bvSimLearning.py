import datetime
import sys
import pandas as pd
import numpy as np


from bvWorldEvo import *
from bvLifeEvo import *

import string
import random

from sklearn.ensemble import RandomForestRegressor

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#'file' + id_generator()


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

def testLife(tests, 
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
        endOnExtinction = False):
    save_name = 'testData/individualEpochs/' + str(tests) + 'x' + str(years) + '-' + id_generator() + '.csv' 
    testStats = []
    for i in range(0, tests):
        #create an instance of World 
        bigValley = World(5)
        print(datetime.datetime.now())

        #define your life forms
        newLife(Predator('wolf', energy = wolfEn, repro = wolfRe, fatigue = wolfFa), 
                bigValley, 'wolf') # adding in the parameters from above
        newLife(Prey('rabbit', energy = rabbitEn, repro = rabbitRe, fatigue = rabbitFa), 
                bigValley, 'rabbit') # adding in the parameters from above
        newLife(Plant('grass'), bigValley, 'grass')
        newLife(Rock('debris'), bigValley, 'debris')

        #now populate the world
        populate(bigValley, 'wolf', wolfNum)
        populate(bigValley, 'rabbit', rabbitNum)
        populate(bigValley, 'grass', grassNum)
        populate(bigValley, 'debris', debrisNum)
        
        #now run the test
        test = bigValley.silentTime(years, yearlyPrinting = True, endOnExtinction = endOnExtinction)
        testStats.append(test)
        print('testStats ' + str(i) + ' ::: ' + str(testStats))
        
        # save each epoch to a csv (instead of the average of each test)
        testDF = pd.DataFrame(testStats, columns=['firstExt', 'deadWorld', 'id'])
        #testDF.to_csv(save_name, index=False) # saves a csv for each epoch

    #return testStats
    print(testDF)
    return testDF



# function to count the lines in a file (for seeing how many epochs have been logged)
'''
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    	#return i + 1
    	print(str(fname) + ' is now ' + str(i + 1) + ' lines long.')
'''
 
def loadSimData(file_name):
    cols = ['tests','years','firstExt', 'firstExtSTD', 'deadWorld', 'deadWorldSTD', 'id',
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
    df = pd.read_csv('testData/1x500SIMS.csv', header = None, names = cols)

def runSim(file_name,
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
          endOnExtinction=False):
    start=datetime.datetime.now()
    #file_name = 'data/' + str(tests) + 'x' + str(years) + '-' + id_generator() + '.csv' 
    testDF = testLife(tests, 
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
        endOnExtinction)
    thisSim = [
        tests,
        years,
        round(np.mean(testDF['firstExt']), 2), # first extinction
        round(np.std(testDF['firstExt']), 2),
        round(np.mean(testDF['deadWorld']), 2), # dead world
        round(np.std(testDF['deadWorld']), 2),
        ','.join(testDF['id'].tolist()),
        wolfEn,
        wolfRe,
        wolfFa,
        rabbitEn,
        rabbitRe,
        rabbitFa,
        wolfNum,
        rabbitNum,
        grassNum,
        debrisNum]
    print(thisSim)
    #open the file
    file = open(file_name, "a")
    #write the new line
    file.write(str(thisSim).strip('[]') + '\n')
    #print the number of lines logged to the file
    #file_len(file_name)
    print("%d lines in your choosen file" % len(open(file_name).readlines()))
    ##print "%d lines in your choosen file" % len(file.readlines())

    #close the file
    file.close()
    print(datetime.datetime.now()-start)
    print('%%%%%%%%')


def runSimLearningRF1(file_name, 
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
          endOnExtinction=False, optsNum=20):
    start=datetime.datetime.now()
    #file_name = 'data/' + str(tests) + 'x' + str(years) + '-' + id_generator() + '.csv' 
    
    ####### DO THE LEARNING

    # get the latest sim data
    simDF = pd.read_csv(file_name, header = None, names = simCols)

    # train the model
    rfModel=RandomForestRegressor(n_estimators=300,
                            max_depth=None, 
                            max_features=.8,
                            min_samples_split=1,
                            #random_state=0,
                            n_jobs=-1)

    rfModel.fit(simDF[xList], np.array(simDF[yList]).ravel())

    # get options
    xs = []
    for i in range(0,optsNum):
        we = int(wolfEn + (np.random.randn(1)[0] * 10))
        wr = int(wolfRe + (np.random.randn(1)[0] * 15))
        if wr < we * 1.1:
            wr = we * 1.1
        wf = max(int(wolfFa + (np.random.randn(1)[0] * 5)), 5) # minimum of 5

        re = int(rabbitEn + (np.random.randn(1)[0] * 10))
        rr = int(rabbitRe + (np.random.randn(1)[0] * 10))
        if rr < re * 1.1:
            rr = re * 1.1
        rf = max(int(rabbitFa + (np.random.randn(1)[0] * 5)), 5) # minimum of 5

        # minumum of 1 for each of these
        wn = max(int(wolfNum + (np.random.randn(1)[0] * 3)), 1)
        rn = max(int(rabbitNum + (np.random.randn(1)[0] * 5)), 1)
        gn = max(int(grassNum + (np.random.randn(1)[0] * 10)), 1)
        dn = max(int(debrisNum + (np.random.randn(1)[0] * 10)), 1)
        xs.append([we, wr, wf, re, rr, rf, wn, rn, gn, dn])

    optsDF = pd.DataFrame(xs, columns = xList)

    # predict the best of the options
    optsDF['preds'] = rfModel.predict(optsDF)
    winner = optsDF[optsDF.preds == max(optsDF.preds)]

    ####### RUN THE SIM

    testDF = testLife(tests, 
        years, 
        int(winner['wolfEn']),
        int(winner['wolfRe']),
        int(winner['wolfFa']),
        int(winner['rabbitEn']),
        int(winner['rabbitRe']),
        int(winner['rabbitFa']),
        int(winner['wolfNum']),
        int(winner['rabbitNum']),
        int(winner['grassNum']),
        int(winner['debrisNum']),
        endOnExtinction)
    thisSim = [
        tests,
        years,
        round(np.mean(testDF['firstExt']), 2), # first extinction
        round(np.std(testDF['firstExt']), 2),
        round(np.mean(testDF['deadWorld']), 2), # dead world
        round(np.std(testDF['deadWorld']), 2),
        ','.join(testDF['id'].tolist()),
        int(winner['wolfEn']),
        int(winner['wolfRe']),
        int(winner['wolfFa']),
        int(winner['rabbitEn']),
        int(winner['rabbitRe']),
        int(winner['rabbitFa']),
        int(winner['wolfNum']),
        int(winner['rabbitNum']),
        int(winner['grassNum']),
        int(winner['debrisNum']), int(winner['preds'])]
    print(thisSim)
    print('$$$$$\n PREDICTED FirstExt: ' + str(int(winner['preds'])) + '\n$$$$$')
    #open the file
    file = open(file_name, "a")
    #write the new line
    file.write(str(thisSim).strip('[]') + '\n')
    #print the number of lines logged to the file
    #file_len(file_name)
    print("%d lines in your choosen file" % len(open(file_name).readlines()))
    ##print "%d lines in your choosen file" % len(file.readlines())

    #close the file
    file.close()
    print(datetime.datetime.now()-start)
    print('%%%%%%%%')


