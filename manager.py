#!/usr/bin/env python
from flask.ext.script import Manager , Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db, models
from app.utils  import GunicornServer
import os

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver',Server(port=5000,host="0.0.0.0"))
manager.add_command('shell',Shell())
manager.add_command('gunicorn', GunicornServer(app))
manager.add_command('db',MigrateCommand)
@manager.command
def create_db():
        db.create_all()
        depts = ['CSE', 'EEE', 'ECE', 'MECH', 'PROD', 'ICE', 'META', 'CIVIL', 'ARCHI', 'CHEM']
        for dept in depts :
                entry = models.Department(department = dept)
                db.session.add(entry)
                db.session.commit()


@manager.command
def delete_db():
        db.drop_all()

        
manager.run()
