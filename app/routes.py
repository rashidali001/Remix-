from app import  app, db
from flask import render_template, flash, redirect, request,url_for
from app.forms import LoginForm, RegisterForm, AdminForm, Entry, ResetForm, ResetPasswordForm
from app.models import User, Employees
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.email import send_password_reset_email


# MAIN INDEX PAGE
@app.route("/")
@app.route("/index")
def index():
    logout_user()
    return render_template("index.html", title="Remix")


# LOGGING IN USER
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        if type(current_user._get_current_object()) == Employees:
            from app import login
            @login.user_loader
            def user_loader(id):
                print("employee")
                return Employees.query.get(int(id))
            login_user(current_user)
            return redirect(url_for('admin_dashboard'))
        return redirect("/user_dashboard")
    form = LoginForm()
    # VALIDATING USER ON LOGGING IN
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Email or Password")
            return redirect("/login") 
        # LOADING USER MODEL TO USER_LOADER
        from app import login
        @login.user_loader
        def user_loader(id):
            return User.query.get(int(id))        
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("user_dashboard")            
        return redirect(next_page)
        
    return render_template("login.html", title="login", form=form)


# REGISTERING USER
@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/user_dashboard")
    form = RegisterForm()
    # VALIDATING USER REGISTRATION FORM
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.fullname = form.fullname.data
        new_user.phone_no = form.phone_no.data
        new_user.set_password(form.password.data)
        new_user.points = 0
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/user_dashboard")

    return render_template("register.html", title="Register", form=form)

# USER DASHBOARD
@app.route("/user_dashboard")
@login_required
def user_dashboard():
    return render_template("user_dashboard.html", title="Remix Rewards")

# ADMIN DASHBOARD
@app.route("/admin_dashboard", methods=["POST", "GET"])
def admin_dashboard():
    if not current_user.is_authenticated:
        return redirect("/adminlogin")

    # NEW ENTRY FORM
    form = Entry()
    if form.validate_on_submit():
        user = User.query.filter_by(phone_no=form.phone_no.data).first()
        if user is None:
            flash("Failed!")
            flash("Phone number not found!")
            return redirect(url_for('admin_dashboard'))
        user.points += form.points.data
        db.session.add(user)
        db.session.commit()
        flash(f"SUCCESS!")
        flash(f"Username: {user.username}")
        flash(f"Current points : {user.points}")
        return redirect(url_for('admin_dashboard'))
    
    return render_template("admin.html", title="Remix Admin", form=form)

# LOGGIN IN ADMIN USER
@app.route("/adminlogin", methods=["POST", "GET"])
def admin():
    if current_user.is_authenticated:
        return redirect("/admin_dashboard")
    form = AdminForm()
    if form.validate_on_submit():
        employee = Employees.query.filter_by(id_no=form.id_no.data).first()
        if employee is None or not employee.check_password(form.password.data):
            flash("Invalid Phone No or Password")
            return redirect("/adminlogin") 
        # LOADING EMPLOYEE MODEL TO USER_LOADER
        from app import login
        @login.user_loader
        def user_loader(id):
            print("employee")
            return Employees.query.get(int(id))
        login_user(employee)
        return redirect("/admin_dashboard")    

    return render_template("adminlogin.html", title="Admin", form=form)

#RESET PAGE
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset.html',
                           title='Reset Password', form=form)



#RESETTING PASSWORD
@app.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect("/user_dashboard")
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect("/index")
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect("/login")
    return render_template('reset_password.html', form=form)

# LOGGING OUT
@app.route("/logout")
def logout():
    # IF CURRENT USER IS AN EMPLOYEE, BACK TO INDEX PAGE
    if type(current_user._get_current_object()) == Employees:
        logout_user()
        return redirect("/index")
    
    # ELSE GO TO LOGIN PAGE
    logout_user()
    return redirect("/login")
