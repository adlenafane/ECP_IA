from utility import *

def passFailedTest(function, target_value):
	print "Result:", str(function)
	print ("----Failed", "Pass")[function == target_value]

print '\n##### Utility distance tests #####\n'

print "computeMinDistance((1,2),(1,4)):"
passFailedTest(computeMinDistance((1,2),(1,4)), 2)

print "findNextMove((1,2),(1,4)):"
passFailedTest(findNextMove((1,2),(1,4)), (1,3))

print "computeMinDistance((1,2),(3,4)):"
passFailedTest(computeMinDistance((1,2),(3,4)), 2)

print "findNextMove((1,2),(3,4)):"
passFailedTest(findNextMove((1,2),(3,4)),(2,3))
print '\n##########'
