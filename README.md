# ny_taxi

## install

- requires pipenv and a python version stated in [Pipfile](Pipfile)
- `pipenv install`

## Concept

Under [etl](etl) all tasks of a bigger DAG are defined.
Each task is always separated in extraxct/transform/load.
One dir is used for reading/writing files.
(Actually, these are not glued to an Airflow DAG yet, but are designated for this.)

### Tasks 
Small scripts which represent different parts of a DAG
- requires taxi csv [data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) in location [resources/data](resources/data) together with lookup file `taxi+_zone_lookup.csv`

#### run preprocessor
- `pipenv shell`
- in the shell, run `pipenv run task:preprocess` 

#### run ranker
- `pipenv shell`
- in the shell, run `pipenv run task:ranking` 

## notebook
under [notebooks](notebooks):
- used for modelling DAG task logic (*modeling.ipynb)
- used for query examples (*sample_queries.ipynb)
- `pipenv shell`
- in pipenv shell run `jupyter-notebook`

## ci
- `pipenv run ci:lint` --> search for code to lint
- `pipenv run ci:lint:ci` --> actually lint code
- `pipenv run ci:test` --> unittests (no integration tests)

# caveats/not done in this approach:
- tasks would rather read and write on true SQL DBS or Spark Data Stores than on local files
- tasks would operate rather on spark dataframes then on pandas dataframes (or would do the enrichment via sql statements)
- data quality steps should be introduced as extra tasks before and after each core etl
- orchestrator like Airflow is needed to coordinate tasks
- tasks would be deployed in a docker environment (k8s, AWS Batch/EC2 or similar)
- if using files in prod system, we would store it in a zipped format




