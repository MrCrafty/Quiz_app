
from datetime import datetime
from flask import Blueprint,  jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt
from . import db
from .models import Chapter, Subject, Questions, Quiz, Scores
api = Blueprint('api', __name__)

# region Subject


@api.route('/subjects', methods=['GET'])
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


@api.route('/subject/<int:id>', methods=['GET'])
def get_subject(id):
    subject = Subject.query.filter_by(id=id).first()
    if subject == None:
        return jsonify({"error": "Subject not found"}), 404
    return jsonify({"data": subject.toJson()}), 200


@api.route('/subject/<int:id>', methods=['DELETE'])
def delete_subject(id):
    subject = Subject.query.filter_by(id=id).first()
    if subject == None:
        return jsonify({"error": "Subject not found"}), 404
    db.session.delete(subject)
    db.session.commit()
    return jsonify({"message": "Subject deleted successfully"}), 200


@api.route("/subject/<int:id>", methods=['PUT'])
def update_subject(id):
    data = request.get_json()
    subject = Subject.query.filter_by(id=id).first()
    if subject == None:
        return jsonify({"error": "Subject not found"}), 404
    subject.name = data['name']
    subject.description = data['description']
    db.session.commit()
    return jsonify({"message": "Subject updated successfully"}), 200
# endregion

# region Chapter


@api.route('/chapters', methods=['GET'])
def get_chapters():
    chapters = []
    chapterList = Chapter.query.all()
    for chapter in chapterList:
        chapters.append(chapter.toJson())
    return jsonify({"data": chapters}), 200


@api.route('/chapter', methods=['POST'])
def add_chapter():
    data = request.get_json()
    chapter = Chapter.query.filter_by(
        name=data['name'], subject_id=data['subject_id']).first()
    if data['subject_id'] == None:
        return jsonify({'error': "Subject ID is required"}), 400
    if chapter:
        return jsonify({"error": "Chapter already exists"}), 400
    chapter = Chapter(name=data['name'], description=data['description'],
                      subject_id=data['subject_id'])
    db.session.add(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter added successfully"}), 200


@api.route('/chapter/<int:id>', methods=['GET'])
def get_chapter(id):
    chapter = Chapter.query.filter_by(id=id).first()
    if chapter == None:
        return jsonify({"error": "Chapter not found"}), 404
    return jsonify({"data": chapter.toJson()}), 200


@api.route('/chapter/<int:id>', methods=['DELETE'])
def delete_chapter(id):
    chapter = Chapter.query.filter_by(id=id).first()
    if chapter == None:
        return jsonify({"error": "Chapter not found"}), 404
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter deleted successfully"}), 200


@api.route("/chapter/<int:id>", methods=['PUT'])
def update_chapter(id):
    data = request.get_json()
    chapter = Chapter.query.filter_by(id=id).first()
    if chapter == None:
        return jsonify({"error": "Chapter not found"}), 404
    chapter.name = data['name']
    chapter.description = data['description']
    db.session.commit()
    return jsonify({"message": "Chapter updated successfully"}), 200
# endregion

# region Question


@api.route('/questions', methods=['GET'])
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


@api.route('/question/<int:id>', methods=['GET'])
def get_question(id):
    question = Questions.query.filter_by(id=id).first()
    if question == None:
        return jsonify({"error": "Question not found"}), 404
    return jsonify({"data": question.toJson()}), 200


@api.route('/question/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Questions.query.filter_by(id=id).first()
    if question == None:
        return jsonify({"error": "Question not found"}), 404
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"}), 200


@api.route('/question/<int:id>', methods=['PUT'])
def update_question(id):
    data = request.get_json()
    question = Questions.query.filter_by(id=id).first()
    if question == None:
        return jsonify({"error": "Question not found"}), 404
    question.question = data['question']
    question.options = json.dumps(data['options'])
    question.answer = data['answer']
    db.session.commit()
    return jsonify({"message": "Question updated successfully"}), 200
# endregion

# region Quiz


@api.route("/quizzes", methods=["GET"])
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


@api.route('/quiz/<int:id>', methods=['GET'])
def get_quizzes(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if quiz == None:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify({"data": quiz.toJson()}), 200


@api.route('/quiz/<int:id>', methods=['DELETE'])
def delete_quiz():
    data = request.get_json()
    quiz = Quiz.query.filter_by(id=data['id']).first()
    if quiz == None:
        return jsonify({"error": "Quiz not found"}), 404
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted successfully"}), 200


@api.route("/quiz/<int:id>", methods=['PUT'])
def update_quiz(id):
    data = request.get_json()
    quiz = Quiz.query.filter_by(id=id).first()
    if quiz == None:
        return jsonify({"error": "Quiz not found"}), 404
    quiz.chapter_id = data['chapter_id']
    quiz.date = datetime(data['date'])
    quiz.time_duration = data['time_duration']
    db.session.commit()
    return jsonify({"message": "Quiz updated successfully"}), 200
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
                   attempt_timestamp=datetime.now(), score=totalScore)
    db.session.add(score)
    db.session.commit()
    return jsonify({"message": "Quiz submitted successfully"}), 200


@api.route('/scores/<int:id>', methods=['GET'])
def get_score(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if quiz == None:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify({"data": quiz.toJson()}), 200


@api.route('/scores', methods=['DELETE'])
def delete_score():
    data = request.get_json()
    score = Scores.query.filter_by(id=data['id']).first()
    if score == None:
        return jsonify({"error": "Score not found"}), 404
    db.session.delete(score)
    db.session.commit()
    return jsonify({"message": "Score deleted successfully"}), 200


@api.route('/scores/<int:id>', methods=['PUT'])
def update_score(id):
    data = request.get_json()
    score = Scores.query.filter_by(id=id).first()
    if score == None:
        return jsonify({"error": "Score not found"}), 404
    score.user_id = data['user_id']
    score.quiz_id = data['quiz_id']
    score.attempt_timestamp = datetime(data['attempt_timestamp'])
    score.score = data['score']
    db.session.commit()
    return jsonify({"message": "Score updated successfully"}), 200
# endregion
