import os
from sqlalchemy import Column, String, DateTime, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ.get("DATABASE_URL", "postgres://postgres@localhost:5432/casting_agency")
# database_path = os.environ.get("DATABASE_URL", "postgres://xzkklzlapkrcvr:e758762e9287fe1289f2fda6785c5cf924ddfd632ba1e57e89f7c2ab9620b249@ec2-54-236-146-234.compute-1.amazonaws.com:5432/d8fof9gprovnvq")


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