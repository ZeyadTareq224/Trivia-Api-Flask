import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources = {'*/api/*':{'origins':'*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      response.headers.add('Access-Control-Allow-Credentials', 'true')
      response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.order_by(Category.id).all()
      formated_categories = [category.format() for category in categories]
      formated_formated_categories = {item['id']:item['type'] for item in formated_categories}
      if len(formated_categories) == 0:
        abort(404
        )
      return jsonify({
        'categories': formated_formated_categories
          })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions')
  def get_questions():
      
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      if len(current_questions) == 0:
        abort(404)
      categories = Category.query.order_by(Category.id).all()
      formated_categories = [category.format() for category in categories]
      formated_formated_categories = {item['id']:item['type'] for item in formated_categories}
      print(current_questions)
      return jsonify({
          'questions': current_questions,
          'total_questions':len(Question.query.all()),
          'categories': formated_formated_categories
      })
          
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:

      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      return jsonify({
        'deleted': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
        })
    except:
      return abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = int(body.get('difficulty', None))
    category = int(body.get('category', None))

    try:
      question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/search', methods=['POST'])
  def search():
      search_term = request.get_json().get('searchTerm')
      try:

        selection = Question.query.filter(Question.question.ilike('%'+ search_term +'%')).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
          abort(404)
        return jsonify({
            'questions': current_questions,
            'total_questions':len(Question.query.all()),  
          })
      except: 
        abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:id>/questions', methods=['GET'])
  def get_question_by_id(id):
    category = Category.query.get(id)
    questions = Question.query.filter(Question.category==id).all()
    current_questions = [q.format() for q in questions]
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      "questions": current_questions,
      "total_questions": len(Question.query.all()),
      "current_category": category.format()
    })  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def quiz():
    try:

      body = request.get_json()
      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category')
      if int(quiz_category['id']) == 0:
        questions = Question.query.all()
      else:  
        questions = Question.query.filter(Question.category == quiz_category['id']).all()
      formated_questions = [q.format() for q in questions]
      if len(questions) == 0:
        abort(404)
      question = random.choice(formated_questions)
      while 1:
        if int(question['id']) in previous_questions:
          question = random.choice(formated_questions)
        else:
          break  
        
      return jsonify({
          'question':question,
          'total_questions':len(Question.query.all())
        })
    except:
      return abort(422)    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':'unprocessable'
    }), 422


  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'error':405,
      'message':'method not allowed'
    }), 405

  return app
