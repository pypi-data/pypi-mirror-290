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
from project.sparta_a1c64beb30.sparta_5edc841f81 import qube_a840181683 as qube_a840181683
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_8ca5be44d2
@csrf_exempt
@sparta_8ca5be44d2
def sparta_12dd40d3d1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a840181683.sparta_12dd40d3d1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_6adc290f96(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_a840181683.sparta_6adc290f96(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_f44ce15e78(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_a840181683.sparta_f44ce15e78(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_914c58b08b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a840181683.sparta_914c58b08b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_3b7fa09516(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a840181683.sparta_3b7fa09516(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_3de530ac1c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a840181683.sparta_3de530ac1c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_22653999fc(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_a840181683.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_b2fd32592c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a840181683.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_c522eb03a6(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_a840181683.sparta_c522eb03a6(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_694e50c875(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a840181683.sparta_694e50c875(A,C);E=json.dumps(D);return HttpResponse(E)