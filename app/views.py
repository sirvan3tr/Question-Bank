from flask import render_template, flash, redirect, jsonify, request
import requests, json, ystockquote
from app import app
from .forms import LoginForm
from .models import Module, Chapter, Question

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
    db.execute('insert into entries (name, description) values (?, ?)',
                 [request.form['modulename'], request.form['moduledesc']])
    db.commit()

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