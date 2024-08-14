_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_12e8f1bdfd():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_527f4fbd4d(objectToCrypt):A=objectToCrypt;C=sparta_12e8f1bdfd();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a187e1bded(apiAuth):A=apiAuth;B=sparta_12e8f1bdfd();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2cb0ef8921(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7594b07eb1(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_2cb0ef8921(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_ce0d21e171(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_2cb0ef8921(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_20d68ce4b4(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_fbc777c149(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_20d68ce4b4(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_517bc96a48(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_20d68ce4b4(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_be66017d44(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f86b050fcf(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_be66017d44(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c2985b2e3a(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_be66017d44(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)