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
import project.sparta_02c008a725.sparta_27262642be.qube_ddd37178e0 as qube_ddd37178e0
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_ff6fcf4bef
from project.sparta_a1c64beb30.sparta_d5a4a4b037 import qube_53339f257e as qube_53339f257e
from project.sparta_90c405126c.sparta_6ab5a38fa9 import qube_d479e2af0b as qube_d479e2af0b
from project.models import LoginLocation,UserProfile
def sparta_e95e61aff4():return{'bHasCompanyEE':-1}
def sparta_fdef5526fe(request):B=request;A=qube_ddd37178e0.sparta_5b682021d4(B);A[_C]=qube_ddd37178e0.sparta_9faa53957b();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_ff6fcf4bef
def sparta_97b03634e8(request):
	C=request;B='/';A=C.GET.get(_K)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_c5beb9c487(C,A)
def sparta_2169828f7b(request,redirectUrl):return sparta_c5beb9c487(request,redirectUrl)
def sparta_c5beb9c487(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_I;H='Email or password incorrect'
	if A.method==_J:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_53339f257e.sparta_b90927555c(F):return sparta_fdef5526fe(A)
				login(A,F);K,L=qube_ddd37178e0.sparta_046f00e0a8();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_ddd37178e0.sparta_5b682021d4(A);B.update(qube_ddd37178e0.sparta_a3cc86a1aa(A));B[_C]=qube_ddd37178e0.sparta_9faa53957b();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_e95e61aff4());return render(A,'dist/project/auth/login.html',B)
@sparta_ff6fcf4bef
def sparta_ce2154395b(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_I;F=qube_53339f257e.sparta_0b9677e8c7()
	if A.method==_J:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_53339f257e.sparta_88c65d6375(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_53339f257e.sparta_f6f7853468(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_ddd37178e0.sparta_5b682021d4(A);C.update(qube_ddd37178e0.sparta_a3cc86a1aa(A));C[_C]=qube_ddd37178e0.sparta_9faa53957b();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_e95e61aff4());return render(A,'dist/project/auth/registration.html',C)
def sparta_75956df3b0(request):A=request;B=qube_ddd37178e0.sparta_5b682021d4(A);B[_C]=qube_ddd37178e0.sparta_9faa53957b();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_176e5f8bcd(request,token):
	A=request;B=qube_53339f257e.sparta_e85aeacf55(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_ddd37178e0.sparta_5b682021d4(A);D[_C]=qube_ddd37178e0.sparta_9faa53957b();return redirect(_K)
def sparta_0aedf48048(request):logout(request);return redirect(_K)
def sparta_15c958b3dc(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_6d57d7b433(request):
	A=request;E='';F=_I
	if A.method==_J:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_53339f257e.sparta_6d57d7b433(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_ddd37178e0.sparta_5b682021d4(A);C.update(qube_ddd37178e0.sparta_a3cc86a1aa(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_ddd37178e0.sparta_9faa53957b();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_ddd37178e0.sparta_5b682021d4(A);D.update(qube_ddd37178e0.sparta_a3cc86a1aa(A));D[_C]=qube_ddd37178e0.sparta_9faa53957b();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_e95e61aff4());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_14b5a6e487(request):
	D=request;E='';B=_I
	if D.method==_J:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_53339f257e.sparta_14b5a6e487(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_ddd37178e0.sparta_5b682021d4(D);A.update(qube_ddd37178e0.sparta_a3cc86a1aa(D));A[_C]=qube_ddd37178e0.sparta_9faa53957b();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_e95e61aff4());return render(D,_N,A)