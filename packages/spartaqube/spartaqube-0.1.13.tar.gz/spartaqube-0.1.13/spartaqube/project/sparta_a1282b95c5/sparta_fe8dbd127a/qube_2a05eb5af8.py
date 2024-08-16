_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_cb7699d1a4.sparta_67553e9f2a import qube_7480dd05a3 as qube_7480dd05a3
from project.sparta_7ea42ed2bd.sparta_4b6986daa6.qube_8d44c27597 import sparta_3f89e05aa0
@csrf_exempt
def sparta_c2ec5091b6(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_7480dd05a3.sparta_c2ec5091b6(B)
@csrf_exempt
def sparta_59165faa53(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_b7d24f6d6e(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_a5967ff7ca(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)