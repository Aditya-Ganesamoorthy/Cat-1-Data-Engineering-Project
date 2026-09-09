import json
from unittest.mock import MagicMock

import pipeline.consumer as consumer
import pipeline.producer as producer


class FakeProducer:
    def __init__(self):
        self.messages = []

    def produce(self, topic, key, value, callback):
        self.messages.append((topic, key, json.loads(value)))
        callback(None, MagicMock(key=lambda: key))

    def poll(self, _timeout):
        return 0

    def flush(self):
        return 0


def test_publish_movies_sends_transformed_records(tmp_path, monkeypatch):
    payload = [
        {"tmdb_id": 7, "title": "Kafka Film"},
        {"title": "Missing ID"},
    ]
    input_file = tmp_path / "new_movies_transformed.json"
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    fake = FakeProducer()
    monkeypatch.setattr(producer, "INPUT_FILE", input_file)
    monkeypatch.setattr(producer, "create_producer", lambda: fake)

    producer.publish_movies()

    assert len(fake.messages) == 1
    assert fake.messages[0][0] == producer.KAFKA_TOPIC
    assert fake.messages[0][1] == "7"


class FakeMessage:
    def __init__(self, payload):
        self._payload = payload

    def error(self):
        return None

    def value(self):
        return json.dumps(self._payload).encode("utf-8")


def test_consume_movies_deduplicates_and_writes_output(tmp_path, monkeypatch):
    records = [
        {"tmdb_id": 1, "title": "First"},
        {"tmdb_id": 1, "title": "Duplicate"},
        {"tmdb_id": 2, "title": "Second"},
    ]
    queue = [FakeMessage(record) for record in records] + [None, None]

    fake_consumer = MagicMock()
    fake_consumer.poll.side_effect = queue

    monkeypatch.setattr(consumer, "create_consumer", lambda: fake_consumer)
    monkeypatch.setattr(consumer, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(consumer, "OUTPUT_FILE", tmp_path / "kafka_movies.json")
    monkeypatch.setattr(consumer, "IDLE_TIMEOUT", 0)

    movies = consumer.consume_movies()

    assert [movie["tmdb_id"] for movie in movies] == [1, 2]
    written = json.loads((tmp_path / "kafka_movies.json").read_text(encoding="utf-8"))
    assert written == movies
    fake_consumer.close.assert_called_once()
