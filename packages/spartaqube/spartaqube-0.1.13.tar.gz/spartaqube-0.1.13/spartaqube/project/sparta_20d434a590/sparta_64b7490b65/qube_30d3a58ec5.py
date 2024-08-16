from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_7ea42ed2bd.sparta_4b6986daa6.qube_8d44c27597 as qube_8d44c27597
from project.models import UserProfile
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_1dc24a2641
from project.sparta_20d434a590.sparta_f6f1fe2899.qube_b18eda0382 import sparta_95196b127a
@sparta_1dc24a2641
@login_required(redirect_field_name='login')
def sparta_641a8a1571(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_8d44c27597.sparta_eacc3c863b(B);A.update(qube_8d44c27597.sparta_981707199d(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_95196b127a());return render(B,'dist/project/auth/settings.html',A)