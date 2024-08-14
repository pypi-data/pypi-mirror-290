import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_560fb5fd39.sparta_6f25bc549c import qube_578150723d as qube_578150723d
from project.sparta_560fb5fd39.sparta_98436de52f import qube_4efb9f6ee6
from project.sparta_560fb5fd39.sparta_b63ad33d08 import qube_cdd031e311 as qube_cdd031e311
from project.sparta_560fb5fd39.sparta_98436de52f.qube_4c7608ef5a import Connector as Connector
def sparta_d3f9482d44(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_4a3511fe07(B)
	return{'res':1,'output':C,D:B}
def sparta_4a3511fe07(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]