import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_cb7699d1a4.sparta_4de2b55eed import qube_779c4686ef as qube_779c4686ef
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_5dbe3eb082
@csrf_exempt
@sparta_5dbe3eb082
def sparta_47c90f6dd6(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_779c4686ef.sparta_47c90f6dd6(B,A.user);I=json.dumps(H);return HttpResponse(I)