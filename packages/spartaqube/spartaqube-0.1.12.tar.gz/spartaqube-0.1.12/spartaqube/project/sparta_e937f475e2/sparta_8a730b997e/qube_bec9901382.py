from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_cde414cdf7
from project.sparta_560fb5fd39.sparta_99796ceac3 import qube_a90bf9236c as qube_a90bf9236c
from project.models import UserProfile
import project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a as qube_f673e75e5a
@sparta_cde414cdf7
@login_required(redirect_field_name='login')
def sparta_adaf9e6190(request):
	E='avatarImg';B=request;A=qube_f673e75e5a.sparta_f06548cd94(B);A['menuBar']=-1;F=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_cde414cdf7
@login_required(redirect_field_name='login')
def sparta_e47115a294(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_adaf9e6190(A)