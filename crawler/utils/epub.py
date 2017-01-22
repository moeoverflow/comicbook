import os.path
import zipfile
import uuid

class EPUB():
    def __init__(self, file_name):
        if '.epub' not in file_name:
            file_name += '.epub'

        full_file_name = os.path.expanduser(file_name)
        path = os.path.split(full_file_name)[0]
        if not os.path.exists(path):
            os.makedirs(path)
        self.epub = zipfile.ZipFile(full_file_name, 'w')

    title = ""
    author = ""
    subject = ""
    source = ""

    html_count = 0
    manifest = ""
    spine = ""
    cover = ""

    def addImage(self, file_name, data, cover=False):
        self.epub.writestr("OEBPS/Images/" + file_name, data)
        self.manifest += '	<item href="Images/%s" id="Images_%s" media-type="image/%s"/>\n'%(file_name, file_name, file_name.split('.')[-1])
        if cover:
            self.cover = 'Images_' + file_name
    def addHTML(self, title, content):
        self.html_count += 1
        self.epub.writestr("OEBPS/Text/Section_%04d.xhtml"%(self.html_count), xxx_xhtml.format(title=title, body=content))
        self.manifest += '  <item href="Text/Section_%04d.xhtml" id="Text_Section_%04d.xhtml" media-type="application/xhtml+xml"/>\n'%(self.html_count, self.html_count)
        self.spine += '  <itemref idref="Text_Section_%04d.xhtml"/>\n'%(self.html_count)
    def setCover(self, file_name):
        self.cover = "Images_%s"%(file_name)
    def close(self):
        random = uuid.uuid1()

        self.epub.writestr("mimetype", "application/epub+zip")
        self.epub.writestr("META-INF/container.xml", container_xml)
        self.epub.writestr("OEBPS/content.opf", content_opf.format(
            title=self.title,
            author=self.author,
            subject=self.subject,
            identifier=random,
            cover=self.cover,
            manifest=self.manifest,
            spine=self.spine,
            source=self.source))
        self.epub.writestr("OEBPS/toc.ncx", toc_ncx.format(uid=random, title=self.title))
        self.epub.close()



container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
'''
xxx_xhtml = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<!--?xml version='1.0' encoding='utf-8'?--><html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
</head>

<body>
{body}
</body>
</html>
'''

# title
content_opf = '''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="bookid" version="2.0">
  <metadata>
    <dc:title>{title}</dc:title>
    <dc:creator>{author}</dc:creator>
    <dc:subject>{subject}</dc:subject>
	<dc:identifier id="bookid">{identifier}</dc:identifier>
    <dc:source>{source}</dc:source>
    <dc:rights>created by hentaibook https://github.com/MoeOverflow/hentaibook</dc:rights>
    <dc:builder>hentaibook</dc:builder>
	<meta name="cover" content="{cover}" />
  </metadata>
  <manifest>
{manifest}
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
  </manifest>
  <spine toc="ncx">
{spine}
  </spine>
  <guide>
    <reference href="cover.html" type="cover" title="Cover"/>
  </guide>
</package>
'''

toc_ncx = '''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{uid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{title}</text>
  </docTitle>
</ncx>
'''
