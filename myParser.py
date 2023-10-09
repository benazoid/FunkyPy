
import Funky

FUNCTS_2IN = {
	'+': "add",
	'-': "sub",
	'*': "mult",
	'/': "div",
	'%': "mod",
	'^': "pow",
}


ORDER = [
	["^"],
	["*", "/", "%"],
	["+","-"]
]

allFuncts = ["add", "sub", "mult", "div", "pow", "mod", "exp", "log", "ln", "root", "sqrt", "abs", "sin", "cos", "tan"]

functDefs = [Funky.add, Funky.sub, Funky.mult, Funky.div, Funky.pow, Funky.mod, Funky.exp, Funky.log, Funky.ln, Funky.root, Funky.sqrt, Funky.abs, Funky.sin, Funky.cos, Funky.tan]

def replaceBounds(string, low, high, replace):
	# [ )
	return string[0:low] + replace + string[high:len(string)]
def replaceStr(subNodes):
	return '#' + str(len(subNodes)) + '#'
def getType(char):
	numChars = ['0','1','2','3','4','5','6','7','8','9','.']
	keys = FUNCTS_2IN.keys()
	if(char in numChars):
		return "num"
	elif(char in keys):
		return "none"
	return "str"

def findParenPair(content, parenInd):
	parenCt = 0
	if(content[parenInd] == '('):
		parenCt = 1
	index = parenInd + 1
	while(parenCt != 0 and index < len(content)):
		if(content[index] == '('):
			parenCt += 1
		elif(content[index] == ')'):
			parenCt -= 1
		index += 1
	return index


class Node:

	def __init__(self, data, funct):
		self.data = data
		self.funct = funct
		if(funct == "num"):
			data[0] = float(data[0])

	@staticmethod
	def parseParens(content, subNodes):
		paren0 = content.find('(')
		parenInd = findParenPair(content,paren0)
		while(parenInd > 0):
			create = (content[paren0 + 1 : parenInd - 1])
			content = replaceBounds(content, paren0, parenInd + 1, replaceStr(subNodes))
			subNodes.append(Node.createNode(create))
			paren0 = content.find('(')
			parenInd = findParenPair(content,paren0)
		return content
	@staticmethod
	def parseFuncts(content, subNodes):
		for funct in allFuncts:
			functInd = content.find(funct)
			while(functInd >= 0):
				functInd += (len(funct) + 1)
				nodeInd = int(content[functInd : content.find('#', functInd)])

				content = content.replace(funct + '#' + str(nodeInd) + '#', replaceStr(subNodes))
				subNodes.append(Node([subNodes[nodeInd]], funct))
				functInd = content.find(funct)
		return content
	@staticmethod
	def parseCommas(content, subNodes):
		functNodes = []
		start = 0
		commaInd = content.find(',')
		if(commaInd >= 0):
			content += ','
			while(commaInd >= 0):
				functNodes.append(Node.createNode(content[start : commaInd]))
				start = commaInd + 1
				commaInd = content.find(',', start)

			content = replaceStr(subNodes)
			subNodes.append(Node(functNodes, "inputs"))
		return content
	@staticmethod
	def parseBases(content, subNodes):
		current0 = 0
		index = 0
		while(index < len(content)):
			if(content[index] == '#'):
				nextInd = content.find('#',index + 1)
				index = nextInd + 1

			if(index >= len(content)):
				return content

			currType = getType(content[index])
			typ = currType
			while(typ == currType and index < len(content)):
				index += 1
				try:
					typ = getType(content[index])
				except IndexError:
					typ == "none"

			if(currType != "none" and content[current0 : index] != ""):
				replace = replaceStr(subNodes)
				print(content[current0 : index])
				subNodes.append(Node([content[current0 : index]], currType))
				content = replaceBounds(content, current0, index, replace)
				index += (len(replace) - (index-current0))
			
			current0 = index

		return content
	@staticmethod
	def parseOperators(content, subNodes):
		keys = FUNCTS_2IN.keys()

		# deal with stray + or - (pos or neg)
		if(content[0] == '+'):
			content = content.replace('+', "", 1)
		if(content[0] == '-'):
			replace = '#' + str(len(subNodes)) + '#'
			content = content.replace('-', replace, 1)
			subNodes.append(Node([-1], "num"))

		for k in keys:
			searchPos = content.find(k, 0)
			while(searchPos >= 0):
				if(content[searchPos + 1] == '+'):
					content = replaceBounds(content, searchPos + 1, searchPos + 2, "")
				if(content[searchPos + 1] == '-'):
					content = replaceBounds(content, searchPos + 1, searchPos + 2, replaceStr(subNodes))
					subNodes.append(Node([-1], "num"))
				searchPos = content.find(k, searchPos + 1)

		# deal with normal ops
		content = content.replace("##","#*#")
		for level in ORDER:
			while(True):
				first = content.find(level[0])
				for op in level:
					opBest = content.find(op)
					if(opBest != -1 and opBest < first or first < 0):
						first = opBest
				if(first < 0):
					break

				index1 = ""
				index2 = ""
				opChar = content[first]

				index = first
				hashCt = 0
				while(hashCt < 2 or index > len(content)):
					index -= 1
					if(content[index] == '#'):
						hashCt += 1
					else:
						index1 = content[index] + index1

				index = first
				hashCt = 0
				while(hashCt < 2 or index < 0):
					index += 1
					if(content[index] == '#'):
						hashCt += 1
					else:
						index2 += content[index]

				content = content.replace('#' + index1 + '#' + opChar + '#' + index2 + '#', replaceStr(subNodes))

				index1 = int(index1)
				index2 = int(index2)

				subNodes.append(Node([subNodes[index1],subNodes[index2]],FUNCTS_2IN[opChar]))

		return content

	@staticmethod
	def createNode(content):
		subNodes = []

		content = Node.parseParens(content, subNodes)

		content = Node.parseFuncts(content, subNodes)

		content = Node.parseCommas(content, subNodes)

		content = Node.parseBases(content, subNodes)

		content = Node.parseOperators(content, subNodes)

		return Node([subNodes[int(content[1:len(content)-1])]],"")

	def evaluate(self, dict):
		if(self.funct == "num"):
			return self.data[0]
		if(self.funct == "str"):
			return dict[self.data[0]]
		if(self.funct == ''):
			return self.data[0].evaluate(dict)
		evaled = []
		fun = functDefs[allFuncts.index(self.funct)]
		for d in self.data:
			evaled.append(d.evaluate(dict))
		return fun(*evaled)

	def toString(self):
		if(self.funct == "num" or self.funct == "str"):
			return str(self.data[0])
		string = self.funct + '('
		for d in self.data:
			string += d.toString() + ','
		string += ')'
		return string
