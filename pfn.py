from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="filename", 
                    help="read footnotes input", metavar="FILE", required=True)
parser.add_argument("-w", "--write", dest="filenameOut", 
                    help="write footnotes to file", metavar="OUTPUT", required=True)
parser.add_argument("-t", "--try", 
                    action="store_true", dest="verbose", default=False,
                    help="just a run without realy parsing the document")

args = parser.parse_args()

f = open(args.filename, "r")
fn = f.read().split("\n\n")
f2 = open(args.filenameOut, "r")
document = f2.read()
for footn in fn:
	number = footn.split(" ",1)[0].strip()
	text = footn.split(" ",1)[1].strip()
	if args.verbose:
		print (number)
	document = document.replace('<note type="x-footnote">'+number+'</note>', '<note type="x-footnote">'+number+' '+text+'</note>')
if not args.verbose:
	f3 = open(args.filenameOut, "w")
	f3.write(document)


