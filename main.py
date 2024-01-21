from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from views import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/flask_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
	app.run()
