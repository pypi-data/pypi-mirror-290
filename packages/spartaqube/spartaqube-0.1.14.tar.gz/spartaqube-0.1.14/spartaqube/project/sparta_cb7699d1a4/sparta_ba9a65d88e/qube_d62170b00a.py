import os,json,base64,subprocess,pandas as pd
from datetime import datetime,timedelta
from dateutil import parser
import pytz
UTC=pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils.text import Truncator
from django.db.models import CharField,TextField
from django.db.models.functions import Lower
CharField.register_lookup(Lower)
TextField.register_lookup(Lower)
from project.models import User,UserProfile,PlotDBChart,PlotDBChartShared
from project.sparta_cb7699d1a4.sparta_c510742199 import qube_3f29290233 as qube_3f29290233
from project.sparta_cb7699d1a4.sparta_bb3c98daf4 import qube_c678b063ce as qube_c678b063ce
def sparta_99f7e83369(user_obj):
	A=qube_3f29290233.sparta_feddd5b291(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_50a391d4d0(json_data,user_obj):
	J='widgets';B=user_obj;C=json_data['keyword'].lower();E=120;F=sparta_99f7e83369(B)
	if len(F)>0:D=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=F,plot_db_chart__is_delete=0,plot_db_chart=A,plot_db_chart__name__lower__icontains=C)|Q(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart__name__lower__icontains=C))
	else:D=PlotDBChartShared.objects.filter(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart__name__lower__icontains=C)
	K=D.count();G=[]
	for L in D[:5]:A=L.plot_db_chart;G.append({'plot_chart_id':A.plot_chart_id,'type_chart':A.type_chart,'name':A.name,'name_trunc':Truncator(A.name).chars(E),'description':A.description,'description_trunc':Truncator(A.description).chars(E)})
	H=0;I={J:K}
	for(N,M)in I.items():H+=M
	return{'res':1,J:G,'cntTotal':H,'counter_dict':I}