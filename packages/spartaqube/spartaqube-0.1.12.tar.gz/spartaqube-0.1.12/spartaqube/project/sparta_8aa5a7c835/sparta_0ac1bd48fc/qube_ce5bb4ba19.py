import os
from project.sparta_8aa5a7c835.sparta_0ac1bd48fc.qube_74c7e9356b import qube_74c7e9356b
from project.sparta_8aa5a7c835.sparta_0ac1bd48fc.qube_3e0d7ec558 import qube_3e0d7ec558
from project.sparta_8aa5a7c835.sparta_0ac1bd48fc.qube_79bed0122f import qube_79bed0122f
from project.sparta_8aa5a7c835.sparta_0ac1bd48fc.qube_ffe2de4c20 import qube_ffe2de4c20
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_74c7e9356b()
		elif A.dbType==1:A.dbCon=qube_3e0d7ec558()
		elif A.dbType==2:A.dbCon=qube_79bed0122f()
		elif A.dbType==4:A.dbCon=qube_ffe2de4c20()
		return A.dbCon