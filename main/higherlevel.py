
__author__ = 'michaelbinger'

# This will combine RFC methods with some powerful filtering methods

from time import time, clock
starttime = time()
import csv as csv
import numpy as np
import scipy
from numpy import *
from sklearn.ensemble import RandomForestClassifier
from predictions import genderpred, f3sm12pred, newpred, predicttrain, comparepreds, randomforests
from PrepareTitanicData import titandata, convertages
from DataFilters import df, dfrange, showstats


set_printoptions(suppress = True) # makes for nice printing without scientific notation
np.set_printoptions(linewidth=132)

# File PrepareTitanicData.py goes through the details of preparing the data.
# It converts sex to 1,0 for F,M, and 0,1,2,3 for city embarked "S","C","Q",""
# Also for no-age we put in placeholder 1000
# for no fare we put placeholder 1000
# Cabin, Ticket #, and name are deleted


data=titandata("train") #(891,8) array
testdata=titandata("test") #(418,7) array
test8 = titandata("test8") #(418,8) array
# Call function titandata which takes an argument string, which must be either "train", "test", or "test8"
#print data[0:10]
#print testdata[0:10]
#print test8[0:10]
# Note that data and test8 are regularized and floated into an array of 8 columns:
# [0=sur, 1=class, 2=sex, 3=age, 4=sibsp, 5=parch, 6=fare, 7=embarked]
# The survival values are 0=die, 1=live, 2=don't know (for test8)
# Note that testdata is regularized and floated into an array of 7 columns
# [class, sex, age, sibsp, parch, fare, embarked]

totdata = vstack((data,test8)) # stacks data on top of test8 to create a (1309,8) array


# convert unknown placeholder ages to reasonable averages
data = convertages(data,3)
test8 = convertages(test8,3)
testdata = convertages(testdata,2)
totdata = convertages(totdata,3)


def showsurvivaltablesanalysis():
    # Now we can easily recreate the survival tables from predict.py, but more elegantly:
    malestats = showstats(df([[0,2]],data))
    femstats = showstats(df([[1,2]],data))

    print "female and male stats"
    print femstats
    print malestats

    sexclass=[]
    for s in xrange(2):
        for c in xrange(1,4):
            sexclass.append(showstats(df([[s,2],[c,1]],data)))

    sca = np.array(sexclass).reshape(2,3,3)
    print "Sex-Class"
    print sca

    #sex-class-embarked
    malesce=[]
    femsce=[]
    for c in xrange(1,4):
        for e in xrange(3):
            malesce.append(showstats(df([[0,2],[c,1],[e,7]],data)))
            femsce.append(showstats(df([[1,2],[c,1],[e,7]],data)))

    msce = np.array(malesce).reshape(3,3,3)
    fsce = np.array(femsce).reshape(3,3,3)

    print "Male Class(1st block is 1st class) and City (rows 0-2 in each block)"
    print msce
    print "Female Class(1st block is 1st class) and City (rows 0-2 in each block)"
    print fsce

    print "Male sibsp"
    for sibsp in xrange(10):
        print sibsp, showstats(df([[0,2],[sibsp,4]],data))

    print "Female sibsp"
    for sibsp in xrange(10):
        print sibsp, showstats(df([[1,2],[sibsp,4]],data))

    print "Male parch"
    for parch in xrange(10):
        print parch, showstats(df([[0,2],[parch,5]],data))

    print "Female parch"
    for parch in xrange(10):
        print parch, showstats(df([[1,2],[parch,5]],data))

    for sib in xrange(3):
        for par in xrange(3):
            print sib,par,"male: %s" %showstats(df([[0,2],[sib,4],[par,5]],data)), \
            "female: %s" %showstats(df([[1,2],[sib,4],[par,5]],data))

    print "1st class males sibsp"
    for sibsp in xrange(10):
        print sibsp, showstats(df([[0,2],[1,1],[sibsp,4]],data))

    print "1st class males parch"
    for parch in xrange(10):
        print parch, showstats(df([[0,2],[1,1],[parch,5]],data))

    #all young males that survive
    #print df([[0,2],[1,0]],dfrange(0,10,3,data))

    print "1st and 2nd class French males by sibsp"
    for sibsp in xrange(2):
        print "age 0-80, sibsp = %i" %sibsp, showstats(df([[0,2],[1,7],[sibsp,4]],dfrange(0,80,3,dfrange(1,2,1,data))))
        print "age 0-19, sibsp = %i" %sibsp, showstats(df([[0,2],[1,7],[sibsp,4]],dfrange(0,19,3,dfrange(1,2,1,data))))
        print "age 20-80, sibsp = %i" %sibsp, showstats(df([[0,2],[1,7],[sibsp,4]],dfrange(20,80,3,dfrange(1,2,1,data))))

    print showstats(df([[0,2],[1,7]],data))

    print "3rd class young males by age bin"
    for x in xrange(5):
        print showstats(df([[0,2],[3,1]],dfrange(2*x+0.01,2*(x+1),3,data)))

    print "3rd class S females under age<=5"
    print showstats(df([[1,2],[0,7]],dfrange(3,3,1,dfrange(0,5,3,data))))
    print "3rd class S females under 18 with sibsp=0,1"
    print df([[1,2],[0,7]],dfrange(0,1,4,dfrange(3,3,1,dfrange(0,18,3,data))))
    print showstats(df([[1,2],[0,7]],dfrange(0,1,4,dfrange(3,3,1,dfrange(0,18,3,data)))))


    print "young (age<=12) 3rd class males by sibsp"
    print "sibsp=0,1:",showstats(df([[0,2],[3,1]],dfrange(0,1,4,dfrange(0,12,3,data))))
    print "sibsp=2-8:",showstats(df([[0,2],[3,1]],dfrange(2,8,4,dfrange(0,12,3,data))))


    print "3rd class girls then boys (age<=15) with many siblings (sibsp>=2)"
    print showstats(df([[1,2]],dfrange(2,8,4,dfrange(3,3,1,dfrange(0,15,3,data)))))
    print showstats(df([[0,2]],dfrange(2,8,4,dfrange(3,3,1,dfrange(0,15,3,data)))))

    print "3rd class young girls from C or Q with many siblings"
    print showstats(df([[1,2],[3,3]],dfrange(2,8,4,dfrange(1,2,7,dfrange(0,15,3,data)))))

    print "3rd class S female young (age<=8) with 0 or 1 sibling"
    print showstats(df([[1,2],[0,7]],dfrange(0,1,4,dfrange(3,3,1,dfrange(0,8,3,data)))))
    print df([[1,2],[0,7]],dfrange(0,1,4,dfrange(3,3,1,dfrange(0,8,3,data))))
    #print showstats(df([[1,2],[0,7]],dfrange(0,1,4,dfrange(3,3,1,dfrange(18,80,3,data)))))

    # It looks like having lots of siblings is really bad for you. Conversely, having 0 or 1 seems to save
    # otherwise damned souls F3Syoung and M3young.

    print "3rd class S females in test data!! under 18 with sibsp=0,1"
    print df([[1,2],[0,7]],dfrange(0,1,4,dfrange(3,3,1,dfrange(0,18,3,test8))))

    # No-age-given analysis
    print "The average age for passengers. "\
          "NOTE this should be run only when placeholder age for age not given is set to 1000"
    print np.mean(dfrange(0,100,3,data)[0::,3]) #mean of age for age <=100
    # However, we might do a bit better. Generally, sibsp>1 implies you are a child. Let's see this.
    print "Average age by sibsp:"
    for sp in xrange(6):
        print "sibsp = %i" %sp, np.mean(dfrange(sp,sp,4,dfrange(0,100,3,data))[0::,3])

    # Random Forests

    # It feels like fare is a redundant variable, as it tracks closely with class (and perhaps city).
    # Perhaps we should train the forest without fare, and maybe also parch.
    # And while we are at it try without sibsp again. Let's create the necessary data.

    data7 = scipy.delete(data,6,1) #delete fare column, resulting in a (891,7) array
    data6 = scipy.delete(data7,5,1) #delete parch column, resulting in a (891,6) array
    data5 = scipy.delete(data6,4,1) #delete sibsp column, resulting in a (891,5) array
    # And we'll want to test these forests on the test data too, which must be of the same form:
    test7 = scipy.delete(test8,6,1)
    test6 = scipy.delete(test7,5,1)
    test5 = scipy.delete(test6,4,1)


    # The function randomforests in predictions.py runs many forests and finds the average prediction.

    # RFC105 = randomforests(10,100,data5,test5[0::,1::])
    # print np.nonzero(f3sm12pred(test8) - RFC105)[0]
    # this confirms the results of randforest.py for which passengers RFC and F3SM12 disagree

    # Let's apply the RFC method to both the train data (this helps to see the degree of over-fitting)
    # as well as the test data, to make new predictions.
    numfor = 5
    RFC8 = randomforests(numfor,100,data,test8[0::,1::])
    RFC7 = randomforests(numfor,100,data7,test7[0::,1::])
    RFC6 = randomforests(numfor,100,data6,test6[0::,1::])
    RFC5 = randomforests(numfor,100,data5,test5[0::,1::])
    RFC8train = randomforests(numfor,100,data,data[0::,1::])
    RFC7train = randomforests(numfor,100,data7,data7[0::,1::])
    RFC6train = randomforests(numfor,100,data6,data6[0::,1::])
    RFC5train = randomforests(numfor,100,data5,data5[0::,1::])


    print "Scores for 'predictions' back on train data for GM, F3SM12, newpred, and RFC8, RFC7, RFC6, RFC5"
    print "GM", predicttrain(genderpred(data))
    print "F3SM12", predicttrain(f3sm12pred(data))
    print "new", predicttrain(newpred(data))
    print "RFC8",predicttrain(RFC8train)
    print "RFC7",predicttrain(RFC7train)
    print "RFC6",predicttrain(RFC6train)
    print "RFC5",predicttrain(RFC5train)


    print "Comparing predictions"
    comparepreds(newpred(test8),RFC8)
    comparepreds(f3sm12pred(test8),RFC8)
    comparepreds(newpred(test8),f3sm12pred(test8))
    comparepreds(RFC8,RFC7)
    comparepreds(RFC7,RFC6)
    comparepreds(RFC6,RFC5)

    # Scores for predictions on [test, train] data sets.
    # Note the RFC5 (neglecting fare, sibsp, parch) prediction on train is random,
    # so changes each time (usually is around 0.85)
    # The first entries are our scores from Kaggle.com.
    # The spread indicates the degree of over-fitting. Clearly RFC over-fits the most.
    # However, all of the prediction models do worse on the test data than the train data.
    # This didn't have to be the case, particularly for the simpler models (GM and F3SM12)

    scoreGM = [0.76555, predicttrain(genderpred(data))] #160/209 right
    scoreF3SM12 = [0.78947, predicttrain(f3sm12pred(data))] #165/209
    scorenew = [0.78469, predicttrain(newpred(data))] #164/209
    scoreRFC5 = [0.77033, predicttrain(RFC5train)] #161/209
    scoreRFC7 = [0.77512, predicttrain(RFC7train)] #162/209
    # Note that only half of the test data (209) is used on the leaderboard.

    print "Scores for predictions on [test, train] data sets for GM, F3SM12, newpred, RFC5, RFC7"
    print scoreGM
    print scoreF3SM12
    print scorenew
    print scoreRFC5
    print scoreRFC7


#showsurvivaltablesanalysis()

totaltime = time() - starttime
print "This code took %f s to run" %totaltime