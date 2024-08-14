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
from project.sparta_560fb5fd39.sparta_09712e09ec import qube_c8cecf739b as qube_c8cecf739b
from project.sparta_560fb5fd39.sparta_09712e09ec import qube_4a75ca07bf as qube_4a75ca07bf
from project.sparta_560fb5fd39.sparta_182eae079f import qube_53105bc5e5 as qube_53105bc5e5
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_f076ba2889
@csrf_exempt
@sparta_f076ba2889
def sparta_3127584c29(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_c8cecf739b.sparta_6e84a3fcfe(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_f076ba2889
def sparta_ed800313d5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_6b2ae25455(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_c444fa9ca5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_eabb20d474(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_895c5d77ca(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_98f730f705(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_e47cdab2d2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4a75ca07bf.sparta_958430498f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_3c95f74ee6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_b89fd1fbac(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_845ada5bf4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_1dbd6a417e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_9328f51106(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_25ca8b097b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_053cdea98c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c8cecf739b.sparta_882253a7ce(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f076ba2889
def sparta_96554e6ea6(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_c8cecf739b.sparta_089b5b14ac(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_f076ba2889
def sparta_cbf996fc5e(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_c8cecf739b.sparta_ee0bc81dfb(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_f076ba2889
def sparta_72218caf76(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_c8cecf739b.sparta_7f054fd86f(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A