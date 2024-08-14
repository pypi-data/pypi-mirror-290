_A='utf-8'
import base64,hashlib
from cryptography.fernet import Fernet
def sparta_5a85088f38():B='db-conn';A=B.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A.decode(_A)
def sparta_067d8c87ea(password_to_encrypt):A=password_to_encrypt;A=A.encode(_A);C=Fernet(sparta_5a85088f38().encode(_A));B=C.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c6d95b856a(password_e):B=Fernet(sparta_5a85088f38().encode(_A));A=base64.b64decode(password_e);A=B.decrypt(A).decode(_A);return A
def sparta_05cf9541af():return sorted(['aerospike','arctic','cassandra','clickhouse','couchdb','csv','duckdb','influxdb','json_api','mariadb','mongo','mssql','mysql','oracle','parquet','postgres','python','questdb','redis','scylladb','sqlite','wss'])