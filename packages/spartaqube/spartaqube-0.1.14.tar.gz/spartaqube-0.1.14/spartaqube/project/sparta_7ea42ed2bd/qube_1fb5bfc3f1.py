import time
def sparta_0afcb4dfc0():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_0afcb4dfc0()
def sparta_515ea9e1e4(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_7456a6d386():sparta_515ea9e1e4(False)