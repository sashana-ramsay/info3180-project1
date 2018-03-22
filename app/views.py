"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager,filefolder
import os,random,datetime
from flask import render_template, request, redirect, url_for, flash,jsonify, make_response
from forms import ProfileForm
from models import UserProfile
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user, current_user, login_required



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/profile', methods=["GET", "POST"])
def profile():
    form = ProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            
            # get form data
            firstname = form.firstname.data
            lastname = form.lastname.data
            gender = form.gender.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            file = form.upload.data
            filename = secure_filename(file.filename)
            profile_created_on = datetime.datetime.now()
            
            new_user = UserProfile(firstname = firstname, lastname = lastname, gender = gender, email = email, location = location, biography = biography, image = filename, date_joined = profile_created_on )
                
            db.session.add(new_user)
            db.session.commit()
            file.save(os.path.join(filefolder, filename))
            flash('Successfully added user', 'success')
            return redirect(url_for('profiles'))
            
    return render_template("profile.html", form = form)

def get_uploaded_images():
    images = os.listdir(filefolder)
    images_arr = []
    for j in images:
        a,b = j.split(".")
        if b == "jpg" or b == "png":
            images_arr.append(j)
    return images_arr
    
@app.route("/profiles")
def profiles():
    images = get_uploaded_images()
    profiles = UserProfile.query.all()
    return render_template('profiles.html', profiles = profiles, images = images)
        
        
@app.route("/profiles/<filename>")
def view_profile(filename):
    profile = UserProfile.query.filter_by(id = filename).first()
    images= get_uploaded_images()
    return render_template('view_profile.html', profile = profile, images = images)
            



    

    
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
