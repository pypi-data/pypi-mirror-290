from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a as qube_f673e75e5a
from project.models import UserProfile
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_cde414cdf7
from project.sparta_e937f475e2.sparta_228b35792f.qube_dc7c943f64 import sparta_a8f1b938bf
@sparta_cde414cdf7
@login_required(redirect_field_name='login')
def sparta_4eda064f4e(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_f673e75e5a.sparta_f06548cd94(B);A.update(qube_f673e75e5a.sparta_48f5515226(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_a8f1b938bf());return render(B,'dist/project/auth/settings.html',A)