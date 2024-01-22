import psycopg2.errors
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect

USERNAME = "postgres"
PASSWORD = "root"
HOST = "localhost"
DATABASE = "flask_crud"

db = SQLAlchemy()


def setup_app() -> tuple[Flask, SQLAlchemy]:
	try:
		conn = connect(user=USERNAME, password=PASSWORD, host=HOST)
		cursor = conn.cursor()
		conn.autocommit = True
		cursor.execute(f'CREATE DATABASE {DATABASE}')
		cursor.close()
		conn.close()
	except psycopg2.errors.DuplicateDatabase:
		print(f"Database {DATABASE} already exists")

	app = Flask(__name__)
	app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	from .views import main_bp
	app.register_blueprint(main_bp)

	db.init_app(app)
	with app.app_context():
		db.create_all()

	return app, db
