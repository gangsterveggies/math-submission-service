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

## Test Setup

To setup a debug environment run the following
```
$ flask setup-debug
```

## Add New Dependencies

```
# install em with pip in the venv
$ pip freeze --local > requirements.txt
