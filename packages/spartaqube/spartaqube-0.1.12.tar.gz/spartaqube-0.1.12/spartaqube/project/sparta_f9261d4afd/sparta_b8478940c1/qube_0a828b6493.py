_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_560fb5fd39.sparta_807a69b80d import qube_62bde84090 as qube_62bde84090
from project.sparta_560fb5fd39.sparta_99796ceac3 import qube_a90bf9236c as qube_a90bf9236c
from project.sparta_560fb5fd39.sparta_ec245d0f93.qube_6a153c9958 import sparta_f076ba2889
@csrf_exempt
@sparta_f076ba2889
def sparta_c6d6af1d81(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_a90bf9236c.sparta_8d1f84c29b(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_62bde84090.sparta_c6d6af1d81(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_f076ba2889
def sparta_a918720494(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_62bde84090.sparta_ecd65e0514(C,A.user);E=json.dumps(D);return HttpResponse(E)