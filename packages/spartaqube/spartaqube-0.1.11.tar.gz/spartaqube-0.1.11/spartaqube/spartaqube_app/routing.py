import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_02c008a725.sparta_d5cd08ed37 import qube_a6d75df4b2,qube_b7885715b4
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_2a7741b88a(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/notebookWS',sparta_2a7741b88a(qube_a6d75df4b2.NotebookWS)),url('ws/wssConnectorWS',sparta_2a7741b88a(qube_b7885715b4.WssConnectorWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)