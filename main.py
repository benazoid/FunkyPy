import myParser
import Funky

dict = {
	"E": Funky.E,
	"PI": Funky.PI
}

def xSquared(x):
	return x * x
def twoX(x):
	return x + x

def main():
	print(Funky.inverseFunct(Funky.ln, Funky.inv, 2))

	line = ""
	while(line != "end"):
		line = input(":")
		node = myParser.Node.createNode(line)
		print(node.evaluate(dict))

main()
