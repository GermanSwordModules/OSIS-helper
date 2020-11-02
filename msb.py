import os, subprocess
import unicodedata as ud
import pdfplumber
import re
# please define input and output 
filename = ".../John_MacArthur_Studienbibel_Schlachter_2000.pdf"
filename2 = "MASB.xml"
# ------------------------------

titlelist = ['Titel', 'Autor und Abfassungszeit', 'Hintergrund und Umfeld', 'Historische und lehrmäßige Themen',
            'Herausforderungen für den Ausleger', 'Gliederung']
linelength = 80

filter = {"1Mo":"Gen","1 Mo":"Gen", "Gen":"Gen", "1Mose":"Gen",
          "2Mo":"Exod","2 Mo":"Exod", "Ex":"Exod", "Exod":"Exod",  "2Mose":"Exod", 
          "3Mo":"Lev","3 Mo":"Lev", "Lev":"Lev", "3Mose":"Lev", 
          "Neh":"Neh", 
          "4Mo":"Num","4 Mo":"Num", "Num":"Num", "4Mose":"Num",
          "5Mo":"Deut", "5 Mo":"Deut", "Dtn":"Deut", "Deut":"Deut", "5Mose":"Deut", "Dr":"Deut",
          "Dan":"Dan",
          "Ri":"Judg","Richt":"Judg",
          "Rth":"Ruth",
          "1 Sam":"1Sam", "1Sam":"1Sam", "2 Sam":"2Sam", "2Sam":"2Sam",
          "1Kön":"1Kgs","2Kön":"2Kgs","1 Kö":"1Kgs","2 Kö":"2Kgs",
          "1 Chro":"1Chr", "2 Chro":"2Chr", 
          "Esr":"Ezra",
          "Neh":"Neh",
          "Esth":"Esth",
          "Hio":"Job", 
           "Ps":"Ps", 
         "Spr":"Prov",
          "Pred":"Eccl",
          "Hoh":"Song",
          "Jes":"Jes",
          "Jer":"Jer",
          "Kla":"Lam",
          "Hes":"Ezek",
          "Dan":"Dan", "Da":"Dan", 
          "Hos":"Hos",
          "Joe":"Joel","Joel":"Joel",
          "Am":"Amos",
          "Ob":"Obad",
          "Jon":"Jonah",
          "Mi":"Mic",
          "Nah":"Nah",
          "Hab":"Hab",
          "Ze":"Zeph", "Zef":"Zeph",
          "Hag":"Hag",
          "Sach":"Zech",
          "Mal":"Mal", 
          "Mt":"Matt", 
          "Mk":"Mark",
         "Lk":"Luke", "Luk.":"Luke",
          "Joh":"John", "Jo":"John",
           "Apg":"Acts",
          "Röm":"Rom", "Rö":"Rom","Rom":"Rom",
           "1Kor":"1Cor", "1 Kor":"1Cor", "1. Kor":"1Cor", "1.Kor":"1Cor",
          "2Kor":"2Cor", "2 Kor":"2Cor", "2. Kor":"2Cor", "2.Kor":"2Cor",
          "Gal":"Gal",
          "Eph":"Eph",
          "Phil":"Phil",
          "Kol":"Col", "Kol.":"Col",
          "1Th":"1Thess","1 Th":"1Thess","1.Thess":"1Thess",
          "2Th":"2Thess","2 Th":"2Thess","2.Thess":"2Thess",
          "1Tim":"1Tim","1 Tim":"1Tim", "1. Tim.":"1Tim",
          "2Tim":"2Tim","2 Tim":"2Tim", "2. Tim.":"2Tim",
          "Tit":"Titus",
          "Phlm":"Phlm",
          "1Petr":"1Pet", "1 Pt":"1Pet", "1 Petr":"1Pet",
          "2Petr":"2Pet", "2 Pt":"2Pet", "2 Petr":"2Pet",
          "1Joh":"1John", "1 Jh":"1John",
          "2Joh":"2John", "2 Jh":"2John",
          "3Joh":"3John", "3 Jh":"3John",
          "Hebr":"Heb",
          "Jak":"Jas", 
           "Jud":"Jude",
          "Offb": "Rev", "Ofb":"Rev", 
         # Apokryphen
           "Sir":"Sir", "Tob":"Tob"}
def markbooks (text):
    for book in filter:
        text = text.replace (book+"  ", book+" ")
    for book in filter:
        #print (book)
        #ret = re.findall( )
        bookn = str(filter[book])
        text = re.sub (   r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(?!-)[ ]?.*?(\.?)([0-9]*)" ,
                       '<reference osisRef="'+str(filter[book])+r'.\g<2>.\g<3>\g<4>'+'"'+r'>\g<0>'+'</reference>'
                    #r'<reference osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</reference>'
                    , text)
        text = re.sub (        r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(-+)[ ]?(\.?)([0-9]*)" ,
                       '<reference osisRef="'+bookn+r'.\g<2>.\g<3>\g<4>'+bookn+r'.\g<2>.\g<6>'+'"'+r'>\g<0></reference>'
                    #r'<reference osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</reference>'
                    , text)
        # One more Iteration
        text = re.sub (        r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(?!-)[ ]?.*?(\.?)([0-9]*)</reference>[;]?[:]?[ ]?([0-9]+?),[ ]?([0-9]*)" ,
                       '<reference osisRef="'+str(filter[book])+r'.\g<2>.\g<3>\g<4>'+'"'+'>'+book+r' \g<2> \g<3>,\g<4>'+'</reference>'+'; <reference osisRef="'+str(filter[book])+r'.\g<6>.\g<7>'+'"'+r'>\g<6>,\g<7>'+'</reference>'
                    #r'<reference osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</reference>'
                    , text)
    return text

books = [
    ['Gen', 45,49,121],
    ['Exod', 122 , 125, 183],
    ['Lev', 184, 187, 224],
    ['Num', 225, 227, 272],
    ['Deut', 273, 276, 327],
    ['Josh', 328 , 330, 357],
    ['Judg', 358, 360, 386],
    ['Ruth', 387, 389, 394],
    ['1Sam', 395, 398, 442],
    ['2Sam', 443, 444, 481],
    ['1Kgs', 482, 486, 528],
    ['2Kgs', 529, 529, 573],
    ['1Chr', 574, 576, 605],
    
    ['2Chr', 606, 607, 645],
    ['Ezra', 646, 649, 662],
    ['Neh', 663, 666, 685],
    ['Esth', 686,689,695],
    ['Job', 696, 702, 738],
    ['Ps', 739, 741, 853],
    ['Prov', 854, 857, 895],
    ['Eccl', 896, 899, 909],
    ['Song', 910, 912, 920],
    ['Isa', 921, 924, 1004],
    ['Jer', 1005, 1008, 1070],
    ['Lam', 1071, 1074, 1080],
    ['Ezek', 1081, 1085, 1152],
    ['Dan', 1153, 1156, 1178],
    ['Hos', 1179, 1181, 1190],
    ['Joel', 1191, 1193, 1197],
    ['Amos', 1198, 1200, 1207],
    ['Obad', 1208, 1210, 1211],
    ['Jonah', 1212, 1214, 1216],
    ['Mic', 1217, 1219, 1225],
    ['Nah', 1226, 1228, 1231],
    ['Hab', 1232, 1234, 1238],
    ['Zeph', 1239, 1241, 1244],
    ['Hag', 1245, 1247, 1250],
    ['Zech', 1251, 1253, 1270],
    ['Mal', 1271, 1273,1279],
    ['Matt', 1301, 1306, 1635],
    ['Mark', 1636, 1368, 1414],
    ['Luke', 1415, 1421, 1478],
    ['John', 1479, 1483, 1538],
    ['Acts', 1539, 1541, 1596],
    ['Rom', 1597, 1600, 1635],
    ['1Cor', 1636, 1639, 1670],
    ['2Cor', 1671, 1674, 1697],
    ['Gal', 1698, 1701, 1714],
    ['Eph', 1715, 1718, 1731],
    ['Phil', 1732,1735, 1745],
    ['Col', 1746, 1749, 1758],
    ['1Thess', 1759, 1761, 1769],
    ['2Thess', 1770, 1772, 1776],
    ['1Tim', 1777, 1780, 1793],
    ['2Tim', 1794, 1796, 1804],
    ['Titus', 1805, 1807, 1811],
    ['Phlm', 1812, 1814, 1815],
    ['Heb', 1816, 1819, 1845],
    ['Jas', 1846, 1848, 1857],
    ['1Pet', 1858, 1861, 1872],
    ['2Pet', 1873, 1876, 1884],
    ['1John', 1885, 1889, 1900],
    ['2John', 1901, 1903, 1904],
    ['3John', 1905, 1907, 1908],
    ['Jude', 1909, 1911, 1915],
    ['Rev', 1916, 1919, 1953]    
]

modulename = "MASB"
workingtitle ="MASB"

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
f = open(filename2, "w")
f.write(header)
f.close()

for book in books:
    pdf = pdfplumber.open(filename)
    print ("Processing book "+book[0])
    f = open(filename2, "a")
    f.write('<div type="book" osisID="'+book[0]+'">')
    f.close()
    erklaertext = ""
    paragraph = ""
    title = ""
    # uncomment these lines, if you wish to process the introductionary parts. 
    # currently there is no place for this in osis....
    #for pagenumber in range(book[1]-1, book[2]-2):
    #    continue
    #    page = pdf.pages[pagenumber]
    #    text = page.extract_text()
    #    lines = text.split("\n")
    #    for i in range(0,len(lines)):
    #        line = lines[i].strip()
    #        #print (line)
    #        if i==0:
    #            # header
    #            continue
    #        if line.strip() in titlelist:
    #            if paragraph != "":
    #                erklaertext = erklaertext +  ("<p>"+(paragraph)+"</p>\n")
    #                paragraph = ""
    #            erklaertext = erklaertext +  ("<title>"+(line)+"</title>\n")
    #            title = line
    #        elif len(line)<linelength or title == "Gliederung":
    #            # New Paragraph
    #            if line[-1] == "-":
    #                paragraph = paragraph + line[:-1]
    #            else:
    #                paragraph = paragraph + line + " "
    #            erklaertext = erklaertext +  ("<p>"+(paragraph)+"</p>\n")
    #            paragraph = ""
    #        else:
    #            if line[-1] == "-":
    #                paragraph = paragraph + line[:-1]
    #            else:
    #                paragraph = paragraph + line + " "
    #    if paragraph != "":
    #        erklaertext = erklaertext +  ("<p>"+(paragraph)+"</p>\n")
    #        paragraph = ""
    #    #print (erklaertext)
    #erklaertext = '<div type="section" annotateType="commentary" annotateRef="'+book[0]+'">'+erklaertext+"</div>"
    #f.write(markbooks(erklaertext))
    ## Verses
    vn = 0
    lastv = 1
    verses = ""
    verses = verses+'<chapter sID="'+book[0]+'.'+str(lastv)+'" osisID="'+book[0]+'.'+str(lastv)+'">'
    verse = ""
    for pagenumber in range(book[2]-1, book[3]):
        try:
            page = pdf.pages[pagenumber]   
            #print (page.lines)
            #print ("=== page "+str(pagenumber)+ " - "+str(len(page.lines)))
            yplus = 0
            if len(page.lines)>1:
                ydiff = page.lines[len(page.lines)-1]['y0']
            else:
                #print ("Using image on page "+str(pagenumber))
                ydiff = page.rects[len(page.rects)-1]['y0']
                yplus = page.rects[len(page.rects)-2]['y0']
            pagen = page.crop ( (0,page.height-ydiff, (page.width/2), page.height-20-yplus) )
            pagen2 = page.crop ( ((page.width/2),page.height-ydiff,(page.width) , page.height-20-yplus) )
            #print (pagen.extract_text(x_tolerance=1))
            #print (pagen2.extract_text(x_tolerance=1))
            text1 = pagen.extract_text(x_tolerance=1)
            text2 = pagen2.extract_text(x_tolerance=1)
            text =text1+"\n"+text2
            lines = text.split("\n")
            for i in range(0,len(lines)):
                line = lines[i].strip()
                if re.search ("[0-9+],[0-9+]", line.split(" ")[0]) and not "(" in line and not ")" in line and not ";" in line.split(" ")[0]:
                    if len(line.split(" "))<=1:
                        # passt nicht
                        if line[-1] == "-":
                            verse = verse + line[:-1]
                        else:
                            verse = verse + line + " "
                        continue
                    stelle = line.split(" ")[0]
                    textnach = line.split(" ",1)[1]+" "
                    #print (textnach)
                    if "-" in stelle:
                        bis = stelle.split("-")[1]
                        stelle = stelle.split("-")[0]
                        chapter = stelle.split(",")[0]
                        versen = stelle.split(",")[1]
                    elif "." in stelle:
                        bis = stelle.split(".")[1]
                        stelle = stelle.split(".")[0]
                        chapter = stelle.split(",")[0]
                        versen = stelle.split(",")[1]
                    else:    
                        chapter = stelle.split(",")[0]
                        versen = stelle.split(",")[1]
                    #print (" L "+str(lastv)+" --> "+ str(chapter)+" -->"+str(abs(int(lastv) - int(chapter))))
                    if abs(int(lastv) - int(chapter))>2:
                        # passt nicht
                        if line[-1] == "-":
                            verse = verse + line[:-1]
                        else:
                            verse = verse + line + " "
                        continue
                    if verse != "":
                        verses = verses +  (""+(verse)+"</p></div>\n")
                    verse = ""
                    if str(lastv) != str(chapter):
                            verses = verses+'<chapter  eID="'+book[0]+'.'+str(lastv)+'">\n'
                            verses = verses+'<chapter sID="'+book[0]+'.'+str(chapter)+'" osisID="'+book[0]+'.'+str(chapter)+'">'
                    stelle = line.split(" ")[0]
                    if "-" in stelle:
                        bis = stelle.split("-")[1]
                        stelle = stelle.split("-")[0]
                        chapter = stelle.split(",")[0]
                        versen = stelle.split(",")[1]
                        verse = '<div type="section" annotateType="commentary" annotateRef="'+book[0]+'.'+str(chapter)+'.'+versen+'-'+book[0]+'.'+chapter+'.'+bis+'"><p>'+stelle+" "+textnach
                    elif "." in stelle:
                        bis = stelle.split(".")[1]
                        stelle = stelle.split(".")[0]
                        chapter = stelle.split(",")[0]
                        versen = stelle.split(",")[1]
                        verse = '<div type="section" annotateType="commentary" annotateRef="'+book[0]+'.'+str(chapter)+'.'+versen+'-'+book[0]+'.'+chapter+'.'+bis+'"><p>'+stelle+" "+textnach
                    else:    
                        chapter = stelle.split(",")[0]
                        versen = stelle.split(",")[1]
                        verse = '<div type="section" annotateType="commentary" annotateRef="'+book[0]+'.'+str(chapter)+'.'+versen+'"><p>'+stelle+" "+textnach
                    lastv = int(chapter)
                    # neuer eintrag
                else:
                    if line[-1] == "-":
                        verse = verse + line[:-1]
                    else:
                        verse = verse + line + " "
        except:
            continue
    if verse != "":
        verses = verses +  ""+(verse)+"</p></div>\n"
        verse = ""
    f = open(filename2, "a")
    f.write((verses))
    f.write('<chapter  eID="'+book[0]+'.'+str(lastv)+'">')
    f.write('</div>') #book
    f.close()
    verses = ""
# Write end of file
f = open(filename2, "a")
f.write(tail)
f.close()
