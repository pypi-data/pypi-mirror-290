from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib,project.sparta_8aa5a7c835.sparta_9e21739670.qube_f673e75e5a as qube_f673e75e5a
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_cde414cdf7
@csrf_exempt
def sparta_e064b2c3e2(request):B=request;A=qube_f673e75e5a.sparta_f06548cd94(B);A['menuBar']=8;A['bCodeMirror']=True;C=qube_f673e75e5a.sparta_48f5515226(B.user);A.update(C);return render(B,'dist/project/api/api.html',A)