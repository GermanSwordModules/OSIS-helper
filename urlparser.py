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

books = ["1.Mose","2.Mose","3.Mose","4.Mose","5.Mose","Josua","Richter",
        "Rut","1.Samuel","2.Samuel", "1.Könige", "2.Könige", "1.Chronik",
        "2.Chronik", "Esra", "Nehemia", "Esther", "Hiob", "Psalm", "Sprüche",
        "Prediger", "Hoheslied", "Jesaja", "Jeremia", "Klagelieder",
        "Hesekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadja", "Jona",
        "Micha", "Nahum", "Habakuk", "Zefanja", "Haggai", "Sacharja",
        "Maleachi", "Matthäus", "Markus", "Lukas", "Johannes", "Apostelgeschichte",
        "Römer", "1.Korinther", "2.Korinther", "Galater", "Epheser",
        "Philipper", "Kolosser", "1.Thessalonicher", "2.Thessalonicher",
        "1.Timotheus", "2.Timotheus", "Titus", "Philemon", "Hebräer",
        "Jakobus", "1.Petrus", "2.Petrus", "1.Johannes", "2.Johannes",
        "3.Johannes", "Judas", "Offenbarung"]

booksosis = {"1.Mose": "Gen","2.Mose":"Exod","3.Mose":"Lev","4.Mose":"Num",
             "5.Mose":"Deut","Josua":"Josh","Richter":"Judg","Rut":"Ruth",
             "1.Samuel":"1Sam","2.Samuel":"2Sam", "1.Könige":"1Kgs", 
             "2.Könige":"2Kgs", "1.Chronik":"1Chr", "2.Chronik":"2Chr",
            "Esra":"Ezra", "Nehemia":"Neh", "Esther":"Esth", "Hiob":"Job",
            "Psalm":"Ps", "Sprüche":"Prov", "Prediger":"Eccl", 
            "Hoheslied":"Song", "Jesaja":"Isa", "Jeremia":"Jer", 
            "Klagelieder":"Lam", "Hesekiel":"Ezek", "Daniel":"Dan",
            "Hosea":"Hos", "Joel":"Joel", "Amos":"Amos", "Obadja":"Obad",
            "Jona":"Jonah", "Micha":"Mic", "Nahum":"Nah", "Habakuk":"Hab",
            "Zefanja":"Zeph", "Haggai":"Hag", "Sacharja":"Zech", 
            "Maleachi":"Mal", "Matthäus":"Matt", "Markus":"Mark",
            "Lukas":"Luke", "Johannes":"John", "Apostelgeschichte":"Acts",
            "Römer":"Rom", "1.Korinther":"1Cor", "2.Korinther":"2Cor",
            "Galater":"Gal", "Epheser":"Eph", "Philipper":"Phil",
            "Kolosser":"Col", "1.Thessalonicher":"1Thess", 
             "2.Thessalonicher":"2Thess", "1.Timotheus":"1Tim",
            "2.Timotheus":"2Tim", "Titus":"Titus", "Philemon":"Phlm", 
            "Hebräer":"Heb", "Jakobus":"Jas", "1.Petrus":"1Pet",
            "2.Petrus":"2Pet", "1.Johannes":"1John", "2.Johannes":"2John",
            "3.Johannes":"3John", "Judas":"Jude", "Offenbarung":"Rev"}
limit = {"1.Mose":50, "2.Mose":40,"3.Mose":27,"4.Mose":36,"5.Mose":34,
        "Josua":24,"Richter":21,"Rut":4,"1.Samuel":31, "2.Samuel":24,
        "1.Könige":22, "2.Könige":25, "1.Chronik":29, "2.Chronik":36,
        "Esra":10, "Nehemia":13, "Esther":10, "Hiob":42, "Psalm":150,
        "Sprüche":31, "Prediger":12, "Hoheslied":8, "Jesaja":66,
        "Jeremia":52, "Klagelieder":5, "Hesekiel":48, "Daniel":12,
        "Hosea":14, "Joel":4, "Amos":9, "Obadja":1, "Jona":4, "Micha":7,
        "Nahum":3, "Habakuk":3, "Zefanja":3, "Haggai":2, "Sacharja":14,
        "Maleachi":3, "Matthäus":28, "Markus":16, "Lukas":24,
        "Johannes":21, "Apostelgeschichte":28, "Römer":16, "1.Korinther":16,
        "2.Korinther":13, "Galater":6, "Epheser":6, "Philipper":4, 
         "Kolosser":4, "1.Thessalonicher":5, "2.Thessalonicher":3,
        "1.Timotheus":6,"2.Timotheus":4, "Titus":3, "Philemon":1,
        "Hebräer":13, "Jakobus":5, "1.Petrus":5, "2.Petrus":3,
        "1.Johannes":5, "2.Johannes":1, "3.Johannes":1, "Judas":1,
        "Offenbarung":22}
filter = {"1Mo":"Gen", "2Mo":"Exod", "3Mo":"Lev", "4Mo":"Num",
          "5Mo":"Deut","Hi":"Job","Ri":"Judg","1Kön":"1Kgs","2Kön":"2Kgs",
          "1Petr":"1Pet", "2Petr":"2Pet","Spr":"Prov","Hoh":"Song",
          "Sach":"Zech", "Hes":"Ezek", "Offb": "Rev","Jon":"Jonah",
         "1Kor":"1Cor","2Kor":"2Cor", "Mt":"Matt", "Mk":"Mark",
         "Lk":"Luke", "Joh":"John", "Apg":"Acts", "Röm":"Rom",
         "Hebr":"Heb","Jud":"Jude", "1Joh":"1John", "2Joh":"2John", 
          "3Joh":"3John", "Jos":"Josh", "Jak":"Jas", "Hebr":"Heb",
         "Pred":"Eccl"}

browser = webdriver.Firefox()
browser.set_window_size(2000, 20694)

text = ""
for book in books:
    #if book!="1.Mose":
    #    break
    section = False
    print ("Processing "+book)
    text = text + '<div type="book" osisID="'+booksosis[book]+'">'
    for chapter in range(1,limit[book]+1):
        #if chapter>2:
        #    break
        print ("-- Processing "+str(chapter)+" from chapter "+str(limit[book]+1))
        url = url+'/'+bible+'/'+str(book)+str(chapter)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        data = {}
        table = browser.find_elements(By.CLASS_NAME, 'footnote')
        for t in table:
            try:
                hover = ActionChains(browser).move_to_element(t).move_to_element(t)
                hover.perform()
                #mouseover = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'footnote-content')))#By.XPATH, '//*[@class="footnote-content"]')))
                fns = browser.find_elements(By.CLASS_NAME, 'footnote-content')
                val = ""
                #gr = fns = browser.find_elements(By.CLASS_NAME, 'v-tooltip__content')
                #print ("==")
                #for g in gr:
                #    print (g.text)
                for f in  (fns):
                    #print (f.text)
                    if len(f.text.strip())>4:
                        val =  (f.text.strip())
                old = val
                data[t.text.strip()]= (val.replace("1.", "").strip())
                #data[t.text.strip()]= (val.strip())
            except:
                print ("ERROR in SELENIUM")
        #print (data)
        li = soup.find('article', {'class': 'chapter'})
        versen = "1"
        try:
            children = li.findChildren(recursive=False)
        except:
            children = []
        markierung = booksosis[book]+"."+str(chapter)
        text = text + '\n <chapter sID="'+markierung+'" osisID="'+markierung+'">\n <div type="section">\n'
        headern = 0
        
        for child in children:
            
            if "h3" in str(child):
                if not section:
                    if headern>0:
                        text = text + '\n</div><div type="section">\n'
                    text = text + '\n<title canonical="false">'+child.text.strip()+'</title>'
                    eadern = headern
                    section = True
                else:
                    if headern>0:
                        text = text + '\n</div><div type="section">\n'
                    headern = headern
                    text = text + '\n<title canonical="false"">'+child.text.strip()+'</title>'
            elif child.name == "span" and "verse" in child['class']:
                #print (child)
                versen = child.find("span", {"class":"verse-number"}).text.strip()
                for verse in child.find_all("span", {"class": "verse-content"}):
                    
                    versedrin = False
                    for el in verse:
                        if "-" in versen:
                            fill = markierung+'.'+str(versen).split("-")[0]+"-"+markierung+'.'+str(versen).split("-")[1]
                        else:
                            fill = markierung+'.'+str(versen)
                        if "verse-content--hover" in str(el):
                            #pattern = r'\[.*?\]'
                            #versecontent =  re.sub(pattern, '<note  n="'+str(r'\g<0>').replace("[","").replace("]","")+'">'+
                            #                       data[str(r'\g<0>')]+'</note>', el.text)
                            versecontent = str(el.text)
                            #print ("-->"+versecontent)
                            for key, value in data.items():
                                if value.strip()!="":
                                    versecontent = versecontent.replace(key, '<note  n="'+str(key).replace("[","").replace("]","")+'">'+str(value)+'</note>')
                                else:
                                    versecontent = versecontent.replace(key, "")
                            text = text + '\n <verse sID="'+fill+'" osisID="'+fill.replace("-", " ")+'" n="'+versen+'">'+versecontent
                            versedrin = True
                            #versen = versen+1
                        if "verse-references" in str(el):
                            refs = el.text.strip().replace("\xa0"," ").replace ("(","").replace(")","").split("; ")
                            par = '<note type="crossReference" n="t" osisID="'+fill+'!crossReference.t">'
                            for ref in refs:
                                b = ref.split(" ")
                                bookn = b[0]
                                if bookn in filter:
                                    bookn = filter[bookn]
                                verses = b[1].replace (",", ".")
                                par = par + '\n<reference type="parallel" osisRef="'+bookn+'.'+verses+'">'+ref+'</reference>;'
                            par = par + "\n</note>"
                            text = text + "\n" + par  
                    if versedrin:
                        text = text + '<verse eID="'+fill+'"/>'
                        versedrin = False
        if section:
            section = False
        text = text + "\n</div><chapter  eID=\""+markierung+"\">"
    text = text + "\n</div>"

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

text = text.replace("\x01","")
f = open(""+filename, "w")
f.write(header)
f.write(text)
f.write(tail)
f.close()
