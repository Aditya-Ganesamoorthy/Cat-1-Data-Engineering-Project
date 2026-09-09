# CAT-1 Movie Data Engineering Pipeline

Incremental TMDB movie ETL with Apache Airflow, Confluent Kafka, SQLite, EDA reports, and a Power BI dashboard. This repository treats the pipeline as versioned code and runs automated tests on every push.

## Pipeline as code

Infrastructure and runtime settings live in files, not in manual server clicks:

| Artifact | Role |
| --- | --- |
| `airflow/docker-compose.yml` | Airflow, Postgres, Zookeeper, Kafka |
| `airflow/Dockerfile` | Airflow image with Kafka client |
| `airflow/dags/movie_pipeline_dag.py` | Orchestration DAG |
| `configs/pipeline.yaml` | Extract, path, Kafka, and data-quality settings |
| `.env.example` | Required environment variables (no secrets) |

Copy `.env.example` to `.env` and add a TMDB API key locally. `.env` is gitignored.

## Git branching for data engineering

Use branches that match how data teams change code, schemas, and jobs:

```text
main          # stable pipeline that can run in Airflow
develop       # integration branch for the next demo/release
feature/*     # DAG, transform, or test changes
hotfix/*      # production-breaking pipeline fixes
```

Suggested flow:

1. Create `feature/<short-name>` from `develop` (or `main` if you only use one integration branch).
2. Change transformation or DAG code and add or update unit tests.
3. Open a pull request into `develop`. GitHub Actions must pass.
4. Merge to `main` when the pipeline is ready to run locally with Docker.

Keep **code and configs** in Git. Keep API keys, SQLite databases, Airflow logs, and generated JSON/CSV out of Git. Schema changes belong in the same PR as the transform and load code that uses them.

## Continuous integration

GitHub Actions workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

On push and pull request it:

- installs Python 3.11 and `requirements-dev.txt`
- runs pytest unit tests for transforms and validation
- mock-tests TMDB extract and Kafka produce/consume (no live API or broker)
- checks `configs/pipeline.yaml` and Docker Compose presence

Run the same checks locally:

```bash
pip install -r requirements-dev.txt
pytest tests -v
```

## Local stack

```bash
cd airflow
docker compose up --build
```

Airflow UI: `http://localhost:8080` (default user `admin` / `password` `admin`). Unpause `movie_data_pipeline`. Each successful run updates `database/movies.db`, which Power BI can refresh from.

## Layout

```text
pipeline/     extract, stage, validate, transform, Kafka
database/     SQLite load
analytics/    EDA reports
airflow/      DAG + Docker stack
configs/      pipeline-as-code settings
tests/        unit and mock tests
```
