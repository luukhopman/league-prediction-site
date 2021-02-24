import time
import pandas as pd
import numpy as np
import requests
from webapp.config import Config
from webapp import db
from webapp.models import Prediction

BASE_URL = 'https://api.football-data.org/v2/competitions/DED/'
API_KEY = Config.API_KEY
headers = {'X-Auth-Token': Config.API_KEY}


def get_team_list():
    res = requests.get(BASE_URL+'standings', headers=headers)
    res_json = res.json()
    if res_json.get('message'):
        wait = int(res_json['message'].split()[-2]) + 5
        time.sleep(wait)
    eredivisie_table = res_json['standings'][0]['table']

    eredivisie_teams = []
    for position in eredivisie_table:
        eredivisie_teams.append(position['team']['name'])
    return eredivisie_teams


def get_standings_json():
    res = requests.get(BASE_URL+'standings', headers=headers)
    res_json = res.json()
    if res_json.get('message'):
        wait = int(res_json['message'].split()[-2]) + 5
        time.sleep(wait)
        get_standings_json()

    return res_json['standings'][0]['table']


def get_standings():
    standings_json = get_standings_json()

    standings = []

    for team in standings_json:
        team_dict = {}
        team_dict['Position'] = team['position']
        team_dict['Team'] = team['team']['name']
        team_dict['W'] = team['playedGames']
        team_dict['P'] = team['points']
        team_dict['DV'] = team['goalsFor']
        team_dict['DT'] = team['goalsAgainst']

        standings.append(team_dict)

    return standings


def get_standings_df():
    standings = get_standings()
    df = pd.DataFrame(standings)
    df.set_index('Position', inplace=True)
    return df


def load_eredivisie_pred():
    data = db.session.query(Prediction).all()
    df = pd.DataFrame([(d.ed_1, d.ed_2, d.ed_3, d.ed_4,
                        d.ed_5, d.ed_6, d.ed_7, d.ed_8, d.ed_9,
                        d.ed_10, d.ed_11, d.ed_12, d.ed_13, d.ed_14,
                        d.ed_15, d.ed_16, d.ed_17, d.ed_18) for d in data],
                      index=[d.username for d in data]).T
    df['Position'] = df.index + 1
    df.set_index('Position', inplace=True)
    return df


def determine_points(prediction, standings, num_points):
    '''
    Returns the prediction's points
    '''
    full_points = np.where(standings['Team'] == prediction, num_points, 0)
    half_points = np.where((standings['Team'] == prediction.shift(-1)) |
                           (standings['Team'] == prediction.shift(1)),
                           (num_points/2), 0)

    points = sum(full_points) + sum(half_points)
    return points


def get_points_list(predictions, standings, num_points=10):
    '''
    Returns a list of points by prediction
    '''
    points = predictions.apply(determine_points, args=(standings, num_points,))
    return points.to_list()


def format_table(df):
    '''
    Function that adds classes to cells to format table
    - Underlines (semi-)correct predicitons
    - Changes the standings text color to dark blue
    '''
    for user in df.columns[5:]:
        df[user] = np.where(df[user] == df['Team'],
                            df[user].apply(
                                lambda x: f'<mark class="green-marker">{x}</mark>'),
                            df[user])
        df[user] = np.where((df[user] == df['Team'].shift(1)) |
                            (df[user] == df['Team'].shift(-1)),
                            df[user].apply(
                                lambda x: f'<mark class="yellow-marker">{x}</mark>'),
                            df[user])

    for col in ['Team', 'W', 'P', 'DV', 'DT']:
        if col == 'Team':
            df[col] = df[col].apply(
                lambda x: f'<span class="teams">{x}</span>')
        else:
            df[col] = df[col].apply(
                lambda x: f'<span class="dark-blue">{x}</span>')
        df = df.rename(columns={col: f'<span class="dark-blue">{col}</span>'})
    return df


def sort_table(df, point_list):
    '''
    Sort the predictions horizontally based on points
    '''
    cols = df.columns[5:]
    sorted_cols = [c for _, c in sorted(zip(point_list, cols), reverse=True)]
    return df[list(df.columns[:5]) + sorted_cols]


def get_eredivisie_table():
    # Combine standings and predictionts
    standings = get_standings_df()
    predictions = load_eredivisie_pred()

    if predictions.empty:
        return None

    df = standings.join(predictions)

    # Add points
    point_list = get_points_list(predictions, standings, 100)
    sorted_point_list = sorted(point_list, reverse=True)
    df = sort_table(df, point_list)
    points_row = [''] * len(standings.columns) + sorted_point_list
    df.loc[len(df)+1] = points_row

    # Add HTML formatting
    df = format_table(df)

    return df.to_html(classes=["table table-hover"], table_id="standings",
                      border=0, index=False, justify='center', escape=False)


if __name__ == '__main__':
    print(get_eredivisie_table())
