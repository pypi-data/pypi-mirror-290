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
from project.sparta_7ea42ed2bd.sparta_4b6986daa6.qube_8d44c27597 import sparta_3f89e05aa0
from project.sparta_cb7699d1a4.sparta_ffdb8c6b84 import qube_4cee2863ff as qube_4cee2863ff
from project.sparta_cb7699d1a4.sparta_272b34bb16 import qube_d928fa0973 as qube_d928fa0973
from project.sparta_cb7699d1a4.sparta_a4d0b925fc.qube_f7f6947811 import Email as Email
def sparta_1dc24a2641(function):
	def A(request,*E,**C):
		A=request;B=_B
		if not A.user.is_active:B=_C;logout(A)
		if not A.user.is_authenticated:B=_C;logout(A)
		if not B:
			D=C.get(_H)
			if D is not None:F=qube_d928fa0973.sparta_7cfc3daa18(D);login(A,F)
		return function(A,*E,**C)
	return A
def sparta_5dbe3eb082(function):
	def A(request,*B,**C):
		A=request
		if not A.user.is_active:return HttpResponseRedirect(reverse(_G))
		if A.user.is_authenticated:return function(A,*B,**C)
		else:return HttpResponseRedirect(reverse(_G))
	return A
def sparta_9497f67b35(function):
	def A(request,*B,**C):
		try:return function(request,*B,**C)
		except Exception as A:
			if conf_settings.DEBUG:print('Try catch exception with error:');print(A);print('traceback:');print(traceback.format_exc())
			D={_A:-1,_D:str(A)};E=json.dumps(D);return HttpResponse(E)
	return A
def sparta_4db17ef77e(function):
	def A(request,*D,**E):
		A=request;B=_C
		try:
			F=json.loads(A.body);G=json.loads(F[_I]);H=G[_H];C=qube_d928fa0973.sparta_7cfc3daa18(H)
			if C is not None:B=_B;A.user=C
		except Exception as I:print('exception pip auth');print(I)
		if B:return function(A,*D,**E)
		else:return HttpResponseRedirect(reverse(_G))
	return A
def sparta_f1b9c99a56(code):
	try:
		B=SpartaQubeCode.objects.all()
		if B.count()==0:return code=='admin'
		else:C=B[0].spartaqube_code;A=hashlib.md5(code.encode(_E)).hexdigest();A=base64.b64encode(A.encode(_E));A=A.decode(_E);return A==C
	except Exception as D:pass
	return _C
def sparta_88c2c9c3c4():
	A=LocalApp.objects.all()
	if A.count()==0:B=str(uuid.uuid4());LocalApp.objects.create(app_id=B,date_created=datetime.now());return B
	else:return A[0].app_id
def sparta_7708de197d():A=socket.gethostname();B=socket.gethostbyname(A);return B
def sparta_9a8936058d(json_data):
	D='ip_addr';A=json_data;del A[_J];del A[_K]
	try:A[D]=sparta_7708de197d()
	except:A[D]=-1
	C=dict();C[_I]=json.dumps(A);B=requests.post(f"{conf_settings.SPARTAQUBE_WEBSITE}/create-user",data=json.dumps(C))
	if B.status_code==200:
		try:
			A=json.loads(B.text)
			if A[_A]==1:return{_A:1,_F:_B}
			else:A[_F]=_C;return A
		except Exception as E:return{_A:-1,_F:_C,_D:str(E)}
	return{_A:1,_F:_C,_D:f"status code: {B.status_code}. Please check your internet connection"}
def sparta_c2ec5091b6(json_data,hostname_url):
	O='emailExist';N='passwordConfirm';K='email';B=json_data;F={N:'The two passwords must be the same...',K:'Email address is not valid...','form':'The form you sent is not valid...',O:'This email is already registered...'};E=_C;P=B['firstName'].capitalize();Q=B['lastName'].capitalize();C=B[K].lower();L=B[_J];R=B[_K];S=B['code'];B['app_id']=sparta_88c2c9c3c4()
	if not sparta_f1b9c99a56(S):return{_A:-1,_D:'Invalid spartaqube code, please contact your administrator'}
	if L!=R:E=_B;G=F[N]
	if not re.match('[^@]+@[^@]+\\.[^@]+',C):E=_B;G=F[K]
	if User.objects.filter(username=C).exists():E=_B;G=F[O]
	if not E:
		T=sparta_9a8936058d(B);M=_B;U=T[_F]
		if not U:M=_C
		A=User.objects.create_user(C,C,L);A.is_staff=_C;A.username=C;A.first_name=P;A.last_name=Q;A.is_active=_B;A.save();D=UserProfile(user=A);H=str(A.id)+'_'+str(A.email);H=H.encode(_E);I=hashlib.md5(H).hexdigest()+str(datetime.now());I=I.encode(_E);V=str(uuid.uuid4());D.user_profile_id=hashlib.sha256(I).hexdigest();D.email=C;D.api_key=str(uuid.uuid4());D.registration_token=V;D.b_created_website=M;D.save();J={_A:1,'userObj':A};return J
	J={_A:-1,_D:G};return J
def sparta_ac5d9cb8d1(user_obj,hostname_url,registration_token):C='Validate your account';B=user_obj;A=Email(B.username,[B.email],f"Welcome to {conf_settings.PROJECT_NAME}",C);A.addOneRow(C);A.addSpaceSeparator();A.addOneRow('Click on the link below to validate your account');D=f"{hostname_url.rstrip('/')}/registration-validation/{registration_token}";A.addOneCenteredButton('Validate',D);A.send()
def sparta_3730419ddb(token):
	C=UserProfile.objects.filter(registration_token=token)
	if C.count()>0:A=C[0];A.registration_token='';A.is_account_validated=_B;A.save();B=A.user;B.is_active=_B;B.save();return{_A:1,'user':B}
	return{_A:-1,_D:'Invalid registration token'}
def sparta_5b5f63d50f():return conf_settings.IS_GUEST_CODE_REQUIRED
def sparta_3d234cdeee(guest_code):
	if GuestCodeGlobal.objects.filter(guest_id=guest_code,is_active=_B).count()>0:return _B
	return _C
def sparta_dfc7af875d(guest_code,user_obj):
	D=user_obj;C=guest_code
	if GuestCodeGlobal.objects.filter(guest_id=C,is_active=_B).count()>0:return _B
	A=GuestCode.objects.filter(user=D)
	if A.count()>0:return _B
	else:
		A=GuestCode.objects.filter(guest_id=C,is_used=_C)
		if A.count()>0:B=A[0];B.user=D;B.is_used=_B;B.save();return _B
	return _C
def sparta_01ed41d1c7(user):
	A=UserProfile.objects.filter(user=user)
	if A.count()==1:return A[0].is_banned
	else:return _C
def sparta_c27cd6eabb(email,captcha):
	D=sparta_3f89e05aa0(captcha)
	if D[_A]!=1:return{_A:-1,_D:_L}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0];C=str(uuid.uuid4());A.token_reset_password=C;A.save();sparta_ed73d7a19e(A.user,C);return{_A:1}
def sparta_ed73d7a19e(user_obj,token_reset_password):B=user_obj;A=Email(B.username,[B.email],'Reset Password','Reset Password Message');A.addOneRow('Reset code','Copy the following code to reset your password');A.addSpaceSeparator();A.addOneRow(token_reset_password);A.send()
def sparta_63b0bff7f2(captcha,token,email,password):
	D=sparta_3f89e05aa0(captcha)
	if D[_A]!=1:return{_A:-1,_D:_L}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0]
	if not token==A.token_reset_password:return{_A:-1,_D:'Invalid token..., please try again'}
	A.token_reset_password='';A.save();C=A.user;C.set_password(password);C.save();return{_A:1}