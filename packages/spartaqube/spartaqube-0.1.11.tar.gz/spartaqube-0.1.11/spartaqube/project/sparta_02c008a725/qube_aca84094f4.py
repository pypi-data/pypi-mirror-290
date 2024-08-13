import time
def sparta_c9c0dc8f57():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_c9c0dc8f57()
def sparta_cd0f65ef47(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_9fbf115b52():sparta_cd0f65ef47(False)