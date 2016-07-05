# project/main/views.py


#################
#### imports ####
#################
from flask.ext.login import login_user, logout_user, \
    login_required, current_user
from flask import render_template, Blueprint, request
from flask.ext.login import login_required

from project.models import User
################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################http://stackoverflow.com/questions/23744171/flask-get-all-products-from-table-and-iterate-over-them

@main_blueprint.route('/')
@login_required
def home():
    return render_template('main/index.html')

@main_blueprint.route('/show')
def show():
  users = User.query.all()
  return render_template("main/alluser.html", title="users", users=users)

@main_blueprint.route('/user/<id>')
def singleuser(id):
  singleuser = User.query.filter_by(id=id).first_or_404()
  return render_template('main/alluser.html', singleuser=singleuser)


from werkzeug.security import generate_password_hash, check_password_hash
from project.models import Posts, Tracking, Points
from flask_wtf import Form
from wtforms import validators
from wtforms import TextField, StringField
from wtforms.validators import required
from project import app, db
from flask import redirect, url_for, request, flash
from hashids import Hashids
hashids = Hashids()
db.create_all()
@main_blueprint.route('/tracking')
@login_required
def tracking():
  tracking = Tracking.query.all()
  return render_template('main/alluser.html', tracking = tracking)

@main_blueprint.route('/points')
@login_required
def points():
  points = Points.query.order_by(Points.earned_points.desc()).all()
  return render_template('main/alluser.html', points = points)



@main_blueprint.route('/showposts', methods=['GET'])
@login_required
def showposts():
  if current_user.admin:
    deletepostbyid = request.args.get('deletepostbyid')
    if deletepostbyid > 0:
      Posts.query.filter(Posts.id == deletepostbyid).delete()
      db.session.commit()
  showearning = request.args.get('showearning')
  if showearning > 0:
    posts = Posts.query.join(Points, Posts.id == Points.post_ID) \
    .add_columns(Points.earned_points, Posts.post_title, Posts.id, Posts.post_link, Posts.post_image, Posts.post_code, Posts.post_description).filter_by(user_ID = current_user.id).order_by(Points.earned_points.desc()).all()
    return render_template("main/alluser.html", title="all posts", posts = posts, ref = hashids.encode(current_user.id))

  posts = Posts.query.order_by(Posts.id.desc()).all()
  return render_template("main/alluser.html", title="all posts", posts = posts, ref = hashids.encode(current_user.id))
  # posts = Posts.query.join(Posts.id = Points.post_ID).order_by(desc(Points.earned_points)).all()
  # posts = Posts.query.all()
  # points = Points.query.all()


@main_blueprint.route('/showpost/<code>', methods=['GET'])
@login_required
def showpost(code):
  singlepost = Posts.query.filter_by(post_code=code).first_or_404()
  user_code = request.args.get('ref')
  if(user_code):
    tup = hashids.decode(user_code)
    user_code = float(tup[0])

    if( Tracking.query.filter_by(post_ID = singlepost.id).filter_by( ip = request.remote_addr).filter_by(user_ID = user_code).scalar() is None):
      newtrack = Tracking(singlepost.id, user_code , request.remote_addr)
      db.session.add(newtrack)
      db.session.commit()
      if( Points.query.filter_by(post_ID = singlepost.id).filter_by(user_ID = user_code).scalar() is None):
        newpoint = Points(user_code, singlepost.id, 1)
        db.session.add(newpoint)
        db.session.commit()

      else:
        element = Points.query.filter_by(post_ID = singlepost.id).filter_by(user_ID = user_code).first()
        element.earned_points += 1
        db.session.commit()
        flash (element.earned_points, 'warning')

    flash(user_code, 'success')
  return render_template("main/single.html", title="post", singlepost = singlepost)




# adding post to database

class addpostvalidator(Form):
  post_title = TextField('post_title',validators=[required()])
  post_link = TextField('post_link',validators=[required()])
  post_image = TextField('post_image',validators=[])
  post_description = TextField('post_description',validators=[])

#http://stackoverflow.com/questions/20837209/flask-wtform-save-form-to-db
@main_blueprint.route('/addpost/',methods=['GET','POST'])
@login_required
def addpost():
  if not current_user.admin:
        return redirect('/')
  form = addpostvalidator()
  if form.validate_on_submit():
    
    new_post = Posts(
      form.post_title.data,
      form.post_link.data,
      form.post_image.data,
      form.post_description.data,
      generate_password_hash(form.post_title.data)
      )
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')

  return render_template('main/addpost.html', form=form)