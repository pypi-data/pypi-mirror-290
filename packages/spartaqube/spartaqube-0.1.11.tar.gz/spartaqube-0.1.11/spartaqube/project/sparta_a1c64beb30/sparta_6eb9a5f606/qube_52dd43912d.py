import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_f74c37ee17():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_61e6d58846(userId):A=sparta_f74c37ee17();B=os.path.join(A,userId);return B
def sparta_776b9e741d(notebookProjectId,userId):A=sparta_61e6d58846(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_6a162a80aa(notebookProjectId,userId):A=sparta_61e6d58846(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_0452c28c84(notebookProjectId,userId,ipynbFileName):A=sparta_61e6d58846(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_f4087643c9(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_776b9e741d(B,C);G=sparta_61e6d58846(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_b3d50f16ce(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_f4087643c9(A,B);C=f"{A}.zip";D=sparta_61e6d58846(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}