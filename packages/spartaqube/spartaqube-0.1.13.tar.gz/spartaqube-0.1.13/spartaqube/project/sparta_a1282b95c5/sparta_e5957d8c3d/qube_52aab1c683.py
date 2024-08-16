_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='Content-Disposition'
_C='res'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_cb7699d1a4.sparta_dbd3bfce81 import qube_a976df9130 as qube_a976df9130
from project.sparta_cb7699d1a4.sparta_dbd3bfce81 import qube_349eda04bf as qube_349eda04bf
from project.sparta_cb7699d1a4.sparta_054a28acad import qube_2ba6f147b4 as qube_2ba6f147b4
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_5dbe3eb082
@csrf_exempt
@sparta_5dbe3eb082
def sparta_234cd6438a(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_a976df9130.sparta_3baf64a99e(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_51680e4ebf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_e51ff06034(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_a5d2e6bec0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_55e932f206(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_508a1a5fa2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_7f7d195fff(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_6a696e7566(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_349eda04bf.sparta_55a972dd5d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_f1b9fbcf0a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_c645f12831(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_dc62194d7c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_02dc241237(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_17cf7a1b5d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_0e8ad9a87b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_0543b8f3b8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a976df9130.sparta_7fc9396d78(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_9f700d2b8b(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_a976df9130.sparta_9f2ff40ab6(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_5dbe3eb082
def sparta_84f658dd55(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_a976df9130.sparta_06cdeae40d(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_5dbe3eb082
def sparta_30f543101e(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_a976df9130.sparta_e95565406c(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A