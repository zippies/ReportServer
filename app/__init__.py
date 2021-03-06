# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
	app = Flask(__name__)
	config = Config()
	app.config.from_object(config)
	config.init_app(app)
	db.init_app(app)
	from .main import url as BluePrint
	app.register_blueprint(BluePrint)
	return(app)
