import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_cb7699d1a4.sparta_c510742199 import qube_3f29290233 as qube_3f29290233
from project.sparta_cb7699d1a4.sparta_ab3246baf1 import qube_dc1adaef53
from project.sparta_cb7699d1a4.sparta_6d1c901dee import qube_6b4f96c9f7 as qube_6b4f96c9f7
from project.sparta_cb7699d1a4.sparta_ab3246baf1.qube_e76e202b16 import Connector as Connector
def sparta_47c90f6dd6(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_1062087095(B)
	return{'res':1,'output':C,D:B}
def sparta_1062087095(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]