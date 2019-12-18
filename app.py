import sqlite3
from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/uliamarkova/PycharmProjects/hw5.1/questionnaire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'  # имя таблицы
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    hometown = db.Column(db.Text)
    residence = db.Column(db.Text)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Text)
    q2 = db.Column(db.Text)
    q3 = db.Column(db.Text)
    q4 = db.Column(db.Text)
    q5 = db.Column(db.Text)
    q6 = db.Column(db.Text)
    q7 = db.Column(db.Text)
    q8 = db.Column(db.Text)


@app.route('/')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'index.html',
        questions=questions
    )


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))

    name = request.args.get('name')
    surname = request.args.get('surname')
    gender = request.args.get('gender')
    age = request.args.get('age')
    hometown = request.args.get('hometown')
    residence = request.args.get('residence')

    questionnaire = Questionnaire(
        name=name,
        surname=surname,
        gender=gender,
        age=age,
        hometown=hometown,
        residence=residence
    )

    db.session.add(questionnaire)
    db.session.commit()

    db.session.refresh(questionnaire)

    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    q8 = request.args.get('q8')

    answer = Answers(
        id=questionnaire.id,
        q1=q1,
        q2=q2,
        q3=q3,
        q4=q4,
        q5=q5,
        q6=q6,
        q7=q7,
        q8=q8
    )
    db.session.add(answer)
    db.session.commit()

    return 'Самое большое в мире спасибо :-))'


if __name__ == '__main__':
    app.run(debug=True)
