import time
def sparta_ec646b0f33():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_ec646b0f33()
def sparta_0751810186(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_117a1d9943():sparta_0751810186(False)