from argparse import ArgumentParser
import requests
from bs4 import BeautifulSoup
import re
from transliterate import translit, get_available_language_codes
import sys

parser = ArgumentParser()
parser.add_argument("-u", "--url", dest="url", 
                    help="URL to 'alle artikel'", metavar="URL", required=True)
parser.add_argument("-l", "--last-page", dest="lastpage", default="98890",
                    help="last page for this entry", metavar="LAST", required=True)
parser.add_argument("-o", "--output", dest="filenameOut", 
                    help="write to file", metavar="OUTPUT", required=True)
parser.add_argument("-t", "--try", 
                    action="store_true", dest="verbose", default=False, 
                    help="just a test run")

args = parser.parse_args()
lastpage = int(args.lastpage)
linkliste = []
for i in range (0,lastpage, 20):
	sys.stdout.write('Processing linklist, '+str(i)+' of '+str(lastpage))
	sys.stdout.flush()	
	url = (args.url+"?&s="+str(i))
	#print (url)
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	links = soup.find_all('a')
	for l in links:
		#print (l.text + " : "+l['href'])
		if "/A" in l['href']:
			linkliste.append ([l.text , l['href']])
	
	if args.verbose and i > 100:
		break
	sys.stdout.write('\r')
	sys.stdout.flush()
sys.stdout.write("\n")
header = '''<?xml version="1.0" encoding="utf-8"?>
 <TEI xmlns="http://www.crosswire.org/2013/TEIOSIS/namespace"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.crosswire.org/2013/TEIOSIS/namespace
                          http://www.crosswire.org/OSIS/teiP5osis.2.5.0.xsd">
 <teiHeader>
 <fileDesc>
  <titleStmt>
   <title>A title statement about the electronic text</title>
  </titleStmt>
  <publicationStmt>
   <p>Information on the publication of the electronic text.</p>
  </publicationStmt>
  <sourceDesc>
   <p>A bibliographic description of the source for the electronic text.</p>
  </sourceDesc>
 </fileDesc>
</teiHeader>
<text>
 <body>
 '''                         
f3 = open(args.filenameOut, "w")
f3.write(header)
dlist = []
glist = []
i = 1
for l in linkliste:
	sys.stdout.write('Processing entry '+str(i)+' of '+str(len(linkliste)))
	sys.stdout.flush()
	page = requests.get("http://www.zeno.org/"+l[1])
	soup = BeautifulSoup(page.text, 'html.parser')
	container = soup.find ("div", {"class": "zenoCOMain"})
	if container==None:
		print ("Error on entry "+"http://www.zeno.org/"+l[1])
		continue
	if container.find("p")==None:
		print ("Error 2 on entry "+"http://www.zeno.org/"+l[1])
		continue
	text = str(container.find("p"))[3:][:-4]
	text = text.replace ("<b>", '<hi rend="bold">')
	text = text.replace ("</b>", '</hi>')
	text = text.replace ("<i>", '<hi rend="italic">')
	text = text.replace ("</i>", '</hi>')
	text = text.replace ('<span class="zenoTXSpaced">', '<hi rend="underline">')
	text = text.replace ("</span>", '</hi>')
	clean = re.compile('<a.*?>')
	text = re.sub(clean, '', text)
	clean = re.compile('</a.*?>')
	text = re.sub(clean, '', text)
	lemma = l[0].replace( "ἀ", "α")
	lemma = lemma.replace ("ἆ",  "α")
	lemma = lemma.replace ("ὰ",  "α")
	lemma = lemma.replace ("ἄ",  "α") 
	lemma = lemma.replace ("ἃ",  "α")
	lemma = lemma.replace ("ἅ",  "α")
	lemma = lemma.replace ("ἐ",  "ε")
	lemma = lemma.replace ("ή",  "η")
	lemma = lemma.replace ("ᾱ",  "α")
	lemma = lemma.replace ("ὶ",  "ι")
	lemma = lemma.replace ("ῑ",  "ι")
	lemma = lemma.replace ("ώ",  "ω")
	#print (l[0] )
	#print ("-- : "+translit(lemma, 'el', reversed=True) )
	trans = translit(lemma, 'el', reversed=True)
	if trans in dlist:
		trans = trans + " "+str(i)
	dlist.append(trans)
	if l[0] in glist:
		l[0] = l[0] + " "+str(i)
	glist.append (l[0])
	entrytext = '''<entryFree n="'''+l[0]+'''|'''+trans+'''|P'''+str(i).zfill(10)+'''">
 <title>'''+l[0]+'''</title>
 <orth type="trans" rend="bold">'''+trans+'''</orth>
 <def>'''+text+'''</def>
</entryFree>'''
	f3.write(entrytext)
	i = i+1
	#if args.verbose and i > 41:
	#	break
	sys.stdout.write('\r')
	sys.stdout.flush()
footer = '''  </body>
</text>'''
f3.write(footer)
