from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="filename", 
                    help="read footnotes input", metavar="FILE", required=True)
parser.add_argument("-t", "--try", 
                    action="store_true", dest="verbose", default=False,
                    help="just a run without realy parsing the document")

args = parser.parse_args()

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
          "1Chro":"1Chr", "2Chro":"2Chr", 
          "1Chr":"1Chr", "2Chr":"2Chr", 
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
    text = re.sub (r"\>\s*([a-zA-ZäöüÄÖÜß-]+)", '<xr type="see">→ <ref target="\g<1>">\g<1></ref></xr>', text)
    for book in filter:
        text = text.replace (book+"  ", book+" ")
    for book in filter:
        #print (book)
        #ret = re.findall( )
        bookn = str(filter[book])
        text = re.sub (   r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(?!-)[ ]?.*?(\.?)([0-9]*)" ,
                       '<xr type="Bible"><ref osisRef="'+str(filter[book])+r'.\g<2>.\g<3>\g<4>'+'"'+r'>\g<0>'+'</ref></xr>'
                    #r'<xr type="Bible"><ref osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</ref></xr>'
                    , text)
        text = re.sub (        r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(-+)[ ]?(\.?)([0-9]*)" ,
                       '<xr type="Bible"><ref osisRef="'+bookn+r'.\g<2>.\g<3>\g<4>'+bookn+r'.\g<2>.\g<6>'+'"'+r'>\g<0></ref></xr>'
                    #r'<xr type="Bible"><ref osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</ref></xr>'
                    , text)
        # One more Iteration
        text = re.sub (        r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(?!-)[ ]?.*?(\.?)([0-9]*)</reference>[;]?[:]?[ ]?([0-9]+?),[ ]?([0-9]*)" ,
                       '<xr type="Bible"><ref osisRef="'+str(filter[book])+r'.\g<2>.\g<3>\g<4>'+'"'+'>'+book+r' \g<2> \g<3>,\g<4>'+'</ref></xr>'+'; <xr type="Bible"><ref osisRef="'+str(filter[book])+r'.\g<6>.\g<7>'+'"'+r'>\g<6>,\g<7>'+'</ref></xr>'
                    #r'<xr type="Bible"><ref osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</ref></xr>'
                    , text)
    return text

f = open(args.filename, "r")
text = f.read()

text = markbooks(text).replace("\n\n","\n<lb/>\n\n")

f = open(args.filename, "w")
f.write (text)
