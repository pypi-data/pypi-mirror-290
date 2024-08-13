from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_02c008a725.sparta_27262642be.qube_ddd37178e0 as qube_ddd37178e0
from project.models import UserProfile
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_ff6fcf4bef
from project.sparta_3a78016751.sparta_70dcb86b8d.qube_725467efde import sparta_e95e61aff4
@sparta_ff6fcf4bef
@login_required(redirect_field_name='login')
def sparta_65c20e2650(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_ddd37178e0.sparta_5b682021d4(B);A.update(qube_ddd37178e0.sparta_37713924ea(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_e95e61aff4());return render(B,'dist/project/auth/settings.html',A)