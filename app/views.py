from datetime import datetime
from random import choice, randint

from flask import Blueprint, render_template, redirect, url_for, request, Response

from . import db
from .models import Song

main_bp = Blueprint('main', __name__)


class SampleData:
	TITLES = (
		"Song A", "Song B", "Song C", "Song D", "Song E",
		"Song F", "Song G", "Song H", "Song I", "Song J"
	)

	ARTISTS = (
		"Artist X", "Artist Y", "Artist Z", "Artist W", "Artist V",
		"Artist U", "Artist T", "Artist S", "Artist R", "Artist Q"
	)

	ALBUMS = (
		"Album 1", "Album 2", "Album 3", "Album 4", "Album 5",
		"Album 6", "Album 7", "Album 8", "Album 9", "Album 10"
	)

	GENRES = (
		"Pop", "Rock", "Hip Hop", "Country", "Electronic",
		"R&B", "Jazz", "Blues", "Reggae", "Classical"
	)


@main_bp.route('/')
def home(**kwargs) -> str:
	songs = Song.query.all()
	return render_template("index.html", songs=songs, kwargs=kwargs)


@main_bp.route('/insert', methods=['POST'])
def insert_song() -> Response | str:
	# Retrieve data from the form
	(
		title,
		artist,
		album,
		duration_seconds,
		genre,
		release_date,
	) = process_form_data()

	# Create a new Song instance
	new_song = Song(
		title=title,
		artist=artist,
		album=album,
		duration_seconds=duration_seconds,
		genre=genre,
		release_date=release_date,
	)

	# Add the new song to the database
	db.session.add(new_song)
	db.session.commit()

	return redirect(url_for('main.home'))


@main_bp.route('/update/<int:song_id>', methods=['POST'])
def update_song(song_id: int) -> Response | str:
	(
		title,
		artist,
		album,
		duration_seconds,
		genre,
		release_date,
	) = process_form_data()

	# Find the song to update by its ID
	song_to_update = Song.query.get(song_id)

	# Update the song attributes
	song_to_update.title = title
	song_to_update.artist = artist
	song_to_update.album = album
	song_to_update.duration_seconds = duration_seconds
	song_to_update.genre = genre
	song_to_update.release_date = release_date

	# Commit the changes to the database
	db.session.commit()

	return redirect(url_for('main.home'))


@main_bp.route('/remove/<int:song_id>', methods=['POST'])
def remove_song(song_id: int) -> Response:
	song_to_delete = Song.query.get(song_id)

	db.session.delete(song_to_delete)
	db.session.commit()

	return redirect(url_for('main.home'))


@main_bp.route('/populate', methods=['POST'])
def populate_songs() -> Response:
	db.session.commit()

	for i in range(10):
		title = choice(SampleData.TITLES)
		artist = choice(SampleData.ARTISTS)
		album = choice(SampleData.ALBUMS)
		duration_seconds = randint(120, 300)
		genre = choice(SampleData.GENRES)
		release_date = f"{randint(1900, 2030)}-{randint(1, 12)}-{randint(1, 28)}"

		song = Song(
			title=title,
			artist=artist,
			album=album,
			duration_seconds=duration_seconds,
			genre=genre,
			release_date=release_date,
		)
		db.session.add(song)

	db.session.commit()
	return redirect(url_for('main.home'))


@main_bp.route('/clear', methods=['POST'])
def clear_table() -> Response:
	Song.query.delete()
	db.session.commit()

	return redirect(url_for('main.home'))


def process_form_data() -> tuple:
	title = request.form.get('title')
	artist = request.form.get('artist')
	album = request.form.get('album')
	raw_duration_seconds = request.form.get('duration_seconds')
	genre = request.form.get('genre')
	raw_release_date = request.form.get('release_date')

	duration_seconds = int(raw_duration_seconds) if raw_duration_seconds else 0
	release_date = raw_release_date if raw_release_date else datetime.now()

	return title, artist, album, duration_seconds, genre, release_date
