# coding: UTF-8
import sys
import os.path
import zipfile
import requests
import uuid

import spider.nhentai
from book import Book

link = input("Please input comic link: ")

print('visit to nhentai.net')
data = spider.nhentai.getImagesLinks(link)

print('create .epub file.')
print('%s.epub'%(data.title))
epub = zipfile.ZipFile(data.title + '.epub', 'w')

# create mimetype
epub.writestr("mimetype", "application/epub+zip")

# create container.xml
epub.writestr("META-INF/container.xml",
'''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
''')

count = len(data.images)
items = ''
tocncx = ''

for (index, image) in enumerate(data.images):

	print('[' + str(index+1) + '/' + str(count) + '] Downloading images ' + image, end = '')
	sys.stdout.flush()
	r = requests.get(image, cookies=data.cookies)
	print(' [OK]')

	# download images
	epub.writestr("OEBPS/Images/" + str(index+1) + "." + data.imagesType, r.content)

	# create xhtmls
	epub.writestr("OEBPS/Text/Section_000" + str(index+1) + ".xhtml",
'''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<!--?xml version='1.0' encoding='utf-8'?--><html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title></title>
</head>

<body>
  <div><img src="../Images/%d.%s"/></div>
</body>
</html>
'''%(index+1, data.imagesType))

	items += '	<item href="Text/Section_000%d.xhtml" id="Text_Section_000%d.xhtml" media-type="application/xhtml+xml"/>\n'%(index+1, index+1)
	items += '	<item href="Images/%d.%s" id="Images_%d.%s" media-type="image/%s"/>\n'%(index+1, data.imagesType, index+1, data.imagesType, data.imagesType)
	tocncx += '	<itemref idref="Text_Section_000%d.xhtml"/>\n'%(index+1)


random = uuid.uuid1()
# create content.opf
epub.writestr("OEBPS/content.opf",
'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            unique-identifier="bookid" version="2.0">
  <metadata>
    <dc:title>%s</dc:title>
	<dc:identifier id="bookid">%s</dc:identifier>
	<meta name="cover" content="Images_1.%s" />
  </metadata>
  <manifest>
%s
	<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
  </manifest>
  <spine toc="ncx">
%s
  </spine>
  <guide>
    <reference href="cover.html" type="cover" title="Cover"/>
  </guide>
</package>
'''%(data.title, random, data.imagesType, items, tocncx))

# create toc.ncx
epub.writestr("OEBPS/toc.ncx",
'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="%s"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>%s</text>
  </docTitle>
  <navMap>
    <navPoint id="navPoint-1" playOrder="1">
      <navLabel>
        <text>Start</text>
      </navLabel>
      <content src="Text/Section0001.xhtml"/>
    </navPoint>
  </navMap>
</ncx>
'''%(random, data.title))

print('work done.')

epub.close
