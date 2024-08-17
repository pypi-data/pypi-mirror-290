import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_5dbe3eb082
from project.sparta_cb7699d1a4.sparta_ba9a65d88e import qube_d62170b00a as qube_d62170b00a
@csrf_exempt
@sparta_5dbe3eb082
def sparta_50a391d4d0(request):A=request;B=json.loads(A.body);C=json.loads(B['jsonData']);D=A.user;E=qube_d62170b00a.sparta_50a391d4d0(C,D);F=json.dumps(E);return HttpResponse(F)