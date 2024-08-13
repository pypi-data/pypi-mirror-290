_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_a1c64beb30.sparta_43614d3d0c import qube_70654e7d00 as qube_70654e7d00
from project.sparta_a1c64beb30.sparta_005756b899 import qube_52b6c4a2dd as qube_52b6c4a2dd
from project.sparta_a1c64beb30.sparta_d5a4a4b037.qube_53339f257e import sparta_8ca5be44d2
@csrf_exempt
@sparta_8ca5be44d2
def sparta_f73268eed6(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_52b6c4a2dd.sparta_9a990e68c7(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_70654e7d00.sparta_f73268eed6(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_8ca5be44d2
def sparta_3fd0552109(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70654e7d00.sparta_628c76b463(C,A.user);E=json.dumps(D);return HttpResponse(E)