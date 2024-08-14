_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='login'
_J='POST'
_I=False
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a as qube_f673e75e5a
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_cde414cdf7
from project.sparta_560fb5fd39.sparta_ec245d0f93 import qube_6a153c9958 as qube_6a153c9958
from project.sparta_f9261d4afd.sparta_085a5fa158 import qube_d113abc5f1 as qube_d113abc5f1
from project.models import LoginLocation,UserProfile
def sparta_a8f1b938bf():return{'bHasCompanyEE':-1}
def sparta_3078feeac6(request):B=request;A=qube_f673e75e5a.sparta_f06548cd94(B);A[_C]=qube_f673e75e5a.sparta_eef3e44917();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_cde414cdf7
def sparta_65c2cef46e(request):
	C=request;B='/';A=C.GET.get(_K)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_d1ad0aa6d4(C,A)
def sparta_e0ea84d925(request,redirectUrl):return sparta_d1ad0aa6d4(request,redirectUrl)
def sparta_d1ad0aa6d4(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_I;H='Email or password incorrect'
	if A.method==_J:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_6a153c9958.sparta_3abee88aee(F):return sparta_3078feeac6(A)
				login(A,F);K,L=qube_f673e75e5a.sparta_d11e279f79();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_f673e75e5a.sparta_f06548cd94(A);B.update(qube_f673e75e5a.sparta_b024cde646(A));B[_C]=qube_f673e75e5a.sparta_eef3e44917();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_a8f1b938bf());return render(A,'dist/project/auth/login.html',B)
@sparta_cde414cdf7
def sparta_71a70c8b1d(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_I;F=qube_6a153c9958.sparta_1d05f19a15()
	if A.method==_J:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_6a153c9958.sparta_76b3d2756b(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_6a153c9958.sparta_4f371016a3(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_f673e75e5a.sparta_f06548cd94(A);C.update(qube_f673e75e5a.sparta_b024cde646(A));C[_C]=qube_f673e75e5a.sparta_eef3e44917();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_a8f1b938bf());return render(A,'dist/project/auth/registration.html',C)
def sparta_cc42837b98(request):A=request;B=qube_f673e75e5a.sparta_f06548cd94(A);B[_C]=qube_f673e75e5a.sparta_eef3e44917();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_ba2346862b(request,token):
	A=request;B=qube_6a153c9958.sparta_4060ee3ad8(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_f673e75e5a.sparta_f06548cd94(A);D[_C]=qube_f673e75e5a.sparta_eef3e44917();return redirect(_K)
def sparta_62436d960b(request):logout(request);return redirect(_K)
def sparta_56d398d8c3(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_745715adf1(request):
	A=request;E='';F=_I
	if A.method==_J:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_6a153c9958.sparta_745715adf1(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_f673e75e5a.sparta_f06548cd94(A);C.update(qube_f673e75e5a.sparta_b024cde646(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_f673e75e5a.sparta_eef3e44917();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_f673e75e5a.sparta_f06548cd94(A);D.update(qube_f673e75e5a.sparta_b024cde646(A));D[_C]=qube_f673e75e5a.sparta_eef3e44917();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_a8f1b938bf());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_b9eb4eb4d7(request):
	D=request;E='';B=_I
	if D.method==_J:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_6a153c9958.sparta_b9eb4eb4d7(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_f673e75e5a.sparta_f06548cd94(D);A.update(qube_f673e75e5a.sparta_b024cde646(D));A[_C]=qube_f673e75e5a.sparta_eef3e44917();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_a8f1b938bf());return render(D,_N,A)