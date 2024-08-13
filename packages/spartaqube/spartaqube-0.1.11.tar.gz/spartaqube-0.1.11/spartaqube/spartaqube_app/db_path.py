_A='windows'
import os,sys,getpass,platform
def sparta_ce71e9ac0f(full_path):
	A=full_path
	try:
		if not os.path.exists(A):os.makedirs(A);print(f"Folder created successfully at {A}")
		else:print(f"Folder already exists at {A}")
	except Exception as B:print(f"An error occurred: {B}")
def sparta_ea7e54df00():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_6f7516b5ff():
	B=sparta_ea7e54df00()
	if B==_A:A=f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\SpartaQube\\data"
	elif B=='linux':A=os.path.expanduser('~/SpartaQube/data')
	elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\data')
	sparta_ce71e9ac0f(A);C=os.path.join(A,'db.sqlite3');return C