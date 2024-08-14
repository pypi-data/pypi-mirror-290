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
from project.sparta_560fb5fd39.sparta_36e7e933ed import qube_1872829cc9 as qube_1872829cc9
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_f076ba2889
@csrf_exempt
@sparta_f076ba2889
def sparta_e743cb8eec(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1872829cc9.sparta_e743cb8eec(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_4c5dcb5919(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_1872829cc9.sparta_4c5dcb5919(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_f076ba2889
def sparta_64714290ce(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_1872829cc9.sparta_64714290ce(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_f076ba2889
def sparta_cda6a2ef14(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1872829cc9.sparta_cda6a2ef14(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_7146425da2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1872829cc9.sparta_7146425da2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_41b0c9379b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1872829cc9.sparta_41b0c9379b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_aac223bf4a(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_1872829cc9.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_f076ba2889
def sparta_e732353aac(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1872829cc9.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_9f0cbbaf4e(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_1872829cc9.sparta_9f0cbbaf4e(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_11c30f5174(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1872829cc9.sparta_11c30f5174(A,C);E=json.dumps(D);return HttpResponse(E)