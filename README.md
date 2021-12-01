# math-submission-service

## Setup
Use Python 3

First create a virtual environment and activate it
```
$ python -m venv venv
$ source venv/bin/activate
```

Install dependencies with
```
$ pip install -r requirements.txt
```

Setup the database with
```
$ flask db upgrade
```

## Develop

Run app with
```
$ flask run
```

Access it on [localhost](localhost:5000)


## Add New Dependencies

```
# install em with pip in the venv
$ pip freeze --local > requirements.txt
