import requests
import re
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import urllib3

urllib3.disable_warnings()

parser = ArgumentParser()
parser.add_argument("-u", "--url", dest="url", 
                    help="Baseurl", metavar="URL", required=True)
parser.add_argument("-o", "--output", dest="filenameOut", 
                    help="Filename for output XML", metavar="OUTPUT", required=True)
parser.add_argument("-b", "--bible", dest="bible", 
                    help="Bible short form, e.g., LUT",  metavar="bible", required=True)
parser.add_argument("-w", "--workingtitle", dest="workingtitle", 
                    help="Working title",  metavar="workingtitle", required=True)
                    
args = parser.parse_args()

bible = args.bible
modulename = args.bible
workingtitle = args.workingtitle
filename = args.filenameOut
url = args.url

books = ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges",
        "Ruth","1 Samuel","2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
        "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
        "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah",
        "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
        "Malachi", 
         "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
        "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
        "James", "1 Peter", "2 Peter", "1 John", "2 John",
        "3 John", "Jude", "Revelation"]

booksosis = {"Genesis": "Gen","Exodus":"Exod","Leviticus":"Lev","Numbers":"Num",
             "Deuteronomy":"Deut","Joshua":"Josh","Judges":"Judg","Ruth":"Ruth",
             "1 Samuel":"1Sam","2 Samuel":"2Sam", "1 Kings":"1Kgs", 
             "2 Kings":"2Kgs", "1 Chronicles":"1Chr", "2 Chronicles":"2Chr",
            "Ezra":"Ezra", "Nehemiah":"Neh", "Esther":"Esth", "Job":"Job",
            "Psalm":"Ps", "Proverbs":"Prov", "Ecclesiastes":"Eccl", 
            "Song of Solomon":"Song", "Isaiah":"Isa", "Jeremiah":"Jer", 
            "Lamentations":"Lam", "Ezekiel":"Ezek", "Daniel":"Dan",
            "Hosea":"Hos", "Joel":"Joel", "Amos":"Amos", "Obadiah":"Obad",
            "Jonah":"Jonah", "Micah":"Mic", "Nahum":"Nah", "Habakkuk":"Hab",
            "Zephaniah":"Zeph", "Haggai":"Hag", "Zechariah":"Zech", 
            "Malachi":"Mal", 
             "Matthew":"Matt", "Mark":"Mark",
            "Luke":"Luke", "John":"John", "Acts":"Acts",
            "Romans":"Rom", "1 Corinthians":"1Cor", "2 Corinthians":"2Cor",
            "Galatians":"Gal", "Ephesians":"Eph", "Philippians":"Phil",
            "Colossians":"Col", "1 Thessalonians":"1Thess", 
             "2 Thessalonians":"2Thess", "1 Timothy":"1Tim",
            "2 Timothy":"2Tim", "Titus":"Titus", "Philemon":"Phlm", 
            "Hebrews":"Heb", "James":"Jas", "1 Peter":"1Pet",
            "2 Peter":"2Pet", "1 John":"1John", "2 John":"2John",
            "3 John":"3John", "Jude":"Jude", "Revelation":"Rev"}
limit = {"Genesis":50, "Exodus":40,"Leviticus":27,"Numbers":36,"Deuteronomy":34,
        "Joshua":24,"Judges":21,"Ruth":4,"1 Samuel":31, "2 Samuel":24,
        "1 Kings":22, "2 Kings":25, "1 Chronicles":29, "2 Chronicles":36,
        "Ezra":10, "Nehemiah":13, "Esther":10, "Job":42, "Psalm":150,
        "Proverbs":31, "Ecclesiastes":12, "Song of Solomon":8, "Isaiah":66,
        "Jeremiah":52, "Lamentations":5, "Ezekiel":48, "Daniel":12,
        "Hosea":14, "Joel":3, "Amos":9, "Obadiah":1, "Jonah":4, "Micah":7,
        "Nahum":3, "Habakkuk":3, "Zephaniah":3, "Haggai":2, "Zechariah":14,
        "Malachi":3, 
         "Matthew":28, "Mark":16, "Luke":24,
        "John":21, "Acts":28, "Romans":16, "1 Corinthians":16,
        "2 Corinthians":13, "Galatians":6, "Ephesians":6, "Philippians":4, 
         "Colossians":4, "1 Thessalonians":5, "2 Thessalonians":3,
        "1 Timothy":6,"2 Timothy":4, "Titus":3, "Philemon":1,
        "Hebrews":13, "James":5, "1 Peter":5, "2 Peter":3,
        "1 John":5, "2 John":1, "3 John":1, "Jude":1,
        "Revelation":22}

header = '''<?xml version="1.0" encoding="UTF-8" ?>
<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace
      http://www.bibletechnologies.net/osisCore.2.1.1.xsd">
<osisText osisIDWork="'''+modulename+'''" osisRefWork="defaultReferenceScheme" xml:lang="de">
    <header>
        <work osisWork="'''+modulename+'''">
            <title>'''+workingtitle+'''</title>
            <identifier type="OSIS">KJV.TutorEncoding</identifier>
            <refSystem>Bible.KJV</refSystem>
        </work>
        <work osisWork="defaultReferenceScheme">
            <refSystem>Bible.KJV</refSystem>
        </work>
    </header>
        '''
tail = '''        
  </osisText>
</osis>'''
f = open(filename, "w")
f.write(header)

for book in books:
    print ("Processing "+book)
    f.write('<div type="book" osisID="'+booksosis[book]+'">')
    for chapter in range(1,limit[book]+1):
        #if chapter>2:
        #    break
        markierung = booksosis[book]+"."+str(chapter)
        f.write('\n <chapter sID="'+markierung+'" osisID="'+markierung+'">\n')
        url2 = url+'/passage/?search='+str(book)+'+'+str(chapter)+'&version='+bible
        print (url2)
        r = requests.get(url2, verify=False)
        print (r.status_code)
        soup = BeautifulSoup(r.content, "html.parser")
        # crossreferences
        refs = {}
        li = soup.find('div', {'class': 'crossrefs hidden'})
        if li != None:
            for el in li.find_all('li'):
                #print (''.join(filter(str.isalpha, el['id'].split("-")[-1])))
                number = ''.join(filter(str.isalpha, el['id'].split("-")[-1]))
                refs['('+number+")"] = '<note type="crossReference" n="'+number+'">'+el.text+'</note>'
        # footnotes
        footnotes = {}
        li = soup.find('div', {'class': 'footnotes'})
        if li != None:
            for el in li.find_all('li'):
                number = ''.join(filter(str.isalpha, el['id'].split("-")[-1]))
                footnotes['['+number+"]"] = '<note n="'+number+'">'+el.find('span', {'class':'footnote-text'}).text+'</note>'
        # text
        li = soup.find('div', {'class': 'passage-content passage-class-0'})
        versen = 0
        #markierung = ""
        textalt = ""
        try:
            for el in li.find_all('span'):
                #print (el)
                if "text" in el['class']:
                    text = el.text.replace("\xa0", " ")
                    for short, footnotetext in footnotes.items():
                        text = text.replace(short, footnotetext)
                    for short, footnotetext in refs.items():
                        text = text.replace(short, footnotetext)
                    first = text.split(" ")[0].strip()
                    if versen == 0 and first.strip()==str(chapter):
                        # Erster Vers
                        first = "1"
                        text = text.replace(str(chapter),"").strip()
                    if " " in first:
                        first = text.split(" ")[0].strip()
                    if not first[0].isdigit():
                        if el.parent.name == "h3":
                            # Header
                            f.write('\n<title type="chapter">'+text+'</title>'+"\n")
                        else:
                            # Zeilenumbruch
                            textalt = textalt + text+"</br>"
                    else:
                        # New Verse
                        versen = int(first)
                        #print ("--->"+str(versen))
                        if versen>1:
                            #print ("----->"+str(versen))
                            textalt = textalt + '<verse eID="'+markierung+'.'+str(versen-1)+'"/>'
                            f.write(textalt+"\n")
                            textalt = ""

                        text = text.replace(first,"").strip()
                        #markierung = book+"."+str(chapter)
                        textalt = '\n<verse sID="'+markierung+'.'+str(versen)+'" osisID="'+markierung+'.'+str(versen)+'">'+text
        except:
            print ("Error. No text.")
        # last verse
        text = textalt + '<verse eID="'+markierung+'.'+str(versen-1)+'"/>'
        f.write(text+"\n")
        f.write("\n<chapter  eID=\""+markierung+"\">"+"\n")
        text = ""
    f.write( "\n</div>\n")
    #break
f.write(tail)
f.close()
