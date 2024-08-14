import os,json,base64,json
def sparta_19d5e0e1f6():A=os.path.dirname(__file__);B=os.path.dirname(A);return json.loads(open(B+'/platform.json').read())['PLATFORM']
def sparta_055c3ebf2d(b):return base64.b64decode(b).decode('utf-8')
def sparta_61b1d1c6d2(s):return base64.b64encode(s.encode('utf-8'))