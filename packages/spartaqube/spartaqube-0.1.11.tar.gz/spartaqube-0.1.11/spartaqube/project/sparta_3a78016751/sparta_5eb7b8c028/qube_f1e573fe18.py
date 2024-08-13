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
import project.sparta_02c008a725.sparta_27262642be.qube_ddd37178e0 as qube_ddd37178e0
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_ff6fcf4bef
from project.sparta_a1c64beb30.sparta_21e3337ca7 import qube_b35c843a0d as qube_b35c843a0d
@csrf_exempt
@sparta_ff6fcf4bef
@login_required(redirect_field_name=_F)
def sparta_951bd2caa6(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_ddd37178e0.sparta_5b682021d4(B);A[_C]=7;D=qube_ddd37178e0.sparta_37713924ea(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_ff6fcf4bef
@login_required(redirect_field_name=_F)
def sparta_f1b71dfdbb(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_b35c843a0d.sparta_80c856ab56(C,A.user);D=not E[_K]
	if D:return sparta_951bd2caa6(A)
	B=qube_ddd37178e0.sparta_5b682021d4(A);B[_C]=7;F=qube_ddd37178e0.sparta_37713924ea(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_ff6fcf4bef
def sparta_1a138ec323(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_fa65d3ab3a(A,B)
@csrf_exempt
@sparta_ff6fcf4bef
def sparta_970c9dea6e(request,widget_id,session_id,api_token_id):return sparta_fa65d3ab3a(request,widget_id,session_id)
def sparta_fa65d3ab3a(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_b35c843a0d.sparta_27d0b279ae(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_951bd2caa6(B)
	A=qube_ddd37178e0.sparta_5b682021d4(B);A[_C]=7;I=qube_ddd37178e0.sparta_37713924ea(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_ff6fcf4bef
def sparta_54f58cdd0a(request,session_id,api_token_id):B=request;A=qube_ddd37178e0.sparta_5b682021d4(B);A[_C]=7;C=qube_ddd37178e0.sparta_37713924ea(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_ff6fcf4bef
@login_required(redirect_field_name=_F)
def sparta_a63181c864(request):
	J=',\n    ';B=request;C=B.GET.get('id');E=_G
	if C is _B:E=_A
	else:F=qube_b35c843a0d.sparta_80c856ab56(C,B.user);E=not F[_K]
	if E:return sparta_951bd2caa6(B)
	K=qube_b35c843a0d.sparta_1bc6603a6c(F[_E]);D='';G=0
	for(H,I)in K.items():
		if G>0:D+=J
		if I==1:D+=f"{H}=input_1"
		else:L=str(J.join([f"input_{A}"for A in range(I)]));D+=f"{H}=[{L}]"
		G+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_data(\n    "{C}",\n    {D}\n)';A=qube_ddd37178e0.sparta_5b682021d4(B);A[_C]=7;O=qube_ddd37178e0.sparta_37713924ea(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=F[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_ff6fcf4bef
def sparta_a99e0c0899(request,session_id,api_token_id,json_vars_html):B=request;A=qube_ddd37178e0.sparta_5b682021d4(B);A[_C]=7;C=qube_ddd37178e0.sparta_37713924ea(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)