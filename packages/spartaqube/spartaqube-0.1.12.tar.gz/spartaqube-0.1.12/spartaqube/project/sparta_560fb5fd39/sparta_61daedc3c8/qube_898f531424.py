_H='session_id'
_G='notebook_variables'
_F='errorMsg'
_E='session'
_D=False
_C=None
_B='utf-8'
_A='res'
import os,json,ast,base64,uuid,hashlib,cloudpickle
from random import randint
import pandas as pd
from cryptography.fernet import Fernet
from subprocess import PIPE
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.cache import cache
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared,CodeEditorNotebook
from project.models import ShareRights,UserProfile,NewPlotApiVariables
from project.sparta_560fb5fd39.sparta_6f25bc549c import qube_578150723d as qube_578150723d
from project.sparta_560fb5fd39.sparta_b63ad33d08 import qube_cf4251e798 as qube_cf4251e798
from project.sparta_560fb5fd39.sparta_182eae079f.qube_53105bc5e5 import sparta_dc18dcc477,sparta_b07bd8c600
from project.sparta_560fb5fd39.sparta_182eae079f.qube_600340f353 import sparta_0ab07f545c
from project.sparta_560fb5fd39.sparta_182eae079f.qube_600340f353 import sparta_8d00795a14
def sparta_b629593d4f():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_3f5c771dc4():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_495d225ff4(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_fe04e0e454(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(username='public_spartaqube').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_3f5c771dc4().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_D).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:print('Could not authenticate api with error msg:');print(e);return
def sparta_b1abeb7b5a(json_data,user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _C:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	domain_name=json_data['domain'];random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_3f5c771dc4().encode(_B));private_encryption=sparta_495d225ff4(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_b629593d4f().encode(_B));public_encryption=sparta_495d225ff4(f_public,data_to_encrypt);return{_A:1,'token':public_encryption}
def sparta_81c9e649d9(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_467cd82b71():plot_types=sparta_0ab07f545c();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_D);return{_A:1,'plot_types':plot_types}
def sparta_260dc2a14a(json_data):plot_type=json_data['plot_type'];plot_input_options_dict=sparta_8d00795a14(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_76d46f9e99(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_8849d22e1a(json_data):
	user_code_example=json_data['userCode'];resp=_C;error_msg=''
	try:
		exec(user_code_example,globals(),locals());last_expression_str=sparta_76d46f9e99(user_code_example)
		if last_expression_str is not _C:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			resp=json.dumps(resp);return{_A:1,'resp':resp,_F:error_msg}
	except Exception as e:return{_A:-1,_F:str(e)}
def sparta_620818c254(json_data,user_obj):
	session_id=json_data[_E];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();print(f"gui_plot_api_variables with session_id {session_id}");print(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=sparta_dc18dcc477(notebook_variable)
			if notebook_variables_df is not _C:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(sparta_b07bd8c600(notebook_variables_df))
		print(notebook_variables);return{_A:1,_G:notebook_variables}
	return{_A:-1}
def sparta_8fd5a6e7d7(json_data,user_obj):session_id=json_data[_E];notebook_cached_variables=qube_cf4251e798.sparta_5a05183e71(session_id);return{_A:1,_G:notebook_cached_variables}
def sparta_494b73094f(json_data,user_obj):session_id=json_data[_E];return qube_cf4251e798.sparta_6fcbf11e32(session_id)
def sparta_c0fc59ec6d(json_data,user_obj):session_id=json_data[_E];widget_id=json_data['widgetId'];return qube_cf4251e798.sparta_c0fc59ec6d(user_obj,session_id,widget_id)
def sparta_5df44716f0(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_c47d5dc41c()
	elif api_service=='get_connectors':return sparta_48389ec7c6(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_2167e301da(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_1b4afe4632(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_7bf87ace65(user_obj)
	elif api_service=='get_widget_data':return sparta_18f4bd25bc(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_0ab07f545c()
	elif api_service=='gui_plot_api_variables':return sparta_4bbae40768(json_data,user_obj,b_check_type=_D)
	elif api_service=='plot_cache_variables':return sparta_4bbae40768(json_data,user_obj)
	elif api_service=='clear_cache':return sparta_a621b973af()
	return{_A:1,'output':output}
def sparta_c47d5dc41c():return 1
def sparta_48389ec7c6(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id','name','db_engine'];res_dict=qube_cf4251e798.sparta_c2d8b9ac68(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_2167e301da(json_data,user_obj):res_dict=qube_cf4251e798.sparta_fe339b5aca(json_data,user_obj);return res_dict
def sparta_1b4afe4632(json_data,user_obj):res_dict=qube_cf4251e798.sparta_5253148b63(json_data,user_obj);return res_dict
def sparta_7bf87ace65(user_obj):return qube_cf4251e798.sparta_0c2d3611fe(user_obj)
def sparta_18f4bd25bc(json_data,user_obj):return qube_cf4251e798.sparta_bd91bcf24b(json_data,user_obj)
def sparta_475c5c86e1(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,_H:session_id}
def sparta_52871218dd():return sparta_0ab07f545c()
def sparta_4bbae40768(json_data,user_obj,b_check_type=True):
	A='cache_hash';variables_dict=json_data['variables']
	if b_check_type:
		chart_type_check=variables_dict['chart_type_check']
		if chart_type_check not in[elem['ID']for elem in sparta_0ab07f545c()]:return{_A:-1,_F:'Invalid chart_type input'}
	plot_params=json_data['plot_params'];all_hash_notebook=json_data['all_hash_notebook'];all_hash_server=json_data['all_hash_server'];b_missing_cache=_D
	for this_hash in all_hash_server:
		if cache.get(this_hash)is _C:b_missing_cache=True;break
	if b_missing_cache:
		cache_hash=[]
		for this_hash in all_hash_notebook:
			if cache.get(this_hash)is not _C:cache_hash.append(this_hash)
		return{_A:-1,'status_service':1,A:cache_hash}
	session_id=str(uuid.uuid4());cache.set(session_id,plot_params,timeout=_C)
	for(key,val)in variables_dict.items():
		if isinstance(val,dict):
			hash=val['hash'];hash_value_cache=cache.get(hash)
			if hash_value_cache is _C:hash_value_input=val.get('var',_C);cache.set(hash,hash_value_input,timeout=_C);print(f"Set hash {hash} for {key}")
	cache_hash=[]
	for this_hash in all_hash_notebook:
		if cache.get(this_hash)is not _C:cache_hash.append(this_hash)
	return{_A:1,_H:session_id,A:cache_hash}
def sparta_a621b973af():cache.clear();return{_A:1}