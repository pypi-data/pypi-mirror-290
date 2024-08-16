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
import project.sparta_7ea42ed2bd.sparta_4b6986daa6.qube_8d44c27597 as qube_8d44c27597
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_1dc24a2641
from project.sparta_cb7699d1a4.sparta_6d1c901dee import qube_db955a6690 as qube_db955a6690
@csrf_exempt
@sparta_1dc24a2641
@login_required(redirect_field_name=_F)
def sparta_0d3c208302(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_8d44c27597.sparta_eacc3c863b(B);A[_C]=7;D=qube_8d44c27597.sparta_981707199d(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_1dc24a2641
@login_required(redirect_field_name=_F)
def sparta_9f3494f45c(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_db955a6690.sparta_80ecee9724(C,A.user);D=not E[_K]
	if D:return sparta_0d3c208302(A)
	B=qube_8d44c27597.sparta_eacc3c863b(A);B[_C]=7;F=qube_8d44c27597.sparta_981707199d(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_1dc24a2641
def sparta_fd47f49610(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_f7f15195bb(A,B)
@csrf_exempt
@sparta_1dc24a2641
def sparta_76280e73f6(request,widget_id,session_id,api_token_id):return sparta_f7f15195bb(request,widget_id,session_id)
def sparta_f7f15195bb(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_db955a6690.sparta_dcc80e34a9(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_0d3c208302(B)
	A=qube_8d44c27597.sparta_eacc3c863b(B);A[_C]=7;I=qube_8d44c27597.sparta_981707199d(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_1dc24a2641
def sparta_4968ac6f6d(request,session_id,api_token_id):B=request;A=qube_8d44c27597.sparta_eacc3c863b(B);A[_C]=7;C=qube_8d44c27597.sparta_981707199d(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_1dc24a2641
@login_required(redirect_field_name=_F)
def sparta_36996e379d(request):
	J=',\n    ';B=request;C=B.GET.get('id');E=_G
	if C is _B:E=_A
	else:F=qube_db955a6690.sparta_80ecee9724(C,B.user);E=not F[_K]
	if E:return sparta_0d3c208302(B)
	K=qube_db955a6690.sparta_3f96f52071(F[_E]);D='';G=0
	for(H,I)in K.items():
		if G>0:D+=J
		if I==1:D+=f"{H}=input_1"
		else:L=str(J.join([f"input_{A}"for A in range(I)]));D+=f"{H}=[{L}]"
		G+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_data(\n    "{C}",\n    {D}\n)';A=qube_8d44c27597.sparta_eacc3c863b(B);A[_C]=7;O=qube_8d44c27597.sparta_981707199d(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=F[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_1dc24a2641
def sparta_ecbf367241(request,session_id,api_token_id,json_vars_html):B=request;A=qube_8d44c27597.sparta_eacc3c863b(B);A[_C]=7;C=qube_8d44c27597.sparta_981707199d(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)