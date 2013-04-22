from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import json

from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

from login_mod import check_user_exists, gen_rnd_id, auth_user, new_user, activate_user, update_pass,set_inactive,update_pass
from email_mod import fire_pw_reset


global user

class User(UserMixin):
    def __init__(self, name, id,active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active
	
    def get_id(self):
	return self.id
	
class Anonymous(AnonymousUser):
    name = u"Anonymous"


app = Flask(__name__)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(id):
    user.get_id()

login_manager.setup_app(app)

#DEBUG = True

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

@app.route("/")
def hello():
    return render_template('index.html')
    #return "Hello World!"

@app.route("/activate")
def activate():
	if request.method == 'GET':
		oid = request.args['oid']
		activate_user(oid)
		return render_template('index.html',message='Great! Activate! Please sign in below!')

	return 'Activate here'	

@app.route("/register", methods=['POST','GET'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		name = request.form['name']
		email = request.form['email']
		if check_user_exists(username):
			return render_template('register.html')
		else:
			new_user(username, name, email, password)
		return render_template('index.html',message="Please check your email for activation information")
		#create_user(username,password,name,email)	

	if request.method == 'GET':
		return render_template('register.html')	

	return render_template('index.html')
	

@app.route("/login", methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	remember = request.form.get('remember_me')    
	if check_user_exists(username):
		if auth_user(username, password):	
			if remember:
				remeber == "yes"
			user_id = gen_rnd_id()
			global user 
			user = User(username,user_id)
			if login_user(user, remember=remember):
				#flash("Logged in!")
				#return "Logged in!"
				return render_template('userhome.html', username=username)
			else:
				return render_template('index.html',message="Sorry, but we couldn't log you in.")
        			#return "Couldn't log you in!"
		else:
			return render_template('index.html',message="Invlalid credentials, try again.")
     	else:
		return render_template('no_user.html')
        	#return "invalid username!"
			
	return render_template('index.html') 

@app.route("/forgot")
def forgot():
	if request.method == "GET":
		return render_template('password_reset.html')

	if request.method == "POST":
		email = request.form['email']
		username = request.form['username']
		oid = check_user_email(username,email)
		if oid == False:
			return render_template('index.html',message="You don't exist in the system.")
		else:
			set_inactive(username)
			fire_pw_reset(username, email, oid)
		return render_template('index.html',message="Check your email for a reset link")
	
	return render_template('index.html')

@app.route("/forgot/reset")
def forgot_reset():
	oid = request.args['oid']
	if request.method == "POST":
		#oid = request.args['oid']
		username = request.form['username']
		new_pass = request.form['password']
		new_pass_confirm = request.form['password_confirm']
		if new_pass == new_pass_confirm:
			update_pass(username,oid,password)
			return render_template('index.html',"Password has been reset! Log in here.")
		else:
			return render_template('pass_resetter.html',message="Your passwords don't match!")
	if request.method == "GET":
		return render_template('pass_resetter.html',oid=oid)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()

