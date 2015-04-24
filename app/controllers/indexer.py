import urllib
import shutil
import glob
import os
import pycurl
from io import BytesIO
import pprint
import json


def index_it(file_name):
    c=pycurl.Curl()
    for root, dirs, files in os.walk("/home/sananth12/Desktop/Github/NotesSharing/tmp/"):
        for file in files:
            if str(file) == str(file_name):
                s="http://0.0.0.0:8983/solr/update/extract?stream.file="+root+urllib.quote(file, '')+"&stream.contentType=application/pdf&literal.id="+urllib.quote(file, '')
                print "SUCESS!!" + s
                c.setopt(c.URL,s)
                c.perform()
    os.system("curl 'http://0.0.0.0:8983/solr/update?stream.body=%3Ccommit/%3E' &")

def search(query):
    c = pycurl.Curl()
    data = BytesIO()
    
    Q = str('http://0.0.0.0:8983/solr/select?q=text:'+query+'&wt=json&indent=true')

    c.setopt(c.URL, Q)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()

    di = json.loads(data.getvalue())
    ans = di["response"]["docs"]
    books = []
    for i in ans:
        books.append(str(i["id"]))
    pprint.pprint(books)
    return books

# os.chdir("/home/solr/some_books/books.nitt.edu/books/new/Computers/")
# shutil.copy(os.path.join("/home/solr/tmpupload/",file),os.path.join("/home/solr/public_html/upload/",file))
# http://music.nitt.edu:8983/solr/update?stream.body=%3Ccommit/%3E                                                                        
# http://music.nitt.edu:8983/solr/select?q=text:**searchterm**&wt=json&indent=true&start=0&rows=200
