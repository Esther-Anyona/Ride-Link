from crypt import methods
from . import main
from flask import render_template,session, request,redirect,url_for,abort, flash
from ..models import User,Review, Rider
from .. import db, photos
from .forms import UpdateUserProfile, UserForm, ReviewForm
from flask_login import login_required, current_user
from app.main import forms


@main.route('/')
def index():
  return render_template('home.html')

@main.route('/user', methods=['POST','GET'])
def user():
    form=UserForm()

    if form.validate_on_submit():
        location = form.pick_up.data
        pickup = location.lower()
        return redirect(url_for('main.drivers', location = pickup))

    return render_template('usr.html', form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile_users.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateUserProfile()
    if form.validate_on_submit():
        user.location = form.location.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update_user.html',form =form)

@main.route('/user/review', methods = ['GET','POST'])
@login_required
def review():
    review_form = ReviewForm()
    if review_form.validate_on_submit():
        driver_id = review_form.driver_id.data
        rider_id = Rider.query.filter_by(id = driver_id).first()
        review = review_form.review.data
        new_review = Review(review=review, rider=rider_id, user_id=current_user.id)
        new_review.save_review()
        return redirect(url_for('main.user'))

    return render_template('review.html', review_form=review_form) 

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/drivers/<string:location>')
def drivers(location):
    drivers = Rider.query.filter_by(location = location).all()

    return render_template('drivers.html', drivers = drivers)
   
