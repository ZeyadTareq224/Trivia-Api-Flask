# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Api Refernce:

Getting Started:
	- Base URL: at present this app can only be run locally and is not hosted as a base url, the backend app is hosted at the default http://localhots:5000 which is set as a proxy in the fornend configuration

	- authentication: this version of the application does not require authentication or Api keys

Endpoints
GET '/api/categories'
GET '/api/questions'
GET '/api/categories/{id}/questions'
POST '/api/questions'
DELETE '/api/{id}/questions'
POST '/api/quizzes'
POST '/api/search'
GET '/api/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/api/questions'
- returns a list of question objects, a total number of questions and categories
- questions are paginated in groups of 10 usin the 'page' argument that gets assigned to an integer value startin form 1

{
	'questions':[
	{'id': 6, 'question': 'how old are u?', 'answer': '18 years old', 'category': 2, 'difficulty': 1},
	{'id': 7, 'question': 'how are u?', 'answer': 'fine thanks', 'category': 2, 'difficulty': 1},
	{'id': 8, 'question': 'how old are brother?', 'answer': '15 years old', 'category': 2, 'difficulty': 1},
	],
	'total_questions': 3,
	'categories': {'1':'sports', '2', 'history'}
}


GET 'api/categories/{id}/questions'
- returns a list of questions based on a specific category id, a total number of questions, current category we are using to filter the results

- results are paginated in groups of 10 usin the 'page' argument that gets assigned to an integer value startin form 1

{
	'questions':[
	{'id': 6, 'question': 'how old are u?', 'answer': '18 years old', 'category': 2, 'difficulty': 1},
	{'id': 7, 'question': 'how are u?', 'answer': 'fine thanks', 'category': 2, 'difficulty': 1},
	{'id': 8, 'question': 'how old are brother?', 'answer': '15 years old', 'category': 2, 'difficulty': 1},
	],
	'total_questions': 3,
	'current_category': {'2', 'history'}
}

DELETE '/api/{id}/questions'
- delete a question based on its id which is based as an aregument returns the id of the deleted question, total number of remaining questions, and a list of questions object 

{
	'questions':[
	{'id': 6, 'question': 'how old are u?', 'answer': '18 years old', 'category': 2, 'difficulty': 1},
	{'id': 7, 'question': 'how are u?', 'answer': 'fine thanks', 'category': 2, 'difficulty': 1},
	{'id': 8, 'question': 'how old are brother?', 'answer': '15 years old', 'category': 2, 'difficulty': 1},
	],
	'total_questions': 3,
	'deleted': 5
}

POST '/api/questions'
- creates a new question using the submitted question, answer, difficulty_score, and the question category
-returns a list of question objects and a total number of questions

{
	'questions':[
	{'id': 6, 'question': 'how old are u?', 'answer': '18 years old', 'category': 2, 'difficulty': 1},
	{'id': 7, 'question': 'how are u?', 'answer': 'fine thanks', 'category': 2, 'difficulty': 1},
	{'id': 8, 'question': 'how old are brother?', 'answer': '15 years old', 'category': 2, 'difficulty': 1},
	],
	'total_questions': 3,
}

POST '/api/quizzes'
- this end point submits the answer and get the questions based on category to help playing the quizz game
-returns a random question out of a list of question objects fetched based on a category the user selects, and a number of total questions

{
	'question':
	{'id': 6, 'question': 'how old are u?', 'answer': '18 years old', 'category': 2, 'difficulty': 1},
	'total_questions': 3,
}

POST '/api/search'
- returns a list of questions objects based on a searchTerm that gets submitted, and a total number of questions

-the questions returned are paginated in groups of 10 using the 'page' argument that gets assigned to an integer value starts form 1

{
	'questions':[
	{'id': 6, 'question': 'how old are u?', 'answer': '18 years old', 'category': 2, 'difficulty': 1},
	{'id': 6, 'question': 'where are you form?', 'answer': 'canada', 'category': 2, 'difficulty': 1},

	]
	'total_questions': 3,
}
```
Error Handling
-errors are returned as JSON objects in the following format

{
	'success':False,
	'error': 404,
	'message': 'resource not found'
}

-the api will return three error types when a request fails
404: resource not found
405: method not allowed
422: unprocessable request


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```