from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import current_user, login_required
from webapp import db
from webapp.main.forms import EredivisieForm
from webapp.models import Prediction
from webapp.main.utils import get_team_list, get_eredivisie_table
from webapp.config import Config

main = Blueprint('main', __name__)


@main.route('/eredivisie', methods=['GET', 'POST'])
@login_required
def eredivisie():
    # Load current user's prediction
    found_user = Prediction.query.filter_by(user_id=current_user.id).first()

    # Create form with appropriate order
    eredivisie_list = get_team_list()
    teams = get_teams_order(eredivisie_list, found_user)
    form = EredivisieForm(request.form,
                          ed_1=teams[1], ed_2=teams[2], ed_3=teams[3],
                          ed_4=teams[4], ed_5=teams[5], ed_6=teams[6],
                          ed_7=teams[7], ed_8=teams[8], ed_9=teams[9],
                          ed_10=teams[10], ed_11=teams[11], ed_12=teams[12],
                          ed_13=teams[13], ed_14=teams[14], ed_15=teams[15],
                          ed_16=teams[16], ed_17=teams[17], ed_18=teams[18])

    if form.validate_on_submit():
        if found_user:
            for i in range(1, 19):
                pred_i = eval(f'form.ed_{i}.data')
                exec(f'found_user.ed_{i}="{pred_i}"')
            db.session.commit()
        else:
            prediction = [v for v in form.data.values()]
            entry = Prediction(current_user.id,
                               current_user.username,
                               *prediction[0:18])
            db.session.add(entry)
            db.session.commit()
        return redirect(url_for('main.dashboard'))

    return render_template('eredivisie.html', active_season=False,
                           form=form, title='Voorspelling')


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not Config.ACTIVE_SEASON:
        flash("Je kunt op dit moment alleen je eigen voorspelling bekijken", 'primary')
        return redirect(url_for('main.prediction', user_id=current_user.id))
    df = get_eredivisie_table()
    if not df:
        flash("Nog geen voorspellingen", 'warning')
        return redirect(url_for('users.index'))
    return render_template('dashboard.html', table=df, title='Dashboard')


@main.route("/prediction/<int:user_id>", methods=['GET', 'POST'])
@login_required
def view_prediciton(user_id):
    if not user_id == current_user.id and not current_user.is_admin:
        flash('Je bent geen admin.', 'danger')
        return redirect('/')
    prediction = Prediction.query.filter_by(user_id=user_id).first()
    return render_template('prediction.html', prediction=prediction, title='Prediction')


def get_teams_order(eredivisie_list, found_user):
    '''
    Returns the team order of the user's saved prediction.
    If there is no saved prediction, the current standing error is returned.
    '''
    team_order = {i: c for i, c in enumerate(eredivisie_list, start=1)}
    if found_user:
        for i in range(1, 19):
            team_order[i] = eval(f'found_user.ed_{i}')
    return team_order
