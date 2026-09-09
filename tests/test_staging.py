import json

import pipeline.staging as staging


def test_stage_movies_copies_raw_list_to_staging(tmp_path, monkeypatch):
    raw_file = tmp_path / "new_movies.json"
    staged_file = tmp_path / "staged.json"
    movies = [{"id": 1, "title": "A"}, {"id": 2, "title": "B"}]
    raw_file.write_text(json.dumps(movies), encoding="utf-8")

    monkeypatch.setattr(staging, "INPUT_FILE", raw_file)
    monkeypatch.setattr(staging, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(staging, "OUTPUT_FILE", staged_file)

    staging.stage_movies()

    staged = json.loads(staged_file.read_text(encoding="utf-8"))
    assert staged == movies


def test_stage_movies_rejects_non_list_payload(tmp_path, monkeypatch):
    raw_file = tmp_path / "new_movies.json"
    raw_file.write_text(json.dumps({"id": 1}), encoding="utf-8")

    monkeypatch.setattr(staging, "INPUT_FILE", raw_file)
    monkeypatch.setattr(staging, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(staging, "OUTPUT_FILE", tmp_path / "staged.json")

    try:
        staging.stage_movies()
        raise AssertionError("Expected ValueError")
    except ValueError as error:
        assert "must be a list" in str(error)
