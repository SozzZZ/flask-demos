from datetime import datetime
from flask import render_template, session, redirect, url_for,flash, current_app
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

@main.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html',current_time=datetime.utcnow())


#    form  = NameForm()
  #  if form.validate_on_submit():
 #       user = User.query.filter_by(username=form.name.data).first()
   #     if user is None :
     #       user = User(username=form.name.data)
    #        db.session.add(user)
      #      session['known'] = False
       #     flash('Looks like you have changed your name!')
        #    if current_app.config['FLASKY_ADMIN']:
         #       send_email(current_app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
       # else:
        #    session['known'] = True
       # session['name'] = form.name.data
        #form.name.data = ''
        #return redirect(url_for('.index'))
   # return render_template('index.html',current_time= datetime.utcnow(),form=form, name=session.get('name'),known = session.get('known',False))
