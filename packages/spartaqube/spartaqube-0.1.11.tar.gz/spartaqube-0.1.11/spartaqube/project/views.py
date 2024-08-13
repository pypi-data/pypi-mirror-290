import os,json,base64,json
def sparta_ea7e54df00():A=os.path.dirname(__file__);B=os.path.dirname(A);return json.loads(open(B+'/platform.json').read())['PLATFORM']
def sparta_179ecbd6f0(b):return base64.b64decode(b).decode('utf-8')
def sparta_23b61dd6b6(s):return base64.b64encode(s.encode('utf-8'))