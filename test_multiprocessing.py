import multiprocessing

def worker(num):
	print 'Hello, I am worker', num
	return

if __name__ == '__main__':
	jobs = []
	for i in range(4):
		p = multiprocessing.Process(target=worker(i))
		jobs.append(p)
		p.start()