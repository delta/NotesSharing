from app import db, models 

models.files.query.delete()
db.session.commit()
