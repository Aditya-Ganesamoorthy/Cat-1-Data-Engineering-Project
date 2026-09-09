import json

from pipeline.transform import convert_genres, transform_movie


def test_convert_genres_maps_known_ids():
    assert convert_genres([28, 12]) == "Action, Adventure"


def test_convert_genres_ignores_unknown_ids():
    assert convert_genres([28, 99999]) == "Action"


def test_convert_genres_handles_non_list():
    assert convert_genres(None) == ""
    assert convert_genres("28") == ""


def test_transform_movie_renames_and_cleans_fields(sample_movie):
    result = transform_movie(sample_movie)

    assert result["tmdb_id"] == 550
    assert result["title"] == "Fight Club"
    assert result["overview"] == "An insomniac office worker."
    assert result["adult"] == 0
    assert result["genres"] == "Drama, Thriller, Thriller"
    assert json.loads(result["genre_ids"]) == [18, 53, 53]


def test_transform_movie_defaults_missing_optional_fields():
    result = transform_movie({"id": 1, "title": "Solo"})

    assert result["popularity"] == 0
    assert result["vote_average"] == 0
    assert result["vote_count"] == 0
    assert result["genres"] == ""
    assert result["genre_ids"] == "[]"
