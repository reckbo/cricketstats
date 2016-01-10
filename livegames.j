#!/usr/bin/env jconsole
NB. Prints table of current cricket games around the world with links
NB. to their scorecards.
NB. 
NB. Usage
NB.     ./livegames.j

Locale=:coname''
NB. ========================================
NB. XML parser that converts XML to table format.
NB. Element 'item' defines a record.
require 'api/expat'
coclass 'xml2tbl'
coinsert 'jexpat'

NB. Define expat callbacks

expat_initx=: 3 : 0
  Line=: 0$0
  Lines=: 0 0$0
  Started=:0
)

expat_start_elementx=: 4 : 0
  'Elem Att Val'=. x
  if. Elem -: 'item' do.
    if. Started do.
      Lines=: Lines,Line
      Line=: 0$0
    else.
      Started=:1
    end.
  end.
)

expat_end_elementx=: 3 : 0
  if. Started do.
    Line=: Line , < expat_characterData
  end.
)

NB. xml2tbl fread 'test/test.xml'
xml2tbl=: 3 : 0
  expat_parse_xml y
  Lines -."1 a:
)

xml2tbl_z_=: xml2tbl_xml2tbl_
NB. ========================================

cocurrent Locale
require 'web/gethttp'
URL=:'http://static.cricinfo.com/rss/livescores.xml'
smoutput 2 3 {"1 tbl=:xml2tbl gethttp URL
exit''
