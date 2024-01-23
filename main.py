# https://github.com/gvlk/flask-crud
# Guilherme Azambuja - 149429

from app import setup_app

USERNAME = "postgres"
PASSWORD = "root"
HOST = "localhost"
DATABASE = "flask_crud"

app, db = setup_app(
	USERNAME,
	PASSWORD,
	HOST,
	DATABASE
)

if __name__ == "__main__":
	app.run()
