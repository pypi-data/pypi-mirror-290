import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_a1c64beb30.sparta_a1a910a51f import qube_53baa17931 as qube_53baa17931
from project.sparta_a1c64beb30.sparta_161e58683a import qube_d5ae4ab5b8
from project.sparta_a1c64beb30.sparta_21e3337ca7 import qube_10eb74ee26 as qube_10eb74ee26
from project.sparta_a1c64beb30.sparta_161e58683a.qube_5415a07c44 import Connector as Connector
def sparta_7cd04ed1e1(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_2c94ffa997(B)
	return{'res':1,'output':C,D:B}
def sparta_2c94ffa997(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]