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
from project.sparta_a1c64beb30.sparta_6eb9a5f606 import qube_8c00c9c977 as qube_8c00c9c977
from project.sparta_a1c64beb30.sparta_6eb9a5f606 import qube_18ac50fe85 as qube_18ac50fe85
from project.sparta_a1c64beb30.sparta_30dfa55c71 import qube_04cdeac192 as qube_04cdeac192
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_8ca5be44d2
@csrf_exempt
@sparta_8ca5be44d2
def sparta_4b25d944ab(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_8c00c9c977.sparta_d0f1d007ba(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_96b1c55c84(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_9ba75b06ab(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_363cc0a088(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_5afba87b38(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_8dae9ce112(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_2a5f0dbcd4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_a9a10219da(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_18ac50fe85.sparta_c7b28a3f5d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_c3fbd2977f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_805ac17435(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_36d2e28da0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_2093a666cc(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_e0b96bbcb0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_2576bff371(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_e31a295dea(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8c00c9c977.sparta_ee53bd9e16(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_9dabe36ff0(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_8c00c9c977.sparta_f71e28451a(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_8ca5be44d2
def sparta_f44b8c61cf(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_8c00c9c977.sparta_a645d2095c(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_8ca5be44d2
def sparta_1143fc0030(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_8c00c9c977.sparta_9d36c88c4f(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A