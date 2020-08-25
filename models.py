import os
from sqlalchemy import Column, String, DateTime, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "casting-agency"
# database_path = "postgres://{}/{}".format('postgres@localhost:5432', database_name)

# run API localy
database_path = os.environ.get("DATABASE_URL", "postgres://postgres@localhost:5432/casting_agency")

# 
# database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()

# def db_drop_and_create_all():
#     db.drop_all()
#     db.create_all()


class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(DateTime())

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }

'''
Category

'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }