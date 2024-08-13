import os
from project.sparta_02c008a725.sparta_190e0028fa.qube_5ebfe4b4c3 import qube_5ebfe4b4c3
from project.sparta_02c008a725.sparta_190e0028fa.qube_92cd9b8082 import qube_92cd9b8082
from project.sparta_02c008a725.sparta_190e0028fa.qube_b06163f54b import qube_b06163f54b
from project.sparta_02c008a725.sparta_190e0028fa.qube_d189d43635 import qube_d189d43635
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_5ebfe4b4c3()
		elif A.dbType==1:A.dbCon=qube_92cd9b8082()
		elif A.dbType==2:A.dbCon=qube_b06163f54b()
		elif A.dbType==4:A.dbCon=qube_d189d43635()
		return A.dbCon