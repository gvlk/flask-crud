from flask import Blueprint, render_template, redirect, url_for, request ,Response

from . import db
from .models import Song
from random import choice, randint
from datetime import datetime


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home() -> str:
	songs = Song.query.all()
	return render_template("index.html", songs=songs)


@main_bp.route('/populate', methods=['POST'])
def populate_songs() -> Response:
	if request.method == 'POST':
		Song.query.delete()
		db.session.commit()

		titles = ("Song A", "Song B", "Song C")
		artists = ("Artist X", "Artist Y", "Artist Z")
		albums = ("Album 1", "Album 2", "Album 3")
		genres = ("Pop", "Rock", "Hip Hop")
		lyrics = "Sample lyrics"

		for i in range(10):
			title = choice(titles)
			artist = choice(artists)
			album = choice(albums)
			duration_seconds = randint(180, 300)
			genre = choice(genres)
			release_date = "2022-01-01"

			song = Song(
				title=title,
				artist=artist,
				album=album,
				duration_seconds=duration_seconds,
				genre=genre,
				release_date=release_date,
				lyrics=lyrics
			)
			db.session.add(song)

		db.session.commit()
	return redirect(url_for('main.home'))


@main_bp.route('/create', methods=['POST'])
def create_song() -> Response | str:
	if request.method == 'POST':
		# Retrieve data from the form
		title = request.form.get('title')
		artist = request.form.get('artist')
		album = request.form.get('album')
		duration_seconds = request.form.get('duration_seconds')
		genre = request.form.get('genre')
		release_date = request.form.get('release_date')
		lyrics = request.form.get('lyrics')

		duration_seconds = int(duration_seconds) if duration_seconds else 0
		release_date = release_date if release_date else datetime.now()

		# Create a new Song instance
		new_song = Song(
			title=title,
			artist=artist,
			album=album,
			duration_seconds=duration_seconds,
			genre=genre,
			release_date=release_date,
			lyrics=lyrics
		)

		# Add the new song to the database
		db.session.add(new_song)
		db.session.commit()

	return redirect(url_for('main.home'))


@main_bp.route('/update/<int:song_id>', methods=['POST'])
def update_song(song_id: int) -> Response:
	if request.method == 'POST':
		# Retrieve data from the form
		title = request.form.get('title')
		artist = request.form.get('artist')
		album = request.form.get('album')
		duration_seconds = int(request.form.get('duration_seconds'))
		genre = request.form.get('genre')
		release_date = request.form.get('release_date')
		lyrics = request.form.get('lyrics')

		# Find the song to update by its ID
		song_to_update = Song.query.get(song_id)

		# Update the song attributes
		song_to_update.title = title
		song_to_update.artist = artist
		song_to_update.album = album
		song_to_update.duration_seconds = duration_seconds
		song_to_update.genre = genre
		song_to_update.release_date = release_date
		song_to_update.lyrics = lyrics

		# Commit the changes to the database
		db.session.commit()

	return redirect(url_for('main.home'))


@main_bp.route('/delete/<int:song_id>', methods=['POST'])
def delete_song(song_id: int) -> Response:
	song_to_delete = Song.query.get(song_id)

	db.session.delete(song_to_delete)
	db.session.commit()

	return redirect(url_for('main.home'))
