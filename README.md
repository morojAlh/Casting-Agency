# Casting Agency

## About
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
This is the capstone project for Full-stack development Nanodegree 🌟🌟

## Getting Started Localy
1. Clone repo `https://github.com/morojAlh/Casting-Agency.git`
2. Naviging to `/Casting-Agency` folder
3. Install all of the required packages 
    ```bash
    pip install -r requirements.txt
    ```
4. Create database
    ```
    dropdb casting_agency 
    createdb casting_agency 
    ```
5. Run the server
    ```bash
    FLASK_APP=app.py
    FLASK_DEBUG=true 
    flask run
    ```

## Testing
To run the tests, run
```
dropdb casting_agency_test 
createdb casting_agency_test 
python3 test_app.py
```

 
# API Referance 
### API is hosted live via 

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
OR 
```
{
    "code": "access_denied",
    "description": "you do not have permission"
}
```

The API will return three error types when requests fail:
| Error        | Message         |   description
| ------------- |:-------------: | -------------
| 400     | bad request    |
| 401     | access_denied | you do not have permission
| 401     | invalid_header | Authorization header is expected
| 404    | resource not found   |
| 422 | unprocssable     |

## Endpoints
## Movies

### GET /movies
Returns a list of movies objects and success value.

**Request:** 
* **Endpoint:** `GET /movies`

**Response:**
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 03 Mar 2019 00:00:00 GMT",
      "title": "Joker"
    }
  ],
  "success": true
}

```

### POST /movies
Create a new movie and return object of the new one and success value.

**Request:** 
* **Endpoint:** `POST /movies`
* **Parameters:** title - release_date

**Response:**
```
{
  "movie": {
    "id": 1,
    "release_date": "Sun, 03 Mar 2019 00:00:00 GMT",
    "title": "Joker"
  },
  "success": true
}
```

### PATCH /movies/<movie_id>
Update a movie and return object of the updated one and success value.

**Request:** 
* **Endpoint:** `PATCH /movies/<movie_id>`
* **Parameters:** title - release_date

**Response:**
```
{
  "movie": {
    "id": 1,
    "release_date": "Sun, 03 Mar 2019 00:00:00 GMT",
    "title": "Joker"
  },
  "success": true
}
```


### DELETE /movies/<movie_id>
Delete a movie and return list of movies objects and success value.

**Request:** 
* **Endpoint:** `DELETE /movies/<movie_id>`

**Response:**


```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 03 Mar 2019 00:00:00 GMT",
      "title": "Joker"
    }
  ],
  "success": true
}
```



## Actors

### GET /actors
Returns a list of actors objects and success value.

**Request:** 
* **Endpoint:** `GET /actors`

**Response:**
```
{
  "actors": [
    {
      "age": 45,
      "gender": "m",
      "id": 1,
      "name": "Brad Pitt"
    }
  ],
  "success": true
}

```

### POST /actors
Create a new actors and return object of the new one and success value.

**Request:** 
* **Endpoint:** `POST /actors`
* **Parameters:** name - age - gender

**Response:**
```
{
  "actor": {
    "age": 45,
    "gender": "m",
    "id": 1,
    "name": "Brad Pitt"
  },
  "success": true
}
```

### PATCH /actors/<actor_id>
Update a actor and return object of the updated one and success value.

**Request:** 
* **Endpoint:** `PATCH /actors/<actor_id>`
* **Parameters:** name - age - gender

**Response:**
```
{
  "actor": {
    "age": 42,
    "gender": "M",
    "id": 1,
    "name": "Brad Pitt"
  },
  "success": true
}
```


### DELETE /actors/<actor_id>
Delete a actors and return list of actors objects and success value.

**Request:** 
* **Endpoint:** `DELETE /actors/<actor_id>`

**Response:**


```
{
  "actors": [
    {
      "age": 45,
      "gender": "m",
      "id": 1,
      "name": "Brad Pitt"
    }
  ],
  
```

