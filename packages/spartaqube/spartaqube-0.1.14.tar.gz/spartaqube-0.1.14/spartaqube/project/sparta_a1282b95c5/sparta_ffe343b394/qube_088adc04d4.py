_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_cb7699d1a4.sparta_6294b0b4ef import qube_750b7a5ec9 as qube_750b7a5ec9
from project.sparta_cb7699d1a4.sparta_c275093f31 import qube_8fc188c7d8 as qube_8fc188c7d8
from project.sparta_cb7699d1a4.sparta_67553e9f2a.qube_7480dd05a3 import sparta_5dbe3eb082
@csrf_exempt
@sparta_5dbe3eb082
def sparta_9e7caef723(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_8fc188c7d8.sparta_bf484c712a(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_750b7a5ec9.sparta_9e7caef723(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_5dbe3eb082
def sparta_a8cc9bd320(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_750b7a5ec9.sparta_ab94fb760a(C,A.user);E=json.dumps(D);return HttpResponse(E)