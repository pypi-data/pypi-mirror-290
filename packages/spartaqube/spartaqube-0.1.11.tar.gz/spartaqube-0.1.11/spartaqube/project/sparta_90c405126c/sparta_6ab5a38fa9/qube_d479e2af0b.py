_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_a1c64beb30.sparta_d5a4a4b037 import qube_53339f257e as qube_53339f257e
from project.sparta_02c008a725.sparta_27262642be.qube_ddd37178e0 import sparta_5d58fce052
@csrf_exempt
def sparta_f6f7853468(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_53339f257e.sparta_f6f7853468(B)
@csrf_exempt
def sparta_096b0b12c7(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_841545eafb(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_db4a52971e(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)