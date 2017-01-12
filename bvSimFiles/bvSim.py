import datetime
import sys


from bvWorldEvo import *
import bvWorldEvoPlotting as bvplot
from bvLifeEvo import *

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#'file' + id_generator()


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
        endOnExtinction = True,
        showPlot = False):
    save_name = 'testData/individualEpochs/' + str(tests) + 'x' + str(years) + '-' + id_generator() + '.csv' 
    testStats = []
    for i in range(0, tests):
        #create an instance of World 
        if showPlot == False:
            bigValley = World(5)
        else:
            bigValley = bvplot.World(5)
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
          endOnExtinction=True,
          showPlot=False):
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
        endOnExtinction,
        showPlot)
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


