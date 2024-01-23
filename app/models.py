from . import db


class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	artist = db.Column(db.String(50), nullable=True)
	album = db.Column(db.String(100))
	duration_seconds = db.Column(db.Integer)
	genre = db.Column(db.String(50))
	release_date = db.Column(db.Date)

	def __init__(
			self,
			title: str,
			artist: str,
			album: str,
			duration_seconds: int,
			genre: str,
			release_date,
	) -> None:

		self.title = title
		self.artist = artist
		self.genre = genre
		self.release_date = release_date
		self.album = album
		self.duration_seconds = duration_seconds

	def __repr__(self) -> str:
		return f"<Song {self.title} by {self.artist} ({self.genre})>"
