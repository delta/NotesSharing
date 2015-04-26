import urllib
#import shutil
#import glob
import os
import pycurl
from io import BytesIO
import pprint
import json
import requests

def index_it(file_name,fileFormat):
    c=pycurl.Curl()
    basedir = os.path.abspath(os.path.dirname(__file__))
    for root, dirs, files in os.walk(basedir+'/../../tmp/'):
        for file in files:
            if str(file) == str(file_name):
                x = "http://0.0.0.0:8983/solr/firenotes/update/extract?literal.id="+urllib.quote(file,'')+"&commit=true&stream.contentType="+fileFormat+"'"
                print x
                y = " -F 'myfile=@"+basedir+"/../../tmp/"+file+"'"
                cmd = "curl '"
                os.system(cmd + x + y )
                print "SUCESS!!"
    print 'COMON ITS INDEXED NOW ' + file_name
    
def search(query):
    print query
    c = pycurl.Curl()
    data = BytesIO()
    
    Q = str('http://0.0.0.0:8983/solr/firenotes/select?q=text:'+query+'&wt=json&indent=true')
    #Q = "http://0.0.0.0:8983/solr/firenotes/select?wt=json&indent=true&q="+query
    #print 'RESPONSE ' + Q
    c.setopt(c.URL, Q)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    try:
        di = json.loads(data.getvalue())
        #print di
        ans = di["response"]["docs"]
        #print ans
        books = []
        for i in ans:
            #print i
            try:    
                books.append(str(i["id"]))
            except:
                pass
        return list(set(books))
    except:
        return []

# os.chdir("/home/solr/some_books/books.nitt.edu/books/new/Computers/")
# shutil.copy(os.path.join("/home/solr/tmpupload/",file),os.path.join("/home/solr/public_html/upload/",file))
# http://music.nitt.edu:8983/solr/update?stream.body=%3Ccommit/%3E                                                                        
# http://music.nitt.edu:8983/solr/select?q=text:**searchterm**&wt=json&indent=true&start=0&rows=200
