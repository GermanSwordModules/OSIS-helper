# OSIS-helper
Little tools to support the generation of OSIS modules (see https://crosswire.org/osis/). They can be used to create SWORD Modules.

## pfn.py

Takes two files: 
* One input file has citations 1-n separated by two newlines ```\n\n```. The first characters (or: numbers!) before the first white space will be interpreted as label.
* One input file (xml) contains the text and pre-defined footnote fields ```<note type="x-footnote">label</note>```. They will be filled with the footnote from file 1.

This helps to merge both texts and footnotes which are usually extracted in two steps. 

Example run:
```
python pfn.py -i fn5 -w Mauerhofer-Einleitung.xml
```
If you add the ```-t``` flag it will just output the list of labels without doing any changes to the xml file.
## zenoparser.py 
* Converts public domain dictionaries from zeno.org to TEI Dictionaries (see https://wiki.crosswire.org/TEI_Dictionaries). 
* Takes the link to the "Alle Artikel" page (-u)
* Takes the maximum page which links to the last entry
* Takes an output xml-file.
* Test run with -t flag skips after approx. 100 pages. 
```
python3 zenoparser.py -u "http://www.zeno.org/Kategorien/T/Pape-1880" -l 98890 -o ../test.xml
```

## msb.py

Converts the "John MacArthur Studienbibel (Schlachter_2000)" published by CLV in 2004 as pdf to an OSIS commentary. Please adjust lines 6 and 7. Line 6 holds the path to the PDF commentary (can be found on the web) and line 7 contains the output file. Convert the ouput using

```
osis2mod ~/.sword/modules/comments/zcom/MASB - < B.xml   -v Luther
```

and add a proper config file. That should be all... 

## convert.py

This tool finds (german) bible references (Mt 4,4) in free text and converts them into OSIS format (```<reference osisRef="Matt.4.4">Mt 4,4</reference>```). It can identify ranges (Mt 4,3-6) and can foresee at least one reference without book (Mt 3,4; 6,8). The book names are stored in a dict. 
