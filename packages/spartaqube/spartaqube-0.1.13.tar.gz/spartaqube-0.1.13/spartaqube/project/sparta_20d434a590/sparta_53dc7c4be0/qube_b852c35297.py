from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_1dc24a2641
from project.sparta_cb7699d1a4.sparta_c275093f31 import qube_8fc188c7d8 as qube_8fc188c7d8
from project.models import UserProfile
import project.sparta_7ea42ed2bd.sparta_4b6986daa6.qube_8d44c27597 as qube_8d44c27597
@sparta_1dc24a2641
@login_required(redirect_field_name='login')
def sparta_43cdf6c58e(request):
	E='avatarImg';B=request;A=qube_8d44c27597.sparta_eacc3c863b(B);A['menuBar']=-1;F=qube_8d44c27597.sparta_981707199d(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_1dc24a2641
@login_required(redirect_field_name='login')
def sparta_d8c2d7cc96(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_43cdf6c58e(A)