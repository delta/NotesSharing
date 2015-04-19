import urllib
import shutil
import glob
import os
import pycurl
#os.chdir("/home/solr/some_books/books.nitt.edu/books/new/Computers/")
c=pycurl.Curl()
for root, dirs, files in os.walk("/home/ananth/tmp/"):
        for file in files:
                s="http://localhost:8983/solr/update/extract?stream.file="+root+urllib.quote(file, '')+"&stream.contentType=application/pdf&literal.id="+urllib.quote(file, '')
                print s
                c.setopt(c.URL,s)
                c.perform()
#                shutil.copy(os.path.join("/home/solr/tmpupload/",file),os.path.join("/home/solr/public_html/upload/",file))


