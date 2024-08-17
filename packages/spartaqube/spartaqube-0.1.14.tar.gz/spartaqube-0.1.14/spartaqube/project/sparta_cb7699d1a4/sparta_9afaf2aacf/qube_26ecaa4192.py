import ast
def sparta_64f04cc465(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_ebce0d45e6(script_text):return sparta_64f04cc465(script_text)