import urllib
import pycurl
import requests
c= pycurl.Curl()
requests.post("http://localhost:8983/solr/firenotes/update/extract?literal.id=Ch6_STLAssociativeContainersAndIterators.pdf&commit=true -F myfile=@/home/nirvik/Dev/code/FLASK_APPS/fireNotes/app/controllers/../../tmp/Ch6_STLAssociativeContainersAndIterators.pdf")
#c.setopt(c.URL,s)
#c.perform()
print c
