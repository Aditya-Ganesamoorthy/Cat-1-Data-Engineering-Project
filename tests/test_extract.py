from unittest.mock import MagicMock

import pipeline.extract as extract
import pipeline.incremental_extract as incremental


def test_extract_movies_uses_mocked_tmdb_pages(tmp_path, monkeypatch):
    monkeypatch.setattr(extract, "TMDB_API_KEY", "test-key")
    monkeypatch.setattr(extract, "TARGET_COUNT", 2)
    monkeypatch.setattr(extract, "RAW_DIR", tmp_path)
    monkeypatch.setattr(extract, "OUTPUT_FILE", tmp_path / "raw_movies.json")
    monkeypatch.setattr(extract.time, "sleep", lambda *_args, **_kwargs: None)

    pages = {
        1: {
            "results": [
                {"id": 1, "title": "Movie One"},
                {"id": 2, "title": "Movie Two"},
            ]
        }
    }

    monkeypatch.setattr(
        extract,
        "fetch_page",
        lambda page: pages[page],
    )

    movies = extract.extract_movies()

    assert len(movies) == 2
    assert movies[0]["title"] == "Movie One"
    assert (tmp_path / "raw_movies.json").exists()


def test_fetch_new_movies_skips_ids_already_in_database(monkeypatch):
    monkeypatch.setattr(incremental, "API_KEY", "test-key")
    monkeypatch.setattr(incremental, "TARGET_NEW_MOVIES", 1)
    monkeypatch.setattr(incremental.time, "sleep", lambda *_args, **_kwargs: None)

    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "results": [
            {"id": 10, "title": "Already Loaded"},
            {"id": 11, "title": "Brand New"},
        ]
    }

    session = MagicMock()
    session.get.return_value = response

    monkeypatch.setattr(
        incremental,
        "create_session",
        lambda: session,
    )

    movies = incremental.fetch_new_movies({10})

    assert len(movies) == 1
    assert movies[0]["id"] == 11
    session.close.assert_called_once()
