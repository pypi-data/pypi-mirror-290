_K='has_access'
_J='session'
_I='plot_name'
_H='plot_chart_id'
_G=False
_F='login'
_E='plot_db_chart_obj'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a as qube_f673e75e5a
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_cde414cdf7
from project.sparta_560fb5fd39.sparta_b63ad33d08 import qube_cf4251e798 as qube_cf4251e798
@csrf_exempt
@sparta_cde414cdf7
@login_required(redirect_field_name=_F)
def sparta_0e2b90db94(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_f673e75e5a.sparta_f06548cd94(B);A[_C]=7;D=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_cde414cdf7
@login_required(redirect_field_name=_F)
def sparta_ec6ffc008f(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_cf4251e798.sparta_82e7ee952c(C,A.user);D=not E[_K]
	if D:return sparta_0e2b90db94(A)
	B=qube_f673e75e5a.sparta_f06548cd94(A);B[_C]=7;F=qube_f673e75e5a.sparta_48f5515226(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_cde414cdf7
def sparta_ac7ab063d7(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_76bb5ac120(A,B)
@csrf_exempt
@sparta_cde414cdf7
def sparta_18b5b548da(request,widget_id,session_id,api_token_id):return sparta_76bb5ac120(request,widget_id,session_id)
def sparta_76bb5ac120(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_cf4251e798.sparta_4e84715a99(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_0e2b90db94(B)
	A=qube_f673e75e5a.sparta_f06548cd94(B);A[_C]=7;I=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_cde414cdf7
def sparta_1226a673e2(request,session_id,api_token_id):B=request;A=qube_f673e75e5a.sparta_f06548cd94(B);A[_C]=7;C=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_cde414cdf7
@login_required(redirect_field_name=_F)
def sparta_c7519877c0(request):
	J=',\n    ';B=request;C=B.GET.get('id');E=_G
	if C is _B:E=_A
	else:F=qube_cf4251e798.sparta_82e7ee952c(C,B.user);E=not F[_K]
	if E:return sparta_0e2b90db94(B)
	K=qube_cf4251e798.sparta_b97785b7ff(F[_E]);D='';G=0
	for(H,I)in K.items():
		if G>0:D+=J
		if I==1:D+=f"{H}=input_1"
		else:L=str(J.join([f"input_{A}"for A in range(I)]));D+=f"{H}=[{L}]"
		G+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_data(\n    "{C}",\n    {D}\n)';A=qube_f673e75e5a.sparta_f06548cd94(B);A[_C]=7;O=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=F[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_cde414cdf7
def sparta_b0a1d69f8e(request,session_id,api_token_id,json_vars_html):B=request;A=qube_f673e75e5a.sparta_f06548cd94(B);A[_C]=7;C=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)