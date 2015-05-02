![alt text](./app/static/images/logo.png "Fire Notes")

Fire Notes is a notes sharing platform where students can upload, maintain versions and download notes.

##To do 
- [x] Add apache solr for document search 
- [x] Add Star feature 
- [x] Add Download Counter 
- [x] Add Meta Data before uploading file
- [x] Search files by metadata 
- [ ] Add subjects of each semester to database 
- [ ] Subjects Scraper 
- [x] Concatenate the files into a single pdf 
- [x] Upload multiple files at once 

##How to run
* drop all db
* delete app.db
* delete search.db (Whoosh index)
* delete migration folder
* start redis-server
* initiate apache solr -> ./bin/solr start -e cloud -noprompt
```py
python manager.py create_db
python manager.py db init
python manager.py gunicorn
```

##Features
* Upload and download notes.
* Anybody can download any version of the file.
* People can upload notes only to the deparment they belong to.

##Contribute
If you want to add features, fix bugs, or report issues, feel free to send a pull request!!

####Contributors
* Nirvik Ghosh
* Sriram S
* Anantha Natarajan
* Vignesh Manix


