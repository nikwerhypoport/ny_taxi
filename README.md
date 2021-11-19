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
- in the shell, run `pipenv run preprocess` 

#### run ranker
- `pipenv shell`
- in the shell, run `pipenv run ranking` 

## notebook
Used for modelling code for different DAG Tasks under [notebooks](notebooks).
- `pipenv shell`
- in pipenv shell run `jupyter-notebook`

# caveats/not done in this approach:
- tasks would read and write on True SQL DBS or Spark Data Stores than on local files
- tasks would operate rather on spark dataframes then on pandas dataframes (or would do the enrichment via sql statements)
- there would be a professional orchestrator like Airflow
- tasks would be deployed in a Docker Env 




