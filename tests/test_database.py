import sqlite3

from database.movie_database import create_table, insert_movies


def _connection():
    connection = sqlite3.connect(":memory:")
    create_table(connection)
    return connection


def test_insert_movies_loads_new_records():
    connection = _connection()
    movies = [
        {
            "tmdb_id": 101,
            "title": "New Film",
            "overview": "Plot",
            "release_date": "2024-01-01",
            "popularity": 10.5,
            "vote_average": 7.1,
            "vote_count": 100,
            "original_language": "en",
            "adult": 0,
            "genre_ids": "[28]",
            "poster_path": None,
            "backdrop_path": None,
            "genres": "Action",
        }
    ]

    inserted, skipped = insert_movies(connection, movies)
    connection.commit()

    count = connection.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    connection.close()

    assert inserted == 1
    assert skipped == 0
    assert count == 1


def test_insert_movies_skips_duplicates_and_missing_ids():
    connection = _connection()
    first = {"tmdb_id": 101, "title": "A"}
    duplicate = {"tmdb_id": 101, "title": "A again"}
    missing_id = {"title": "No ID"}

    insert_movies(connection, [first])
    inserted, skipped = insert_movies(connection, [duplicate, missing_id])
    connection.close()

    assert inserted == 0
    assert skipped == 2
