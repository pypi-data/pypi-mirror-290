import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_48887f8cdc():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_571234d4eb(userId):A=sparta_48887f8cdc();B=os.path.join(A,userId);return B
def sparta_8d0da004cb(notebookProjectId,userId):A=sparta_571234d4eb(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_d9cd7e64fb(notebookProjectId,userId):A=sparta_571234d4eb(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_592521e684(notebookProjectId,userId,ipynbFileName):A=sparta_571234d4eb(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_ace5d39159(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_8d0da004cb(B,C);G=sparta_571234d4eb(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_1247be9f66(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_ace5d39159(A,B);C=f"{A}.zip";D=sparta_571234d4eb(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}