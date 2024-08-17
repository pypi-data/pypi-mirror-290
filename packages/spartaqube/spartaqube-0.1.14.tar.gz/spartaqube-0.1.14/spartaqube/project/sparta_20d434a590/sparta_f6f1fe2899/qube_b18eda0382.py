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
import project.sparta_7ea42ed2bd.sparta_4b6986daa6.qube_8d44c27597 as qube_8d44c27597
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_1dc24a2641
from project.sparta_cb7699d1a4.sparta_67553e9f2a import qube_7480dd05a3 as qube_7480dd05a3
from project.sparta_a1282b95c5.sparta_fe8dbd127a import qube_2a05eb5af8 as qube_2a05eb5af8
from project.models import LoginLocation,UserProfile
def sparta_95196b127a():return{'bHasCompanyEE':-1}
def sparta_392647658e(request):B=request;A=qube_8d44c27597.sparta_eacc3c863b(B);A[_C]=qube_8d44c27597.sparta_4ddedd7098();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_1dc24a2641
def sparta_232b3cd6e9(request):
	C=request;B='/';A=C.GET.get(_K)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_b2a697fb04(C,A)
def sparta_28acf5eaa0(request,redirectUrl):return sparta_b2a697fb04(request,redirectUrl)
def sparta_b2a697fb04(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_I;H='Email or password incorrect'
	if A.method==_J:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_7480dd05a3.sparta_01ed41d1c7(F):return sparta_392647658e(A)
				login(A,F);K,L=qube_8d44c27597.sparta_afcedc3765();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_8d44c27597.sparta_eacc3c863b(A);B.update(qube_8d44c27597.sparta_f43a064780(A));B[_C]=qube_8d44c27597.sparta_4ddedd7098();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_95196b127a());return render(A,'dist/project/auth/login.html',B)
@sparta_1dc24a2641
def sparta_9079552741(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_I;F=qube_7480dd05a3.sparta_5b5f63d50f()
	if A.method==_J:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_7480dd05a3.sparta_3d234cdeee(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_7480dd05a3.sparta_c2ec5091b6(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_8d44c27597.sparta_eacc3c863b(A);C.update(qube_8d44c27597.sparta_f43a064780(A));C[_C]=qube_8d44c27597.sparta_4ddedd7098();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_95196b127a());return render(A,'dist/project/auth/registration.html',C)
def sparta_bc1bc76745(request):A=request;B=qube_8d44c27597.sparta_eacc3c863b(A);B[_C]=qube_8d44c27597.sparta_4ddedd7098();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_0caef9f704(request,token):
	A=request;B=qube_7480dd05a3.sparta_3730419ddb(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_8d44c27597.sparta_eacc3c863b(A);D[_C]=qube_8d44c27597.sparta_4ddedd7098();return redirect(_K)
def sparta_6719e14e05(request):logout(request);return redirect(_K)
def sparta_230cd93f5b(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_c27cd6eabb(request):
	A=request;E='';F=_I
	if A.method==_J:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_7480dd05a3.sparta_c27cd6eabb(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_8d44c27597.sparta_eacc3c863b(A);C.update(qube_8d44c27597.sparta_f43a064780(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_8d44c27597.sparta_4ddedd7098();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_8d44c27597.sparta_eacc3c863b(A);D.update(qube_8d44c27597.sparta_f43a064780(A));D[_C]=qube_8d44c27597.sparta_4ddedd7098();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_95196b127a());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_63b0bff7f2(request):
	D=request;E='';B=_I
	if D.method==_J:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_7480dd05a3.sparta_63b0bff7f2(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_8d44c27597.sparta_eacc3c863b(D);A.update(qube_8d44c27597.sparta_f43a064780(D));A[_C]=qube_8d44c27597.sparta_4ddedd7098();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_95196b127a());return render(D,_N,A)