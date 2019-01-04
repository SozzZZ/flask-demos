from flask import Flask,app,request,render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField , SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form  = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html',current_time= datetime.utcnow(),form=form, name=name)

@app.route('/request')
def reque():
    user_agent = request.headers.get('User-Agent')
    return '<p>%s</p>'%user_agent,400

@app.route('/<name>')
def user(name):
    return render_template('user.html',name=name)

#@before_first_request
def start():
    print('start------------------------------------------')

#@before_request
def req():
    print('request==========================================')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404











if __name__ == '__main__':
    manager.run()


