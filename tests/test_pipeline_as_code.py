from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
DAG_FILE = ROOT / "airflow" / "dags" / "movie_pipeline_dag.py"
CONFIG_FILE = ROOT / "configs" / "pipeline.yaml"
COMPOSE_FILE = ROOT / "airflow" / "docker-compose.yml"


def test_pipeline_config_matches_dag_and_quality_rules():
    config = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    dag_source = DAG_FILE.read_text(encoding="utf-8")

    assert config["pipeline"]["name"] in dag_source
    assert config["kafka"]["topic"] == "movie_pipeline"
    assert "id" in config["quality"]["required_fields"]
    assert COMPOSE_FILE.exists()


def test_dag_declares_etl_task_order():
    dag_source = DAG_FILE.read_text(encoding="utf-8")
    expected_tasks = [
        "incremental_extract",
        "stage_movies",
        "validate_movies",
        "transform_movies",
        "publish_to_kafka",
        "consume_from_kafka",
        "load_to_sqlite",
        "run_eda",
    ]

    for task in expected_tasks:
        assert f'task_id="{task}"' in dag_source
