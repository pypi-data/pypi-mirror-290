_T='token_reset'
_S='Invalid captcha'
_R='Passwords must be the same'
_Q='new_password_confirm'
_P='Password must be at least 5 characters'
_O='Please put the same passwords'
_N='The current password is not correct'
_M='oldPassword'
_L='passwordConfirm'
_K='password'
_J='Invalid email'
_I='Invalid spartaqube admin password'
_H='new_password'
_G='admin'
_F='email'
_E='captcha'
_D='utf-8'
_C='message'
_B='errorMsg'
_A='res'
import os,json,uuid,base64,random,string
from datetime import datetime
import hashlib,requests,hashlib
from cryptography.fernet import Fernet
from random import randint
import pytz
UTC=pytz.utc
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password
from django.conf import settings as conf_settings
from django.contrib.auth import login
from project.models import UserProfile,Avatar,contactUS,SpartaQubeCode
from project.sparta_560fb5fd39.sparta_764b7a8fd2 import qube_b42272d78d as qube_b42272d78d
from project.sparta_560fb5fd39.sparta_b004e8bb14.qube_7fc040e78f import Email as Email
from project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a import sparta_1d487ed1b4,sparta_4fd4cb4cf3,sparta_7ddebadc9c
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_14976caafe
def sparta_e743cb8eec(json_data,user_obj):
	B=user_obj;A=json_data;D=A['messageContactUs'];E=A['titleContactUs'];G=A[_E];H=datetime.now();contactUS.objects.create(message=D,title=E,user=B,date_created=H);I={_C:D,'title':E,_E:G,_F:B.email,'first_name':B.first_name,'last_name':B.last_name};F=dict();F['jsonData']=json.dumps(I);C=requests.post(f"{conf_settings.SPARTAQUBE_WEBSITE}/contact-us-app",data=json.dumps(F))
	if C.status_code==200:
		try:print('response.text');print(C.text);A=json.loads(C.text);return A
		except Exception as J:return{_A:-1,_B:str(J)}
	K={_A:-1,_B:'An unexpected error occurred, please check your internet connection and try again'};return K
def sparta_56522e4c91(message,typeCase=0,companyName=None):
	D='Type';B=companyName;C=User.objects.filter(is_staff=True)
	if C.count()>0:
		E=C[0];A=Email(E.username,[conf_settings.CONTACT_US_EMAIL],'Contact US','Contact US new message')
		if B is not None:A.addOneRow('Company',B);A.addLineSeparator()
		A.addOneRow('Message',message);A.addLineSeparator()
		if int(typeCase)==0:A.addOneRow(D,'General question')
		else:A.addOneRow(D,'Report Bug')
		A.send()
def sparta_4c5dcb5919(json_data,userObj):
	C=json_data;A=userObj;D=C[_K];E=C[_L];F=C[_M]
	if len(D)>4:
		if D==E:
			if A.check_password(F):G=make_password(D);A.password=G;A.save();B={_A:1,'userObj':A}
			else:B={_A:-1,_C:_N}
		else:B={_A:-1,_C:_O}
	else:B={_A:-1,_C:_P}
	return B
def sparta_b754d993d9(json_data,userObj):
	B=json_data;C=B[_K];D=B[_L];E=B[_M]
	if len(C)>4:
		if C==D:
			if userObj.check_password(E):A={_A:1}
			else:A={_A:-1,_C:_N}
		else:A={_A:-1,_C:_O}
	else:A={_A:-1,_C:_P}
	return A
def sparta_64714290ce(json_data,userObj):
	D=json_data;F=D['old_spartaqube_code'];G=D['new_spartaqube_code']
	if not sparta_14976caafe(F):return{_A:-1,_B:'Invalid current code'}
	A=hashlib.md5(G.encode(_D)).hexdigest();A=base64.b64encode(A.encode(_D));A=A.decode(_D);B=datetime.now().astimezone(UTC);E=SpartaQubeCode.objects.all()
	if E.count()==0:SpartaQubeCode.objects.create(spartaqube_code=A,date_created=B,last_update=B)
	else:C=E[0];C.spartaqube_code=A;C.last_update=B;C.save()
	return{_A:1}
def sparta_cda6a2ef14(json_data,userObj):A=userObj;C=json_data['base64image'];K=hashlib.sha256((str(A.id)+'_'+A.email+str(datetime.now())).encode(_D)).hexdigest();D,E=C.split(';base64,');F,L=D.split('/');G=F.split(':')[-1];B=UserProfile.objects.get(user=A);H=datetime.now();I=Avatar.objects.create(avatar=G,image64=E,date_created=H);B.avatar=I;B.save();J={_A:1};return J
def sparta_7146425da2(json_data,userObj):B=json_data['bDarkTheme'];A=UserProfile.objects.get(user=userObj);A.is_dark_theme=B;A.save();C={_A:1};return C
def sparta_41b0c9379b(json_data,userObj):B=json_data['theme'];A=UserProfile.objects.get(user=userObj);A.editor_theme=B;A.save();C={_A:1};return C
def sparta_3f5c771dc4():B='spartaqube-reset-password';A=B.encode(_D);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_D));return A.decode(_D)
def sparta_9f0cbbaf4e(json_data):
	A=json_data;C=A[_F];E=A[_G];B=A[_H];F=A[_Q]
	if not sparta_7ddebadc9c(E):return{_A:-1,_B:_I}
	if not User.objects.filter(username=C).exists():return{_A:-1,_B:_J}
	if B!=F:return{_A:-1,_B:_R}
	D=User.objects.filter(username=C).all()[0];G=make_password(B);D.password=G;D.save();return{_A:1,_H:B}
def sparta_3d1b2af394(json_data):
	A=json_data;E=A[_E];B=A[_F];F=A[_G];G=sparta_1d487ed1b4(E)
	if G[_A]!=1:return{_A:-1,_B:_S}
	if not sparta_4fd4cb4cf3(F):return{_A:-1,_B:_I}
	if not User.objects.filter(username=B).exists():return{_A:-1,_B:_J}
	H=User.objects.filter(username=B).all()[0];C=db_functions.get_user_profile_obj(H);D=''.join(random.choice(string.ascii_uppercase+string.digits)for A in range(5));C.token_reset_password=D;C.save();return{_A:1,_T:D}
def sparta_11c30f5174(request,json_data):
	A=json_data;F=A[_E];D=A[_F];G=A[_G];H=A[_T];E=A[_H];I=A[_Q];J=sparta_1d487ed1b4(F)
	if J[_A]!=1:return{_A:-1,_B:_S}
	if not sparta_4fd4cb4cf3(G):return{_A:-1,_B:_I}
	if not User.objects.filter(username=D).exists():return{_A:-1,_B:_J}
	if E!=I:return{_A:-1,_B:_R}
	B=User.objects.filter(username=D).all()[0];C=db_functions.get_user_profile_obj(B)
	if C.token_reset_password!=H:return{_A:-1,_B:'Invalid reset token'}
	C.token_reset_password='';C.save();K=make_password(E);B.password=K;B.save();login(request,B);return{_A:1}