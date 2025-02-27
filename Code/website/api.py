
from datetime import datetime
from flask import Blueprint,  jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt
from . import db
from .models import Chapter, Subject, Questions, Quiz, Scores
api = Blueprint('api', __name__)

# region Subject


@api.route('/subject', methods=['GET'])
def get_subjects():
    subList = []
    subjects = Subject.query.all()
    for subject in subjects:
        subList.append(subject.toJson())
    return jsonify({"data": subList}), 200


@api.route('/subject', methods=['POST'])
def add_subject():
    data = request.get_json()
    subject = Subject.query.filter_by(name=data['name']).first()
    if subject:
        return jsonify({"error": "Subject already exists"}), 400
    subject = Subject(name=data['name'], description=data['description'])
    db.session.add(subject)
    db.session.commit()
    return jsonify({"message": "Subject added successfully"}), 200

# endregion

# region Chapter


@api.route('/chapter', methods=['GET'])
def get_chapters():
    chapters = []
    chapterList = Chapter.query.all()
    for chapter in chapterList:
        chapters.append(chapter.toJson())
    return jsonify({"data": chapters}), 200


@api.route('/chapter', methods=['POST'])
def add_chapter():
    data = request.get_json()
    chapter = Chapter.query.filter_by(name=data['name']).first()
    if data['subject_id'] == None:
        return jsonify({'error': "Subject ID is required"}), 400
    if chapter:
        return jsonify({"error": "Chapter already exists"}), 400
    chapter = Chapter(name=data['name'], description=data['description'],
                      subject_id=data['subject_id'])
    db.session.add(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter added successfully"}), 200
# endregion

# region Question


@api.route('/question', methods=['GET'])
def get_questions():
    questionList = []
    questions = Questions.query.all()
    for question in questions:
        questionList.append(question.toJson())
    return jsonify({"data": questionList}), 200


@api.route("/question", methods=['POST'])
def add_question():
    data = request.get_json()
    question = Questions.query.filter_by(question=data['question']).first()
    if question:
        return jsonify({"error": "Question already exists"}), 400
    question = Questions(question=data['question'], options=json.dumps(data['options']),
                         answer=data['answer'], chapter_id=data['chapter_id'])
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": "Question added successfully"}), 200

# endregion

# region Quiz


@api.route("/quiz", methods=["GET"])
def get_quiz():
    quizList = []
    questions = Questions.query.all()
    for question in questions:
        quizList.append(question.toJson())
    return jsonify({"data": quizList}), 200


@api.route('/quiz', methods=['POST'])
def add_quiz():
    data = request.get_json()
    quiz = Quiz(chapter_id=data['chapter_id'],
                date=datetime(data['date']), time_duration=data['time_duration'])
    db.session.add(quiz)
# endregion

# region Scores


@api.route('/scores', methods=['GET'])
def get_scores():
    scoresList = []
    scores = Scores.query.all()
    for score in scores:
        scoresList.append(score.toJson())
    return jsonify({"data": scoresList}), 200


@api.route('/scores', methods=['POST'])
def add_score():
    data = request.get_json()

    # Answers object will be a dictionary with question_id as key and answer as value
    answers = data['answers']

    totalScore = 0
    quiz_id = data['quiz_id']
    chapter_id = Quiz.query.filter_by(id=quiz_id).first()['chapter_id']
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    questions = chapter.questions
    maxScore = len(questions)
    if questions == None:
        return jsonify({"error": "Something went wrong"}), 500

    for question in questions:
        if question.id in answers:
            if answers[question.id] == question.answer:
                totalScore += 1

    totalScore = (totalScore/maxScore)*100
    score = Scores(user_id=data['user_id'], quiz_id=data['quiz_id'],
                   attempt_timestamp=datetime.now(), score=totalScore, user_id=data['user_id'])
    db.session.add(score)
    db.session.commit()
    return jsonify({"message": "Quiz submitted successfully"}), 200

# endregion
