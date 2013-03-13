from threading import Timer
import time
#time import only required for time.sleep (line 22)
#What I can think of to stop the graph search: while loop + global var becoming False in getLast. I haven't find anythg smarter on the Internet yet.


bestAction=-1
order=None

def getLast():
	print "Dans getLast"
	global order
	global t
	order=bestAction
	t.cancel()

def graphSearch(depth):
	global bestAction
	for i in range(depth):
		print "order value: " +str(order)
		bestAction=i
		print bestAction
		time.sleep(1)
	return "Done"

t=Timer(9.0,getLast)
t.start()
graphSearch(12)


