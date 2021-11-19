# ny_taxi

## install

- requires pipenv and a python version stated in [Pipfile](Pipfile)
- `pipenv install`


## run preprocessor
Small script for reducing size of data and enriching necessary columns for the next steps.
- requires taxi csv [data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) in location [resources/data](resources/data) togehter with lookup file `taxi+_zone_lookup.csv`
- `pipenv shell`
- in the shell, run `pipenv run preprocess` 

## notebook
- just for testing 
- `pipenv shell`
- in pipenv shell run `jupyter-notebook`


