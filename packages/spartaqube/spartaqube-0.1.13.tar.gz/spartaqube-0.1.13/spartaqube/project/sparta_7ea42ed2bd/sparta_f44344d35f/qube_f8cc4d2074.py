import os
from project.sparta_7ea42ed2bd.sparta_f44344d35f.qube_9d1824126e import qube_9d1824126e
from project.sparta_7ea42ed2bd.sparta_f44344d35f.qube_4984b95e5d import qube_4984b95e5d
from project.sparta_7ea42ed2bd.sparta_f44344d35f.qube_1b88ba5b32 import qube_1b88ba5b32
from project.sparta_7ea42ed2bd.sparta_f44344d35f.qube_b74145c0b9 import qube_b74145c0b9
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_9d1824126e()
		elif A.dbType==1:A.dbCon=qube_4984b95e5d()
		elif A.dbType==2:A.dbCon=qube_1b88ba5b32()
		elif A.dbType==4:A.dbCon=qube_b74145c0b9()
		return A.dbCon