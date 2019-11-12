import sys
import re
 

class Stack:
  def __init__(self):
    self.__storage = []

  def empty(self):
    return len(self.__storage) == 0

  def push(self,p):
    self.__storage.append(p)

  def pop(self):
    return self.__storage.pop()

  def __str__(self):
    return str(self.__storage)

  def top(self):
  	return self.__storage[len(self.__storage)-1]


def lex(characters, token_exps):
	pos = 0
	tokens = []
	while pos < len(characters):
		match = None
		for token_exp in token_exps:
			pattern , tag = token_exp
			regex = re.compile(pattern)
			match = regex.match(characters, pos)
			if match:
				text = match.group(0)
				if tag:
					token = (text,tag)
					tokens.append(token)
				break
		if not match:
			sys.stderr.write("Illegal character : %s\\n"%characters[pos])
			sys.exit(1)
		else:
			pos = match.end(0)
	return tokens


RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'
FLOAT    = 'FLOAT'

token_exps = [
    (r'[ \n\t]+',          			None),
    (r'#[^\n]*',           			None),
    (r'\:=',              			RESERVED),
    (r'\(',                			RESERVED),
    (r'\)',                			RESERVED),
    (r';',                 			RESERVED),
    (r'\+',                			RESERVED),
    (r'-',                 			RESERVED),
    (r'\*',                			RESERVED),
    (r'/',                    		RESERVED),
    (r'end',                   		RESERVED),
    (r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',			FLOAT),
    (r'[0-9]+',                		INT),
    (r'[A-Za-z][A-Za-z0-9_]*', 		ID)

]

def imp_lex(characters):
	return lex(characters,token_exps)


def operation(op , n, m):
	if op=="+":
		return float(n)+float(m)
	elif op== "-":
		return float(m)-float(n)
	elif op=="*":
		return float(n)*float(m)
	elif op=="/":
		if n ==0 :
			raise ValueError('can not divide by zero')
		else:
			return int(m)/int(n)


def haspre(op1, op2):
	if op2 =="(" or op1==")":
		return False
	elif  (op1 == '*' or op1 == '/') and (op2 == '+' or op2 == '-'):
		return False
	else:
		return True


def main():
	run = "run"
	flag= sys.argv[1]
	if(flag == run):
		print(">>>", end=' ')
		characters = input()
		while characters!= "end":
			tokens = imp_lex(characters)
			ans = 0
			# ids = []
			s = Stack()
			op = Stack()
			fl = 1
			for token in tokens:
				if token[1]== "INT" or token[1]== "FLOAT":
					s.push(token[0])

				elif token[0]=="(":
					op.push(token[0])

				elif token[0]==")":
					while op.top() != "(" and op.empty() ==False:
						s.push(operation(op.pop(),s.pop(),s.pop()))
					op.pop()
						
				elif token[0]=="+" or token[0]== "-" or token[0]=="*" or token[0]=="/":
					while op.empty()== False and haspre(token[0],op.top()):
						s.push(operation(op.pop(),s.pop(),s.pop()))
					op.push(token[0])
				else:
					print("error in syntax "+token[0])
					return

			while op.empty()== False:
				s.push(operation(op.pop(),s.pop(),s.pop()))

				
					
			print("Calculator gives answer as :", s.pop())
			characters = input(">>> ")
		# print("running")
		else:
			return
	else:
		print("write 'run' to start the interpreter and 'end' to kill it")
		
	

if __name__ == '__main__':
	main()
