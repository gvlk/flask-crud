import psycopg2.errors
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect


db = SQLAlchemy()


def setup_app(username: str, password: str, host: str, database: str) -> tuple[Flask, SQLAlchemy]:
	try:
		conn = connect(user=username, password=password, host=host)
		cursor = conn.cursor()
		conn.autocommit = True
		cursor.execute(f'CREATE DATABASE {database}')
		cursor.close()
		conn.close()
	except psycopg2.errors.DuplicateDatabase:
		print(f"Database {database} already exists")

	app = Flask(__name__)
	app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@{host}/{database}"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	from .views import main_bp
	app.register_blueprint(main_bp)

	db.init_app(app)
	with app.app_context():
		db.create_all()

	return app, db
