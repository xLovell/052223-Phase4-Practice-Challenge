# Flask Code Challenge - Late Show

For this assessment, you'll be working with Late Night TV show domain.

In this repo:

- There is a Flask application with some features built out.
- There are tests included which you can run using `pytest -x`.
- There is a file `challenge-4-lateshow.postman_collection.json` that contains a
  Postman collection of requests for testing each route you will implement.

Depending on your preference, you can either check your API by:

- Using Postman to make requests
- Running `pytest -x` and seeing if your code passes the tests

You can import `challenge-4-lateshow.postman_collection.json` into Postman by
pressing the `Import` button.

![import postman](https://curriculum-content.s3.amazonaws.com/6130/phase-4-code-challenge-instructions/import_collection.png)

Select `Upload Files`, navigate to this repo folder, and select
`challenge-4-lateshow.postman_collection.json` as the file to import.

## Setup

The instructions assume you changed into the `code-challenge` folder **prior**
to opening the code editor.

To download the dependencies for the backend, run:

```console
pipenv install
pipenv shell
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Models

You will implement an API for the following data model:

![domain diagram](https://curriculum-content.s3.amazonaws.com/6130/p4-code-challenge-4/domain.png)

The application keeps track of the guests that have appeared on the show. There
are three models in the domain: `Guest`, `Episode`, and `Appearance`.

The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db upgrade head
```

Now you can implement the relationships as shown in the ER Diagram:

You need to create the following relationships:

- An `Episode` has many `Guest`s through `Appearance`
- A `Guest` has many `Episode`s through `Appearance`
- An `Appearance` belongs to a `Guest` and belongs to an `Episode`

Update `server/models.py` to establish the model relationships. Since an
`Appearance` belongs to a `Episode` and a `Guest`, configure the model to
cascade deletes.

Set serialization rules to limit the recursion depth.

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
flask db upgrade head
python server/seed.py
```

> Note that this seed file uses a CSV file to populate the database. If you
> aren't able to get the provided seed file working, you are welcome to generate
> your own seed data to test the application.

## Validations

Add validations to the `Appearance` model:

- must have a `rating` between 1 and 5 (inclusive - 1 and 5 are okay)

## Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

### GET /episodes

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### GET /episodes/<int:id>

If the `Episode` exists, return JSON data in the format below:

```json
{
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1,
    "appearances": [
        {
            "episode_id": 1,
            "guest": {
                "id": 1,
                "name": "Michael J. Fox",
                "occupation": "actor"
            },
            "guest_id": 1,
            "id": 1,
            "rating": 4
        }
    ]
}
```

If the `Episode` does not exist, return the following JSON data, along with the
appropriate HTTP status code:

```json
{
  "error": "Episode not found"
}
```

### DELETE /episodes/<int:id>

If the `Episode` exists, it should be removed from the database, along with any
`Appearance`s that are associated with it (an `Appearance` belongs to an
`Episode`, so you need to delete the `Appearance`s before the `Episode` can be
deleted).

After deleting the `Episode`, return an _empty_ response body, along with the
appropriate HTTP status code.

If the `Episode` does not exist, return the following JSON data, along with the
appropriate HTTP status code:

```json
{
  "error": "Episode not found"
}
```

### GET /guests

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  },
  {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
]
```

### POST /appearances

This route should create a new `Appearance` that is associated with an existing
`Episode` and `Guest`. It should accept an object with the following properties
in the body of the request:

```json
{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}
```

If the `Appearance` is created successfully, send back a response with the
following data:

```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

If the `Appearance` is **not** created successfully, return the following JSON
data, along with the appropriate HTTP status code:

```json
{
  "errors": ["validation errors"]
}
```
