# Flask Boilerplate
# By Jay Ravaliya

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

import secret

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secret.DBKEY 

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('apichoosinator', MigrateCommand)

class Test(db.Model):

	__tablename__ = "test"

	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Text)

	def __init__(self, value):
		self.value = value

if __name__ == "__main__":
	manager.run()
