from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_ff6fcf4bef
from project.sparta_a1c64beb30.sparta_005756b899 import qube_52b6c4a2dd as qube_52b6c4a2dd
from project.models import UserProfile
import project.sparta_02c008a725.sparta_27262642be.qube_ddd37178e0 as qube_ddd37178e0
@sparta_ff6fcf4bef
@login_required(redirect_field_name='login')
def sparta_cf10e083e5(request):
	E='avatarImg';B=request;A=qube_ddd37178e0.sparta_5b682021d4(B);A['menuBar']=-1;F=qube_ddd37178e0.sparta_37713924ea(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_ff6fcf4bef
@login_required(redirect_field_name='login')
def sparta_0e386db8ab(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_cf10e083e5(A)