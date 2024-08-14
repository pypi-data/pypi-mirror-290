_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_560fb5fd39.sparta_ec245d0f93 import qube_6a153c9958 as qube_6a153c9958
from project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a import sparta_1d487ed1b4
@csrf_exempt
def sparta_4f371016a3(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_6a153c9958.sparta_4f371016a3(B)
@csrf_exempt
def sparta_10eecbb6b9(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_8bcb56c572(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_068058ba8e(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)