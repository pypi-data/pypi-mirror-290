_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_d10a8a48e3():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_047e766ec8(objectToCrypt):A=objectToCrypt;C=sparta_d10a8a48e3();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_3f6f50bb52(apiAuth):A=apiAuth;B=sparta_d10a8a48e3();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_97499e8897(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7988223f61(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_97499e8897(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_73be47e4d9(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_97499e8897(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_ebb1c4a055(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e27549c7fd(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_ebb1c4a055(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_0a4cba20e8(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_ebb1c4a055(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_f6b669d817(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_ab6d025350(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_f6b669d817(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_adb120c45c(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_f6b669d817(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)