from app import setup_app

app, db = setup_app()

if __name__ == "__main__":
	app.run()
