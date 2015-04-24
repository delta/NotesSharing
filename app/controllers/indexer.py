import urllib
#import shutil
#import glob
import os
import pycurl
from io import BytesIO
import pprint
import json
import requests

def index_it(file_name):
    c=pycurl.Curl()
    basedir = os.path.abspath(os.path.dirname(__file__))
    for root, dirs, files in os.walk(basedir+'/../../tmp/'):
        for file in files:
            if str(file) == str(file_name):
                #s="http://0.0.0.0:8983/solr/update/extract?stream.file="+root+urllib.quote(file, '')+"&stream.contentType=application/pdf&literal.id="+urllib.quote(file, '')
#                s = "http://localhost:8983/solr/firenotes/update/extract?literal.id="+urllib.quote(file,'')+"&commit=true -F myfile=@" + basedir+"/../../tmp/"+file
                x = "http://localhost:8983/solr/firenotes/update/extract?literal.id="+urllib.quote('nirvik','')+"&commit=true'"
                y = " -F 'myfile=@"+basedir+"/../../tmp/"+file+"'"
                cmd = "curl '"
                os.system(cmd + x + y )
                #requests.post(s)
                #c.setopt(c.URL,s)
                #c.perform()
                print "SUCESS!!"
    print 'COMON ITS INDEXED NOW ' + file_name
    
def search(query):
    print query
    c = pycurl.Curl()
    data = BytesIO()
    
    #Q = str('http://0.0.0.0:8983/solr/select?q=text:'+query+'&wt=json&indent=true')
    Q = "http://localhost:8983/solr/firenotes/select?wt=json&indent=true&q="+query
    print 'RESPONSE ' + Q
    c.setopt(c.URL, Q)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    try:
        di = json.loads(data.getvalue())
        print di
        ans = di["response"]["docs"]
        books = []
        for i in ans:
            try:    
                books.append(str(i["stream_name"][0]))
            except:
                pass
    #pprint.pprint(books)
        return books
    except:
        return []

# os.chdir("/home/solr/some_books/books.nitt.edu/books/new/Computers/")
# shutil.copy(os.path.join("/home/solr/tmpupload/",file),os.path.join("/home/solr/public_html/upload/",file))
# http://music.nitt.edu:8983/solr/update?stream.body=%3Ccommit/%3E                                                                        
# http://music.nitt.edu:8983/solr/select?q=text:**searchterm**&wt=json&indent=true&start=0&rows=200
