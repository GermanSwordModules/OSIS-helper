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

## convert.py

This tool finds (german) bible references (Mt 4,4) in free text and converts them into OSIS format (```<reference osisRef="Matt.4.4">Mt 4,4</reference>```). It can identify ranges (Mt 4,3-6) and can foresee at least one reference without book (Mt 3,4; 6,8). The book names are stored in a dict. 
