_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_9142899a5a():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_b1337574d0(objectToCrypt):A=objectToCrypt;C=sparta_9142899a5a();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_b9076ed165(apiAuth):A=apiAuth;B=sparta_9142899a5a();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2fa5df8f98(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_78b6079f40(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_2fa5df8f98(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_77432b7293(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_2fa5df8f98(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_a29a7f4f48(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7abdbfa0cd(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_a29a7f4f48(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_0f6d17a55d(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_a29a7f4f48(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_fc9a451816(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7c2795f8e1(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_fc9a451816(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_6860802e3a(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_fc9a451816(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)