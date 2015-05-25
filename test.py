import requests 
import threading 
import random
url = 'http://notes.deltaforce.club/'
a = ['CSE/','ECE/','CHEM/','ARCHI/','META/','MECH/','EEE/','CIVIL/','ICE/']
args = [url+j+str(i) for i in range(1,9) for j in a ]

def worker():
    choose = random.choice(args)
    x= requests.get(choose)

    if x.status_code!=200:
        print choose 
        print x.status_code  

threads = []

for i in range(20):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()




