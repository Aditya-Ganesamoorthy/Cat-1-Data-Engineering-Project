from pipeline.validation import validate_movie


def test_validate_movie_accepts_complete_record(sample_movie):
    assert validate_movie(sample_movie) == []


def test_validate_movie_reports_missing_required_fields():
    errors = validate_movie({})

    assert "Missing field: id" in errors
    assert "Missing title" in errors
    assert "Invalid genre_ids" in errors


def test_validate_movie_rejects_empty_title(sample_movie):
    sample_movie["title"] = ""
    errors = validate_movie(sample_movie)
    assert "Missing title" in errors


def test_validate_movie_rejects_non_list_genre_ids(sample_movie):
    sample_movie["genre_ids"] = "18,53"
    errors = validate_movie(sample_movie)
    assert "Invalid genre_ids" in errors


def test_validate_movie_rejects_null_metrics(sample_movie):
    sample_movie["popularity"] = None
    sample_movie["vote_average"] = None
    errors = validate_movie(sample_movie)
    assert "Missing popularity" in errors
    assert "Missing vote average" in errors
