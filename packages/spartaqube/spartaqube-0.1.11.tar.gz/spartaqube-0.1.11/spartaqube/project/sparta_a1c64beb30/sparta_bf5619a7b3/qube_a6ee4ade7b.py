import ast
def sparta_7826874f92(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_4e0f4f4486(script_text):return sparta_7826874f92(script_text)