from app import db

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime)
    chapters = db.relationship('Chapter', backref='module', lazy='dynamic')

    def __repr__(self):
        return '<Module %r>' % (self.name)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(255))
    level = db.Column(db.Integer)
    questions = db.relationship('Question', backref='Chapter', lazy='dynamic')
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    def __repr__(self):
        return '<Chapter %r>' % (self.name)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    question = db.Column(db.String(255))
    solution = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    def __repr__(self):
        return '<Question %r>' % (self.question)
