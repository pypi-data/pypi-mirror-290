_M='An error occurred, please try again'
_L='Invalid captcha'
_K='password_confirmation'
_J='password'
_I='jsonData'
_H='api_token_id'
_G='notLoggerAPI'
_F='is_created'
_E='utf-8'
_D='errorMsg'
_C=False
_B=True
_A='res'
import hashlib,re,uuid,json,requests,socket,base64,traceback
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout,login
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings as conf_settings
from django.urls import reverse
from project.models import UserProfile,GuestCode,GuestCodeGlobal,LocalApp,SpartaQubeCode
from project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a import sparta_1d487ed1b4
from project.sparta_560fb5fd39.sparta_764b7a8fd2 import qube_b42272d78d as qube_b42272d78d
from project.sparta_560fb5fd39.sparta_61daedc3c8 import qube_898f531424 as qube_898f531424
from project.sparta_560fb5fd39.sparta_b004e8bb14.qube_7fc040e78f import Email as Email
def sparta_cde414cdf7(function):
	def A(request,*E,**C):
		A=request;B=_B
		if not A.user.is_active:B=_C;logout(A)
		if not A.user.is_authenticated:B=_C;logout(A)
		if not B:
			D=C.get(_H)
			if D is not None:F=qube_898f531424.sparta_fe04e0e454(D);login(A,F)
		return function(A,*E,**C)
	return A
def sparta_f076ba2889(function):
	def A(request,*B,**C):
		A=request
		if not A.user.is_active:return HttpResponseRedirect(reverse(_G))
		if A.user.is_authenticated:return function(A,*B,**C)
		else:return HttpResponseRedirect(reverse(_G))
	return A
def sparta_edfcde435a(function):
	def A(request,*B,**C):
		try:return function(request,*B,**C)
		except Exception as A:
			if conf_settings.DEBUG:print('Try catch exception with error:');print(A);print('traceback:');print(traceback.format_exc())
			D={_A:-1,_D:str(A)};E=json.dumps(D);return HttpResponse(E)
	return A
def sparta_0175af00ad(function):
	def A(request,*D,**E):
		A=request;B=_C
		try:
			F=json.loads(A.body);G=json.loads(F[_I]);H=G[_H];C=qube_898f531424.sparta_fe04e0e454(H)
			if C is not None:B=_B;A.user=C
		except Exception as I:print('exception pip auth');print(I)
		if B:return function(A,*D,**E)
		else:return HttpResponseRedirect(reverse(_G))
	return A
def sparta_14976caafe(code):
	try:
		B=SpartaQubeCode.objects.all()
		if B.count()==0:return code=='admin'
		else:C=B[0].spartaqube_code;A=hashlib.md5(code.encode(_E)).hexdigest();A=base64.b64encode(A.encode(_E));A=A.decode(_E);return A==C
	except Exception as D:pass
	return _C
def sparta_e986e968fc():
	A=LocalApp.objects.all()
	if A.count()==0:B=str(uuid.uuid4());LocalApp.objects.create(app_id=B,date_created=datetime.now());return B
	else:return A[0].app_id
def sparta_83bd56c7ae():A=socket.gethostname();B=socket.gethostbyname(A);return B
def sparta_728ce1e1cc(json_data):
	D='ip_addr';A=json_data;del A[_J];del A[_K]
	try:A[D]=sparta_83bd56c7ae()
	except:A[D]=-1
	C=dict();C[_I]=json.dumps(A);B=requests.post(f"{conf_settings.SPARTAQUBE_WEBSITE}/create-user",data=json.dumps(C))
	if B.status_code==200:
		try:
			A=json.loads(B.text)
			if A[_A]==1:return{_A:1,_F:_B}
			else:A[_F]=_C;return A
		except Exception as E:return{_A:-1,_F:_C,_D:str(E)}
	return{_A:1,_F:_C,_D:f"status code: {B.status_code}. Please check your internet connection"}
def sparta_4f371016a3(json_data,hostname_url):
	O='emailExist';N='passwordConfirm';K='email';B=json_data;G={N:'The two passwords must be the same...',K:'Email address is not valid...','form':'The form you sent is not valid...',O:'This email is already registered...'};E=_C;P=B['firstName'].capitalize();Q=B['lastName'].capitalize();C=B[K].lower();L=B[_J];R=B[_K];S=B['code'];B['app_id']=sparta_e986e968fc()
	if not sparta_14976caafe(S):return{_A:-1,_D:'Invalid spartaqube code, please contact your administrator'}
	if L!=R:E=_B;F=G[N]
	if not re.match('[^@]+@[^@]+\\.[^@]+',C):E=_B;F=G[K]
	if User.objects.filter(username=C).exists():E=_B;F=G[O]
	if not E:
		M=sparta_728ce1e1cc(B);T=M[_F]
		if not T:F=M[_D]
		else:A=User.objects.create_user(C,C,L);A.is_staff=_C;A.username=C;A.first_name=P;A.last_name=Q;A.is_active=_B;A.save();D=UserProfile(user=A);H=str(A.id)+'_'+str(A.email);H=H.encode(_E);I=hashlib.md5(H).hexdigest()+str(datetime.now());I=I.encode(_E);U=str(uuid.uuid4());D.user_profile_id=hashlib.sha256(I).hexdigest();D.email=C;D.api_key=str(uuid.uuid4());D.registration_token=U;D.save();J={_A:1,'userObj':A};return J
	J={_A:-1,_D:F};return J
def sparta_c8ce529aae(user_obj,hostname_url,registration_token):C='Validate your account';B=user_obj;A=Email(B.username,[B.email],f"Welcome to {conf_settings.PROJECT_NAME}",C);A.addOneRow(C);A.addSpaceSeparator();A.addOneRow('Click on the link below to validate your account');D=f"{hostname_url.rstrip('/')}/registration-validation/{registration_token}";A.addOneCenteredButton('Validate',D);A.send()
def sparta_4060ee3ad8(token):
	C=UserProfile.objects.filter(registration_token=token)
	if C.count()>0:A=C[0];A.registration_token='';A.is_account_validated=_B;A.save();B=A.user;B.is_active=_B;B.save();return{_A:1,'user':B}
	return{_A:-1,_D:'Invalid registration token'}
def sparta_1d05f19a15():return conf_settings.IS_GUEST_CODE_REQUIRED
def sparta_76b3d2756b(guest_code):
	if GuestCodeGlobal.objects.filter(guest_id=guest_code,is_active=_B).count()>0:return _B
	return _C
def sparta_09d2ae472f(guest_code,user_obj):
	D=user_obj;C=guest_code
	if GuestCodeGlobal.objects.filter(guest_id=C,is_active=_B).count()>0:return _B
	A=GuestCode.objects.filter(user=D)
	if A.count()>0:return _B
	else:
		A=GuestCode.objects.filter(guest_id=C,is_used=_C)
		if A.count()>0:B=A[0];B.user=D;B.is_used=_B;B.save();return _B
	return _C
def sparta_3abee88aee(user):
	A=UserProfile.objects.filter(user=user)
	if A.count()==1:return A[0].is_banned
	else:return _C
def sparta_745715adf1(email,captcha):
	D=sparta_1d487ed1b4(captcha)
	if D[_A]!=1:return{_A:-1,_D:_L}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0];C=str(uuid.uuid4());A.token_reset_password=C;A.save();sparta_7e3df09c05(A.user,C);return{_A:1}
def sparta_7e3df09c05(user_obj,token_reset_password):B=user_obj;A=Email(B.username,[B.email],'Reset Password','Reset Password Message');A.addOneRow('Reset code','Copy the following code to reset your password');A.addSpaceSeparator();A.addOneRow(token_reset_password);A.send()
def sparta_b9eb4eb4d7(captcha,token,email,password):
	D=sparta_1d487ed1b4(captcha)
	if D[_A]!=1:return{_A:-1,_D:_L}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0]
	if not token==A.token_reset_password:return{_A:-1,_D:'Invalid token..., please try again'}
	A.token_reset_password='';A.save();C=A.user;C.set_password(password);C.save();return{_A:1}