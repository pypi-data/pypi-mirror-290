import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_a6409ef632():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_ebffaacc7e(userId):A=sparta_a6409ef632();B=os.path.join(A,userId);return B
def sparta_de5015f028(notebookProjectId,userId):A=sparta_ebffaacc7e(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_a44ff6bb63(notebookProjectId,userId):A=sparta_ebffaacc7e(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_0024a3eefa(notebookProjectId,userId,ipynbFileName):A=sparta_ebffaacc7e(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_5780bf7bff(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_de5015f028(B,C);G=sparta_ebffaacc7e(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_5f605f5d14(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_5780bf7bff(A,B);C=f"{A}.zip";D=sparta_ebffaacc7e(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}