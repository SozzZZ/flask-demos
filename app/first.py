from flask import Flask,app,request,render_template,session,redirect,url_for,flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField , SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Shell
from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.mail import Mail
from flask.ext.mail import Message
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '17826839707@163.com'
app.config['MAIL_PASSWORD'] = 'Zhujun32032'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <17826839707@163.com>'
app.config['FLASKY_ADMIN'] = '17826839707@163.com'

mail = Mail(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

class NameForm(Form):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User',backref='role',lazy='dynamic')
    def __repr__(self):
        return '<Role %s>' %self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %s>' %self.username

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr



@app.route('/',methods=['GET','POST'])
def index():
    form  = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None :
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            flash('Looks like you have changed your name!')
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',current_time= datetime.utcnow(),form=form, name=session.get('name'),known = session.get('known',False))


@app.route('/request')
def reque():
    user_agent = request.headers.get('User-Agent')
    return '<p>%s</p>'%user_agent,400

@app.route('/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.before_first_request
def start():
    print('start------------------------------------------')

@app.before_request
def req():
    print('request==========================================')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404



def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()


