_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_560fb5fd39.sparta_98436de52f.qube_4efb9f6ee6 as qube_4efb9f6ee6
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_76c3f76a5b.qube_1494cc3c7e import ArcticConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_22e1512465.qube_e4a75aedc3 import AerospikeConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_8d4241e3e5.qube_d330bd56ff import CassandraConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_6da0f919a4.qube_5089da26cb import ClickhouseConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_94dab28882.qube_be465ca3b2 import CouchdbConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_596276909f.qube_f83969419a import CsvConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_128e34b02d.qube_5744d2b504 import DuckDBConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_28a3bac54f.qube_b1d2bd940a import JsonApiConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_6cee05d961.qube_9327596251 import InfluxdbConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_68aa3541fd.qube_b93532b0ff import MariadbConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_2930860aaf.qube_011de89e96 import MongoConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_312bdb4de8.qube_9231978ae7 import MssqlConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_a1d4c4f693.qube_0fd755acf3 import MysqlConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_971f227fab.qube_e99a9f5652 import OracleConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_7ab28e85ad.qube_890d2f293d import ParquetConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_5083c3d9b2.qube_74afcde213 import PostgresConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_c8ff4fdb56.qube_00503130d9 import PythonConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_ce647baa27.qube_fdff4075db import QuestDBConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_828510f18a.qube_1b5dba64be import RedisConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_246639c58e.qube_498b2bc061 import ScylladbConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_377015b678.qube_9956c77e53 import SqliteConnector
from project.sparta_560fb5fd39.sparta_98436de52f.sparta_de0a1d4cb6.qube_45a672ba67 import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_4efb9f6ee6.sparta_c6d95b856a(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host;print('self.db_engine > '+str(A.db_engine))
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='arctic':A.db_connector=ArcticConnector(database_path=G,library_arctic=library_arctic)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_C:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_B:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_d7bbfc28e7(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)