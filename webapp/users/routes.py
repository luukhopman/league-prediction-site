from flask import render_template, request, redirect, url_for, flash, Markup, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from webapp import db
from webapp.users.forms import RegisterForm, LoginForm
from webapp.models import Prediction, User

users = Blueprint('users', __name__)


@users.route('/', methods=['POST', 'GET'])
@users.route('/home', methods=['POST', 'GET'])
@users.route('/index', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html')

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        user = User(username)
        db.session.add(user)
        db.session.commit()

        found_user = User.query.filter_by(username=username).first()
        login_user(found_user)
        flash(Markup(
            f"Hi <strong>{username}</strong>. Je PIN is <strong>{found_user.pin}</strong>, deze kun je gebruiken om je voorspelling later aan te passen."), 'success')
        return redirect(url_for('main.eredivisie'))
    return render_template('index.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("Je bent al ingelogd.", 'success')
        return redirect(url_for('users.index'))

    form = LoginForm()
    if form.validate_on_submit():
        found_user = User.query.filter_by(username=form.username.data).first()

        if found_user and found_user.pin == form.pin.data:
            login_user(found_user)
            flash(Markup(
                f'Ingelogd als <strong>{form.username.data}</strong>'), 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.index'))
        else:
            flash("Vul de juiste gegevens in.", 'danger')
    return render_template('login.html', form=form)


@users.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html', users=User.query.all())
    else:
        flash("Je bent geen admin", 'danger')
        return redirect(url_for('users.index'))


@login_required
@users.route('/delete/<int:id>')
def delete(id):
    if not current_user.is_admin:
        flash('Je bent geen admin.', 'danger')
        return redirect('/')

    user_to_delete = User.query.get_or_404(id)
    if user_to_delete.username == 'admin':
        flash('')
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f"{user_to_delete.username} verwijderd.", 'danger')
    if user_to_delete.username == current_user.username:
        return redirect('users.logout')
    return render_template('admin.html', users=User.query.all())


@login_required
@users.route('/toggle-admin/<int:id>')
def toggle_admin(id):
    if not current_user.is_admin:
        flash('Je bent geen admin.', 'danger')
        return redirect('/')

    user_to_admin = User.query.get_or_404(id)
    if user_to_admin.username != 'admin':
        if user_to_admin.is_admin:
            User.query.filter_by(username=user_to_admin.username).update(
                dict(is_admin=False))
            flash(f"{user_to_admin.username} is geen admin meer", 'danger')
        else:
            User.query.filter_by(username=user_to_admin.username).update(
                dict(is_admin=True))
            flash(f"{user_to_admin.username} is nu admin", 'success')
    db.session.commit()
    return render_template('admin.html', users=User.query.all())


@users.route('/delete-prediction/<int:id>')
def delete_prediciton(id):
    if not current_user.is_admin:
        flash('Je bent geen admin.', 'danger')
        return redirect('/')

    user_to_admin = User.query.get_or_404(id)
    Prediction.query.filter_by(user_id=user_to_admin.id).delete()
    flash(f"Voorspelling van {user_to_admin.username} verwijderd", 'danger')
    db.session.commit()
    return render_template('admin.html', users=User.query.all())


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.index'))
