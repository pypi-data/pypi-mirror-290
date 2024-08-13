import os,json,platform,websocket,threading,time,pandas as pd
from project.sparta_a1c64beb30.sparta_21e3337ca7 import qube_b35c843a0d as qube_b35c843a0d
from project.sparta_a1c64beb30.sparta_30dfa55c71.qube_04cdeac192 import sparta_572804153f
from project.sparta_a1c64beb30.sparta_161e58683a.qube_5415a07c44 import Connector as Connector
IS_WINDOWS=False
if platform.system()=='Windows':IS_WINDOWS=True
from channels.generic.websocket import WebsocketConsumer
from project.sparta_02c008a725.sparta_27262642be import qube_ddd37178e0 as qube_ddd37178e0
from project.sparta_a1c64beb30.sparta_30dfa55c71 import qube_04cdeac192 as qube_04cdeac192
class WssConnectorWS(WebsocketConsumer):
	channel_session=True;http_user_and_session=True
	def connect(A):print('Connect Now');A.accept();A.user=A.scope['user'];A.json_data_dict=dict()
	def init_socket(B,json_data):
		A=json_data;D=A['is_model_connector'];B.connector_obj=Connector(db_engine='wss')
		if D:
			E=A['connector_id'];C=qube_b35c843a0d.sparta_3c8472bfc8(E,B.user)
			if C is None:F={'res':-2,'errorMsg':'Invalid connector, please try again'};G=json.dumps(F);B.send(text_data=G);return
			B.connector_obj.init_with_model(C)
		else:B.connector_obj.init_with_params(host=A['host'],port=A['port'],user=A['user'],password=A['password'],database=A['database'],oracle_service_name=A['oracle_service_name'],csv_path=A['csv_path'],csv_delimiter=A['csv_delimiter'],keyspace=A['keyspace'],library_arctic=A['library_arctic'],database_path=A['database_path'],read_only=A['read_only'],json_url=A['json_url'],socket_url=A['socket_url'],redis_db=A['redis_db'],dynamic_inputs=A['dynamic_inputs'],py_code_processing=A['py_code_processing'])
		B.connector_obj.get_db_connector().start_stream(gui_websocket=B)
	def disconnect(A,close_code):
		print('Disconnect')
		try:A.connector_obj.get_db_connector().stop_threads()
		except:pass
	def receive(A,text_data):
		E='service';C=text_data
		if len(C)>0:
			D=json.loads(C);B=D[E]
			if B=='init-socket':A.init_socket(D);F={'res':1,E:B};G=json.dumps(F);A.send(text_data=G)
			if B=='stop-socket':A.connector_obj.get_db_connector().stop_stream(gui_websocket=A)