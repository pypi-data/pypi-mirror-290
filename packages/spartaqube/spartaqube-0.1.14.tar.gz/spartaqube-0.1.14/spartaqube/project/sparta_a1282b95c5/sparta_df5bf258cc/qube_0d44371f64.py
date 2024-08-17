_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_cb7699d1a4.sparta_678522f69e import qube_e7fa6015f8 as qube_e7fa6015f8
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_5dbe3eb082
@csrf_exempt
@sparta_5dbe3eb082
def sparta_20564b22a2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e7fa6015f8.sparta_20564b22a2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_02146abdca(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_e7fa6015f8.sparta_02146abdca(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_c6e31146a7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_e7fa6015f8.sparta_c6e31146a7(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_c9290ebfa9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e7fa6015f8.sparta_c9290ebfa9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_b6fb7fd68f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e7fa6015f8.sparta_b6fb7fd68f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_ee636968a5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e7fa6015f8.sparta_ee636968a5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_3d155d479d(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_e7fa6015f8.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_ab1208539b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e7fa6015f8.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_2603c5933c(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_e7fa6015f8.sparta_2603c5933c(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_00ff3bcba2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e7fa6015f8.sparta_00ff3bcba2(A,C);E=json.dumps(D);return HttpResponse(E)