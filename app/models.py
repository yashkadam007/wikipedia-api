from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255))
    result = db.Column(db.String)
    status = db.Column(db.String)