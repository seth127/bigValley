import datetime
import sys


from bvWorldEvoArchiving import *
from bvLifeEvo import *

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#'file' + id_generator()


def testLife(years, 
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
        endOnExtinction = True):
    
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
    
    #now run
    testStats = bigValley.archivalTime(years, endOnExtinction = endOnExtinction)
    return testStats
    '''
    # save each run to a csv
    testDF = pd.DataFrame(testStats, columns=['firstExt', 'deadWorld', 'id'])

    #return testStats
    print(testDF)
    return testDF
    '''



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
          endOnExtinction=True):
    start=datetime.datetime.now()
    #file_name = 'data/' + str(tests) + 'x' + str(years) + '-' + id_generator() + '.csv' 
    testStats = testLife(years, 
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
        testStats[0], # first extinction
        testStats[1], # dead world
        testStats[2], # id
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
    print("%d years logged in " % len(open(file_name).readlines()) + file_name)
    ##print "%d lines in your choosen file" % len(file.readlines())

    #close the file
    file.close()
    print(datetime.datetime.now()-start)
    print('%%%%%%%%')


