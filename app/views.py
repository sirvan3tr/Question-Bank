from flask import render_template, flash, redirect, jsonify, request
import requests, json, ystockquote
from app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .forms import LoginForm
from .models import Module, Chapter, Question
from config import SQLALCHEMY_DATABASE_URI

# index view function suppressed for brevity
@app.route('/')
@app.route('/index')
def index():
    modules = Module.query.all()
    chapters = Chapter.query.all()
    newa = Chapter.query.join(Module, Chapter.module_id==Module.id).filter(Chapter.module_id==Module.id).add_columns(Module.name, Chapter.name.label("c_name"), Chapter.level).all()

    return render_template('index.html',
                           title='Home',
                           chapters=chapters,
                           currentid='',
                           newa=newa,
                           modules=modules)

@app.route('/getChapters', methods=['POST'])
def getChapters():
    chapters = Chapter.query.filter(Chapter.module_id==request.form['moduleId']).all()
    list = []
    for chapter in chapters:
        cobj = {'name': chapter.name,
            'level': chapter.level,
            'id': chapter.id,
            'descrioption':chapter.description}
        list.append(cobj)
    return jsonify(results=list)

@app.route('/getQuestions', methods=['POST'])
def getQuestions():
    questions = Question.query.filter(Question.chapter_id==request.form['chapterId']).all()
    list = []
    for question in questions:
        cobj = {'question': question.question,
            'solution': question.solution,
            'id': question.id}
        list.append(cobj)
    return jsonify(results=list)

@app.route('/newModule', methods=['POST'])
def newModule():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    # Create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    mod = Module(name=request.form['modulename'], description=request.form['moduledesc'])
    session.add(mod)
    session.commit()

@app.route('/newChapter', methods=['POST'])
def newChapter():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    # Create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    chapter = Chapter(module_id=request.form['moduleID'], name=request.form['chaptername'])
    session.add(chapter)
    session.commit()

@app.route('/newQuestion', methods=['POST'])
def newQuestion():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    # Create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    question = Question(chapter_id=request.form['chapterId'], question=request.form['questionname'])
    session.add(question)
    session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
