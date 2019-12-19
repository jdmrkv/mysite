from collections import Counter

from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/uliamarkova/PycharmProjects/hw5.1/questionnaire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/statistics')
def stats():
    all_info = {}

    age_stats = db.session.query(
        func.avg(Questionnaire.age),
        func.min(Questionnaire.age),
        func.max(Questionnaire.age)
    ).one()

    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]

    all_info['total_count'] = Questionnaire.query.count()

    q1_answers = db.session.query(Answers.q1).all()
    q2_answers = db.session.query(Answers.q2).all()
    q3_answers = db.session.query(Answers.q3).all()
    q4_answers = db.session.query(Answers.q4).all()
    q5_answers = db.session.query(Answers.q5).all()
    q6_answers = db.session.query(Answers.q6).all()
    q7_answers = db.session.query(Answers.q7).all()
    q8_answers = db.session.query(Answers.q8).all()

    if Counter(q1_answers).most_common(1)[0][0][0] == 'tv-rog':
        all_info['q1_mode'] = 'твОрог'
        all_info['q1_mode_num'] = Counter(q1_answers).most_common(1)[0][1]
        all_info['q1_not_mode'] = 'творОг'
        all_info['q1_not_mode_num'] = all_info['total_count'] - all_info['q1_mode_num']
    else:
        all_info['q1_mode'] = 'творОг'
        all_info['q1_mode_num'] = Counter(q1_answers).most_common(1)[0][1]
        all_info['q1_not_mode'] = 'твОрог'
        all_info['q1_not_mode_num'] = all_info['total_count'] - all_info['q1_mode_num']
    if Counter(q2_answers).most_common(1)[0][0][0] == 'odnovr-menno':
        all_info['q2_mode'] = 'одноврЕменно'
        all_info['q2_mode_num'] = Counter(q2_answers).most_common(1)[0][1]
        all_info['q2_not_mode'] = 'одновремЕнно'
        all_info['q2_not_mode_num'] = all_info['total_count'] - all_info['q2_mode_num']
    else:
        all_info['q2_mode'] = 'одновремЕнно'
        all_info['q2_mode_num'] = Counter(q2_answers).most_common(1)[0][1]
        all_info['q2_not_mode'] = 'одноврЕменно'
        all_info['q2_not_mode_num'] = all_info['total_count'] - all_info['q2_mode_num']
    if Counter(q3_answers).most_common(1)[0][0][0] == 'n-wton':
        all_info['q3_mode'] = 'НьЮтон'
        all_info['q3_mode_num'] = Counter(q3_answers).most_common(1)[0][1]
        all_info['q3_not_mode'] = 'НьютОн'
        all_info['q3_not_mode_num'] = all_info['total_count'] - all_info['q3_mode_num']
    else:
        all_info['q3_mode'] = 'НьютОн'
        all_info['q3_mode_num'] = Counter(q3_answers).most_common(1)[0][1]
        all_info['q3_not_mode'] = 'НьЮтон'
        all_info['q3_not_mode_num'] = all_info['total_count'] - all_info['q3_mode_num']
    if Counter(q4_answers).most_common(1)[0][0][0] == '-goditsy':
        all_info['q4_mode'] = 'Ягодицы'
        all_info['q4_mode_num'] = Counter(q4_answers).most_common(1)[0][1]
        all_info['q4_not_mode'] = 'ягодИцы'
        all_info['q4_not_mode_num'] = all_info['total_count'] - all_info['q4_mode_num']
    else:
        all_info['q4_mode'] = 'ягодИцы'
        all_info['q4_mode_num'] = Counter(q4_answers).most_common(1)[0][1]
        all_info['q4_not_mode'] = 'Ягодицы'
        all_info['q4_not_mode_num'] = all_info['total_count'] - all_info['q4_mode_num']
    if Counter(q5_answers).most_common(1)[0][0][0] == 'k-shitsa':
        all_info['q5_mode'] = 'кАшица'
        all_info['q5_mode_num'] = Counter(q5_answers).most_common(1)[0][1]
        all_info['q5_not_mode'] = 'кашИца'
        all_info['q5_not_mode_num'] = all_info['total_count'] - all_info['q5_mode_num']
    else:
        all_info['q5_mode'] = 'кашИца'
        all_info['q5_mode_num'] = Counter(q5_answers).most_common(1)[0][1]
        all_info['q5_not_mode'] = 'кАшица'
        all_info['q5_not_mode_num'] = all_info['total_count'] - all_info['q5_mode_num']
    if Counter(q6_answers).most_common(1)[0][0][0] == 'metall-rgiya':
        all_info['q6_mode'] = 'металлУргия'
        all_info['q6_mode_num'] = Counter(q6_answers).most_common(1)[0][1]
        all_info['q6_not_mode'] = 'металлургИя'
        all_info['q6_not_mode_num'] = all_info['total_count'] - all_info['q6_mode_num']
    else:
        all_info['q6_mode'] = 'металлургИя'
        all_info['q6_mode_num'] = Counter(q6_answers).most_common(1)[0][1]
        all_info['q6_not_mode'] = 'металлУргия'
        all_info['q6_not_mode_num'] = all_info['total_count'] - all_info['q6_mode_num']
    if Counter(q7_answers).most_common(1)[0][0][0] == 't-fteli':
        all_info['q7_mode'] = 'тЕфтели'
        all_info['q7_mode_num'] = Counter(q7_answers).most_common(1)[0][1]
        all_info['q7_not_mode'] = 'тефтЕли'
        all_info['q7_not_mode_num'] = all_info['total_count'] - all_info['q7_mode_num']
    else:
        all_info['q7_mode'] = 'тефтЕли'
        all_info['q7_mode_num'] = Counter(q7_answers).most_common(1)[0][1]
        all_info['q7_not_mode'] = 'тЕфтели'
        all_info['q7_not_mode_num'] = all_info['total_count'] - all_info['q7_mode_num']
    if Counter(q8_answers).most_common(1)[0][0][0] == 'k-mbala':
        all_info['q8_mode'] = 'кАмбала'
        all_info['q8_mode_num'] = Counter(q8_answers).most_common(1)[0][1]
        all_info['q8_not_mode'] = 'камбалА'
        all_info['q8_not_mode_num'] = all_info['total_count'] - all_info['q8_mode_num']
    else:
        all_info['q8_mode'] = 'камбалА'
        all_info['q8_mode_num'] = Counter(q8_answers).most_common(1)[0][1]
        all_info['q8_not_mode'] = 'кАмбала'
        all_info['q8_not_mode_num'] = all_info['total_count'] - all_info['q8_mode_num']


    return render_template('statistics.html', all_info=all_info)

if __name__ == '__main__':
    app.run(debug=True)
