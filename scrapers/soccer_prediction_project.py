import sqlite3
from sqlite3 import Error
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, ShuffleSplit
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')
#warnings.filterwarnings('default')

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None
    
def read_data(table_name, conn):
    return pd.read_sql("SELECT * FROM " + table_name, conn)    

def add_player_stats(abt_table, player_data, player_stats_data):
    player_data.is_copy = False
    player_stats_data.is_copy = False
    player_data = player_data[['player_api_id', 'player_name', 'birthday']]
    td = pd.datetime.now().date() - pd.to_datetime(player_data['birthday'], format='%Y-%m-%d')
    player_data['player_age'] = td.dt.days / 365
    player_data.drop('birthday', axis=1, inplace = True)
    player_stats_data = player_stats_data[['player_api_id', 'overall_rating']]
    player_stats_data = player_stats_data.drop_duplicates(['player_api_id'], keep='last')
    
    mean_player_rating = player_stats_data['overall_rating'].mean()
    
    for index in range(1,12):
        #Get home team player names and ratings
        abt_table = pd.merge(abt_table, player_data, left_on='home_player_' + str(index), right_on='player_api_id', how='left')  
        abt_table.drop('player_api_id', axis=1, inplace = True)
        abt_table = abt_table = abt_table.rename(columns = {'player_name':'home_player_' + str(index) + '_name'})
        abt_table = abt_table = abt_table.rename(columns = {'player_age':'home_player_' + str(index) + '_age'})
        abt_table = pd.merge(abt_table, player_stats_data, left_on='home_player_' + str(index), right_on='player_api_id', how='left')  
        abt_table.drop('player_api_id', axis=1, inplace = True)
        abt_table['overall_rating'] = abt_table['overall_rating'].fillna(mean_player_rating)
        abt_table = abt_table.rename(columns = {'overall_rating':'home_player_' + str(index) + '_rating'})
        
        #Get away team player names and ratings
        abt_table = pd.merge(abt_table, player_data, left_on='away_player_' + str(index), right_on='player_api_id', how='left')  
        abt_table.drop('player_api_id', axis=1, inplace = True)
        abt_table = abt_table.rename(columns = {'player_name':'away_player_' + str(index) + '_name'})
        abt_table = abt_table.rename(columns = {'player_age':'away_player_' + str(index) + '_age'})
        abt_table = pd.merge(abt_table, player_stats_data, left_on='away_player_' + str(index), right_on='player_api_id', how='left')  
        abt_table.drop('player_api_id', axis=1, inplace = True)
        abt_table['overall_rating'] = abt_table['overall_rating'].fillna(mean_player_rating)
        abt_table = abt_table.rename(columns = {'overall_rating':'away_player_' + str(index) + '_rating'})
        
    abt_table['avg_home_player_rating'] = ( abt_table['home_player_1_rating'] + abt_table['home_player_2_rating'] + abt_table['home_player_3_rating'] + abt_table['home_player_4_rating'] + abt_table['home_player_5_rating'] + abt_table['home_player_6_rating'] + abt_table['home_player_7_rating'] + abt_table['home_player_8_rating'] + abt_table['home_player_9_rating'] + abt_table['home_player_10_rating'] + abt_table['home_player_11_rating'] ) / 11
    abt_table['avg_away_player_rating'] = ( abt_table['away_player_1_rating'] + abt_table['away_player_2_rating'] + abt_table['away_player_3_rating'] + abt_table['away_player_4_rating'] + abt_table['away_player_5_rating'] + abt_table['away_player_6_rating'] + abt_table['away_player_7_rating'] + abt_table['away_player_8_rating'] + abt_table['away_player_9_rating'] + abt_table['away_player_10_rating'] + abt_table['away_player_11_rating'] ) / 11
    abt_table['avg_home_player_age'] = ( abt_table['home_player_1_age'] + abt_table['home_player_2_age'] + abt_table['home_player_3_age'] + abt_table['home_player_4_age'] + abt_table['home_player_5_age'] + abt_table['home_player_6_age'] + abt_table['home_player_7_age'] + abt_table['home_player_8_age'] + abt_table['home_player_9_age'] + abt_table['home_player_10_age'] + abt_table['home_player_11_age'] ) / 11
    abt_table['avg_away_player_age'] = ( abt_table['away_player_1_age'] + abt_table['away_player_2_age'] + abt_table['away_player_3_age'] + abt_table['away_player_4_age'] + abt_table['away_player_5_age'] + abt_table['away_player_6_age'] + abt_table['away_player_7_age'] + abt_table['away_player_8_age'] + abt_table['away_player_9_age'] + abt_table['away_player_10_age'] + abt_table['away_player_11_age'] ) / 11
    
    #drop unnecessary columns
    for index in range(1,12):
        abt_table.drop(['home_player_' + str(index), 'home_player_' + str(index) + '_rating', 'home_player_' + str(index) + '_age', 'home_player_' + str(index) + '_name'], axis=1, inplace=True)
        abt_table.drop(['away_player_' + str(index), 'away_player_' + str(index) + '_rating', 'away_player_' + str(index) + '_age', 'away_player_' + str(index) + '_name'], axis=1, inplace=True)
    return abt_table

def add_team_stats(abt_table, team_data, team_stats_data):
    team_stats_data = team_stats_data.drop_duplicates(['team_api_id'], keep='last')
#    abt_table = pd.merge(abt_table, team_stats_data, left_on='home_team_api_id', right_on='team_api_id', suffixes='_home', how='left')
#    abt_table.drop(['date_x', 'id', 'team_fifa_api_id', 'team_api_id', 'date_y'], axis=1, inplace=True)
#    abt_table = pd.merge(abt_table, team_stats_data, left_on='away_team_api_id', right_on='team_api_id', suffixes='_away', how='left')
#    abt_table.drop(['date_x', 'id', 'team_fifa_api_id', 'team_api_id', 'date_y'], axis=1, inplace=True)
#    print(abt_table.columns)
    return abt_table

def get_recent_matches( full_match_data, team, date, num_matches):
    #Get all of the matches with the given team involved
    all_team_matches = full_match_data[(full_match_data['home_team_api_id'] == team) | (full_match_data['away_team_api_id'] == team)]
    #Sort the matches by date and pick the last 'num_matches' before the given date
    last_team_matches = all_team_matches[all_team_matches.date < date].sort_values(by = 'date', ascending = False).iloc[0:num_matches,:]
    return last_team_matches

def get_recent_against_matches( full_match_data, team1, team2, date, num_matches):
    #Get all of the matches with the given team involved
    all_team_matches_1 = full_match_data[(full_match_data['home_team_api_id'] == team1) & (full_match_data['away_team_api_id'] == team2)]
    all_team_matches_2 = full_match_data[(full_match_data['home_team_api_id'] == team2) & (full_match_data['away_team_api_id'] == team1)]
    all_team_matches = pd.concat([all_team_matches_1, all_team_matches_2])
    #Sort the matches by date and pick the last 'num_matches' before the given date
    last_team_matches = all_team_matches[all_team_matches.date < date].sort_values(by = 'date', ascending = False).iloc[0:num_matches,:]
    return last_team_matches

def get_recent_wins(match_subset, team):
    #Counts recent games where given team scored more than away team
    home_wins = int(match_subset.home_team_goal[(match_subset.home_team_api_id == team) & (match_subset.home_team_goal > match_subset.away_team_goal)].count())
    home_losses = int(match_subset.home_team_goal[(match_subset.home_team_api_id == team) & (match_subset.home_team_goal < match_subset.away_team_goal)].count())
    home_ties = int(match_subset.home_team_goal[(match_subset.home_team_api_id == team) & (match_subset.home_team_goal == match_subset.away_team_goal)].count())
    
    #Counts recent games where given team scored more than home team
    away_wins = int(match_subset.away_team_goal[(match_subset.away_team_api_id == team) & (match_subset.away_team_goal > match_subset.home_team_goal)].count())
    away_losses = int(match_subset.away_team_goal[(match_subset.away_team_api_id == team) & (match_subset.away_team_goal < match_subset.home_team_goal)].count())
    away_ties = int(match_subset.away_team_goal[(match_subset.away_team_api_id == team) & (match_subset.away_team_goal == match_subset.home_team_goal)].count())
    
    #Gets and returns total number of wins out of the given subset of matches by the given team
    total_wins = home_wins + away_wins
    total_losses = home_losses + away_losses
    total_ties = home_ties + away_ties
    total_games = total_wins + total_losses + total_ties
    if total_games == 0:
        # If no games were found, just guess as 50/50 with slight advantage to home team
        return 0.501
    
    win_percent = (total_wins + (total_ties * .33)) / total_games
    return win_percent  

def get_goals(matches, team):
    #Find home and away goals
    home_goals = int(matches.home_team_goal[matches.home_team_api_id == team].sum())
    away_goals = int(matches.away_team_goal[matches.away_team_api_id == team].sum())

    total_goals = home_goals + away_goals
    
    #Return total goals
    return total_goals

def get_goals_conceided(matches, team):
    #Find home and away goals
    home_goals = int(matches.home_team_goal[matches.away_team_api_id == team].sum())
    away_goals = int(matches.away_team_goal[matches.home_team_api_id == team].sum())

    total_goals = home_goals + away_goals

    #Return total goals
    return total_goals
    

def create_match_features(match, full_match_data, match_data, num_matches = 10):
    #Get details about single match
    date = match.date
    home_team = match.home_team_api_id
    away_team = match.away_team_api_id
    
    # Get the most recent matches for each team
    last_home_team_matches = get_recent_matches(full_match_data, home_team, date, num_matches)
    last_away_team_matches = get_recent_matches(full_match_data, away_team, date, num_matches)
    
    # Get the most recent matches that both teams played each other
    last_against_matches = get_recent_against_matches(full_match_data, home_team, away_team, date, num_matches)
    
    #Create goal variables
    home_goals_scored = get_goals(last_home_team_matches, home_team)
    away_goals_scored = get_goals(last_away_team_matches, away_team)
    
    home_goals_allowed = get_goals_conceided(last_home_team_matches, home_team)
    away_goals_allowed = get_goals_conceided(last_away_team_matches, away_team)
    
    #Create results df for match features
    match_features = pd.DataFrame()
    match_features.loc[0, 'match_api_id'] = match.match_api_id
    
    home_win_percent = get_recent_wins(last_home_team_matches, home_team)
    match_features.loc[0, 'home_win_percentage'] = home_win_percent
    
    away_win_percent = get_recent_wins(last_away_team_matches, away_team)
    match_features.loc[0, 'away_win_percentage'] = away_win_percent
    
    home_against_win_percent = get_recent_wins(last_against_matches, home_team)
    match_features.loc[0, 'home_win_percent_against_away'] = home_against_win_percent
    
    home_goal_differential = home_goals_scored - home_goals_allowed
    match_features.loc[0, 'total_home_goal_differential'] = home_goal_differential
    
    away_goal_differential = away_goals_scored - away_goals_allowed
    match_features.loc[0, 'total_away_goal_differential'] = away_goal_differential
    
    return match_features.loc[0]

def add_recent_matches(abt_table, full_match_data, match_data):
    match_stats = match_data.apply(lambda x: create_match_features(x, full_match_data, match_data, num_matches=5), axis=1)
    abt_table = pd.merge(abt_table, match_stats, on = 'match_api_id', how = 'left')
    return abt_table

def set_match_outcome(abt_table):
    if abt_table['home_goal_differential']  == 0:
        return 'draw'
    elif abt_table['home_goal_differential']  > 0:
        return 'win'
    else:
        return 'loss'

def create_features(full_match_data, match_data, player_data, player_stats_data, team_data, team_stats_data, league_data, country_data):
    
    abt_table = match_data[['date', 'match_api_id', 'country_id', 'league_id', 'home_team_api_id', 'away_team_api_id', 'home_team_goal', 'away_team_goal',
                            'home_player_1', 'home_player_2', 'home_player_3', 'home_player_4', 'home_player_5', 'home_player_6', 'home_player_7', 'home_player_8', 
                            'home_player_9', 'home_player_10', 'home_player_11', 'away_player_1', 'away_player_2', 'away_player_3', 'away_player_4', 'away_player_5', 'away_player_6', 'away_player_7', 'away_player_8', 
                            'away_player_9', 'away_player_10', 'away_player_11']]
    abt_table.is_copy = False
    abt_table['home_goal_differential'] = match_data['home_team_goal'] - match_data['away_team_goal']
    
    abt_table = add_player_stats(abt_table, player_data, player_stats_data)
    abt_table = add_team_stats(abt_table, team_data, team_stats_data) #Need to implement
    abt_table = add_recent_matches(abt_table, full_match_data, match_data)
    abt_table.drop('match_api_id', axis=1, inplace=True)
    abt_table['actual_outcome'] = abt_table.apply(set_match_outcome, axis=1)
    
    return abt_table

def predict_match_outcome(abt_table, based_on, home_advantage):
    if based_on == 'rating':
        if abs(((abt_table['avg_home_player_rating'] * home_advantage) - abt_table['avg_away_player_rating'])) < 0.05:
            return 'draw'
        elif (abt_table['avg_home_player_rating'] * home_advantage) > abt_table['avg_away_player_rating']:
            return 'win'
        else:
            return 'loss'
    elif based_on == 'age':
        # age is not affected by home/away??
        home_advantage = 1
        if (abt_table['avg_home_player_age'] * home_advantage) < abt_table['avg_away_player_age']:
            return 'win'
        else:
            return 'loss'
    elif based_on == 'win_percent_overall':
        if (abt_table['home_win_percentage'] * home_advantage) > abt_table['away_win_percentage']:
            return 'win'
        else:
            return 'loss'
    elif based_on == 'win_percent_against':
        # Based on whether home team wins over half the games against opponent
        if (abt_table['home_win_percent_against_away'] * home_advantage) > 0.5:
            return 'win'
        else:
            return 'loss'
    else:
        return 'Not a valid based_on option'

def check_accuracy(abt_table):
    if abt_table['predicted_outcome'] == abt_table['actual_outcome']:
        return 'correct'
    else:
        return 'wrong'

def predict_outcomes(abt_table, based_on, home_advantage):
    abt_table['predicted_outcome'] = abt_table.apply(predict_match_outcome, args=(based_on, home_advantage), axis=1)
    return abt_table
    
def check_results(abt_table):
    abt_table['results'] = abt_table.apply(check_accuracy, axis=1)
    return abt_table

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        title = "Normalized confusion matrix"
    else:
        title = 'Confusion matrix, without normalization'

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
def plot_outcome_chart(predicted_values, title='Predicted outcomes'):
    objects = ('Draw', 'Loss', 'Win')
    y_pos = np.arange(len(objects))
    values = list(predicted_values.values())
    if len(values) < 3:
        values.insert(0, 0)
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Count')
    plt.title(title)
    plt.show()
    
def plot_model_comparison(model_names, train_accuracies, test_accuracies, cv_scores):
    raw_data = pd.DataFrame(
        {'model': model_names,
         'train_accuracy': train_accuracies,
         'test_accuracy': test_accuracies,
         'cv_score': cv_scores
        })
    pos = list(range(len(raw_data['train_accuracy']))) 
    width = 0.25 
    fig, ax = plt.subplots(figsize=(20,10))
    
    plt.bar(pos, 
            raw_data['train_accuracy'], 
            width, 
            alpha=0.5, 
            color='#B3CCFF', 
            label=raw_data['model'][0]) 
    
    plt.bar([p + width for p in pos], 
            raw_data['test_accuracy'],
            width, 
            alpha=0.5, 
            color='#4D88FF', 
            label=raw_data['model'][1]) 
    
    plt.bar([p + width*2 for p in pos], 
            raw_data['cv_score'],
            width, 
            alpha=0.5, 
            color='#003399', 
            label=raw_data['model'][2]) 
    
#    for rect in raw_data['train_accuracy']:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., height * 1.05,
#                '%d' % int(height),
#                ha='center', va='bottom')
#    for rect in raw_data['test_accuracy']:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., height * 1.05,
#                '%d' % int(height),
#                ha='center', va='bottom')
#    for rect in raw_data['cv_score']:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., height * 1.05,
#                '%d' % int(height),
#                ha='center', va='bottom')
    
    ax.set_ylabel('Accuracy')
    ax.set_title('Model Comparison')
    ax.set_xticks([p + 1.5 * width for p in pos])
    ax.set_xticklabels(raw_data['model'])
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim( [0, 1] )
    # Adding the legend and showing the plot
    plt.legend(['Training Accuracy', 'Testing Accuracy', 'CV Score'], loc='upper left')
    plt.grid()
    plt.show()
    
def plot_feature_comparison(num_features, cv_scores):
    
    y_pos = np.arange(len(num_features))
    
    plt.bar(y_pos, cv_scores, align='center', alpha=0.5)
    plt.xticks(y_pos, num_features)
    plt.xlabel('Number of Features')
    plt.ylabel('Cross-Validation Score')
    plt.title('CV Scores for Given Number of Features')
    plt.ylim( [.45, .55] )
    plt.show()
        
def main(numRecords=1000):
    # Path to the database file
    database = "database.sqlite"
    
    
    conn = create_connection(database)
    
    player_data = read_data("Player", conn)
    player_stats_data = read_data("Player_Attributes", conn)
    team_data = read_data("Team", conn)
    team_stats_data = read_data("Team_Attributes", conn)
    full_match_data = read_data("Match", conn)
    league_data = read_data("League", conn)
    country_data = read_data("Country", conn)
    
    # Filters the data to only include rows where none of these fields are missing
    non_null_cols = ["country_id", "league_id", "date", "match_api_id", "home_team_api_id", 
        "away_team_api_id", "home_team_goal", "away_team_goal", "home_player_1", "home_player_2",
        "home_player_3", "home_player_4", "home_player_5", "home_player_6", "home_player_7", 
        "home_player_8", "home_player_9", "home_player_10", "home_player_11", "away_player_1",
        "away_player_2", "away_player_3", "away_player_4", "away_player_5", "away_player_6",
        "away_player_7", "away_player_8", "away_player_9", "away_player_10", "away_player_11"]
    full_match_data.dropna(subset = non_null_cols, inplace = True)
    
    match_data = full_match_data.tail(numRecords)
    abt_table = create_features(full_match_data, match_data, player_data, player_stats_data, team_data, team_stats_data, league_data, country_data)

    #############    Creates dataset with 13 features
    data_origin = pd.DataFrame()
    data_origin['country_id'] = abt_table['country_id']
    data_origin['league_id'] = abt_table['league_id']
    data_origin['home_team_api_id'] = abt_table['home_team_api_id']
    data_origin['away_team_api_id'] = abt_table['away_team_api_id']
    data_origin['avg_home_player_rating'] = abt_table['avg_home_player_rating']
    data_origin['avg_away_player_rating'] = abt_table['avg_away_player_rating']
    data_origin['avg_home_player_age'] = abt_table['avg_home_player_age']
    data_origin['avg_away_player_age'] = abt_table['avg_away_player_age']
    data_origin['home_win_percentage'] = abt_table['home_win_percentage']
    data_origin['away_win_percentage'] = abt_table['away_win_percentage']
    data_origin['home_win_percent_against_away'] = abt_table['home_win_percent_against_away']
    data_origin['home_goal_differential'] = abt_table['total_home_goal_differential']
    data_origin['away_goal_differential'] = abt_table['total_away_goal_differential']
    x = data_origin.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pd.DataFrame(x_scaled, columns=data_origin.columns)
    
    #############    Creates dataset with 4 features
    dataSmall_origin = pd.DataFrame()
    dataSmall_origin['diff_avg_player_rating'] = abt_table['avg_home_player_rating'] - abt_table['avg_away_player_rating']
    dataSmall_origin['diff_win_percentage'] = abt_table['home_win_percentage'] - abt_table['away_win_percentage']
    dataSmall_origin['home_win_percent_against_away'] = abt_table['home_win_percent_against_away']
    dataSmall_origin['diff_goal_differential'] = abt_table['total_home_goal_differential'] - abt_table['total_away_goal_differential']
    x = dataSmall_origin.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    dataSmall = pd.DataFrame(x_scaled, columns=dataSmall_origin.columns)
    
    target = pd.DataFrame()
    abt_table.actual_outcome = pd.Categorical(abt_table.actual_outcome)
    print("Dictionary values: ")
    print(dict( enumerate(abt_table['actual_outcome'].cat.categories) ))
    print()
    
    target['expected'] = abt_table.actual_outcome.cat.codes
    print("Actual outcomes:")
    print(target['expected'].value_counts())
    print()    
    
    
    ########## Keeps track of accuracies for later plots
    model_names = []
    train_accuracies = []
    test_accuracies = []
    cv_scores = []
    class_names = ['draw','loss','win']
    
    
    #############    Five models with all 13 features
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    
    GNB_clf = GaussianNB()
    GNB_clf.fit(x_train, y_train['expected'])
    GNB_predicted = cross_val_predict(GNB_clf, data, target['expected'])
    GNB_scores = cross_val_score(GNB_clf, data, target.values.ravel(), cv=cv)
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    model_names.append('GaussianNB')
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (cv_score))
    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
    AB_clf = AdaBoostClassifier(n_estimators = 200, random_state = 3)
    AB_clf.fit(x_train, y_train['expected'])
    AB_predicted = cross_val_predict(AB_clf, data, target['expected'])
    AB_scores = cross_val_score(AB_clf, data, target, cv=cv)
    unique, counts = np.unique(AB_predicted, return_counts=True)
    AB_counts = dict(zip(unique, counts))
    AB_confusion = confusion_matrix(target,AB_predicted)
    model_names.append('AdaBoost')
    train_accuracy = accuracy_score(y_train, AB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, AB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, AB_predicted)
    cv_scores.append(cv_score)
    print("AdaBoost Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(AB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(AB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (AB_scores.mean(), AB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, AB_predicted) ))
    plot_outcome_chart(AB_counts)
    plt.figure()
    plot_confusion_matrix(AB_confusion, class_names)
    plt.show()
    print(classification_report(target, AB_predicted)) 
    print()
    importances = AB_clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print ('Feature Ranking: ')
    for i in range(0,12):
        print ("{} feature no.{} ({})".format(i+1,indices[i],importances[indices[i]]))
    
    RF_clf = RandomForestClassifier(n_estimators = 200, random_state = 3)
    RF_clf.fit(x_train, y_train['expected'])
    RF_predicted = cross_val_predict(RF_clf, data, target['expected'])
    RF_scores = cross_val_score(RF_clf, data, target, cv=cv)
    unique, counts = np.unique(RF_predicted, return_counts=True)
    RF_counts = dict(zip(unique, counts))
    RF_confusion = confusion_matrix(target,RF_predicted)
    model_names.append('RandomForest')
    train_accuracy = accuracy_score(y_train, RF_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, RF_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, RF_predicted)
    cv_scores.append(cv_score)
    print("Random Forest Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(RF_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(RF_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (RF_scores.mean(), RF_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, RF_predicted) ))
    plot_outcome_chart(RF_counts)
    plt.figure()
    plot_confusion_matrix(RF_confusion, class_names)
    plt.show()
    print(classification_report(target, RF_predicted)) 
    print()
    
    GB_clf = GradientBoostingClassifier(n_estimators = 200, random_state = 3)
    GB_clf.fit(x_train, y_train['expected'])
    GB_predicted = cross_val_predict(GB_clf, data, target['expected'])
    GB_scores = cross_val_score(GB_clf, data, target, cv=cv)
    unique, counts = np.unique(GB_predicted, return_counts=True)
    GB_counts = dict(zip(unique, counts))
    GB_confusion = confusion_matrix(target,GB_predicted)
    model_names.append('GradientBoosting')
    train_accuracy = accuracy_score(y_train, GB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, GB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, GB_predicted)
    cv_scores.append(cv_score)
    print("Gradient Boosting Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GB_scores.mean(), GB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GB_predicted) ))
    plot_outcome_chart(GB_counts)
    plt.figure()
    plot_confusion_matrix(GB_confusion, class_names)
    plt.show()
    print(classification_report(target, GB_predicted)) 
    print()
    
    DT_clf = DecisionTreeClassifier(random_state = 3)
    DT_clf.fit(x_train, y_train['expected'])
    DT_predicted = cross_val_predict(DT_clf, data, target['expected'])
    DT_scores = cross_val_score(DT_clf, data, target, cv=cv)
    unique, counts = np.unique(DT_predicted, return_counts=True)
    DT_counts = dict(zip(unique, counts))
    DT_confusion = confusion_matrix(target,DT_predicted)
    model_names.append('DecisionTree')
    train_accuracy = accuracy_score(y_train, DT_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, DT_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, DT_predicted)
    cv_scores.append(cv_score)
    print("Decision Tree Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(DT_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(DT_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (DT_scores.mean(), DT_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, DT_predicted) ))
    plot_outcome_chart(DT_counts)
    plt.figure()
    plot_confusion_matrix(DT_confusion, class_names)
    plt.show()
    print(classification_report(target, DT_predicted)) 
    print()
    

    #############    Five models with only 4 features
    x_train, x_test, y_train, y_test = train_test_split(dataSmall, target, test_size=0.2, random_state=3)
    print()
    print("Models with fewer features:")
    
    GNB_clf = GaussianNB()
    GNB_clf.fit(x_train, y_train['expected'])
    GNB_predicted = cross_val_predict(GNB_clf, dataSmall, target['expected'])
    GNB_scores = cross_val_score(GNB_clf, dataSmall, target.values.ravel(), cv=cv)
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    model_names.append('GaussianNB - Small')
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GNB_predicted) ))
    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
    AB_clf = AdaBoostClassifier(n_estimators = 200, random_state = 3)
    AB_clf.fit(x_train, y_train['expected'])
    AB_predicted = cross_val_predict(AB_clf, dataSmall, target['expected'])
    AB_scores = cross_val_score(AB_clf, dataSmall, target, cv=cv)
    unique, counts = np.unique(AB_predicted, return_counts=True)
    AB_counts = dict(zip(unique, counts))
    AB_confusion = confusion_matrix(target,AB_predicted)
    model_names.append('AdaBoost - Small')
    train_accuracy = accuracy_score(y_train, AB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, AB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, AB_predicted)
    cv_scores.append(cv_score)
    print("AdaBoost Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(AB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(AB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (AB_scores.mean(), AB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, AB_predicted) ))
    plot_outcome_chart(AB_counts)
    plt.figure()
    plot_confusion_matrix(AB_confusion, class_names)
    plt.show()
    print(classification_report(target, AB_predicted)) 
    print()
    importances = AB_clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print ('Feature Ranking: ')
    for i in range(0, 4):
        print ("{} feature no.{} ({})".format(i+1,indices[i],importances[indices[i]]))
        
    RF_clf = RandomForestClassifier(n_estimators = 200, random_state = 3)
    RF_clf.fit(x_train, y_train['expected'])
    RF_predicted = cross_val_predict(RF_clf, dataSmall, target['expected'])
    RF_scores = cross_val_score(RF_clf, dataSmall, target, cv=cv)
    unique, counts = np.unique(RF_predicted, return_counts=True)
    RF_counts = dict(zip(unique, counts))
    RF_confusion = confusion_matrix(target,RF_predicted)
    model_names.append('RandomForest - Small')
    train_accuracy = accuracy_score(y_train, RF_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, RF_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, RF_predicted)
    cv_scores.append(cv_score)
    print("Random Forest Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(RF_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(RF_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (RF_scores.mean(), RF_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, RF_predicted) ))
    plot_outcome_chart(RF_counts)
    plt.figure()
    plot_confusion_matrix(RF_confusion, class_names)
    plt.show()
    print(classification_report(target, RF_predicted)) 
    print()
    
    GB_clf = GradientBoostingClassifier(n_estimators = 200, random_state = 3)
    GB_clf.fit(x_train, y_train['expected'])
    GB_predicted = cross_val_predict(GB_clf, dataSmall, target['expected'])
    GB_scores = cross_val_score(GB_clf, dataSmall, target, cv=cv)
    unique, counts = np.unique(GB_predicted, return_counts=True)
    GB_counts = dict(zip(unique, counts))
    GB_confusion = confusion_matrix(target,GB_predicted)
    model_names.append('GradientBoosting - Small')
    train_accuracy = accuracy_score(y_train, GB_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, GB_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, GB_predicted)
    cv_scores.append(cv_score)
    print("Gradient Boosting Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GB_scores.mean(), GB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GB_predicted) ))
    plot_outcome_chart(GB_counts)
    plt.figure()
    plot_confusion_matrix(GB_confusion, class_names)
    plt.show()
    print(classification_report(target, GB_predicted)) 
    print()
    
    DT_clf = DecisionTreeClassifier(random_state = 3)
    DT_clf.fit(x_train, y_train['expected'])
    DT_predicted = cross_val_predict(DT_clf, dataSmall, target['expected'])
    DT_scores = cross_val_score(DT_clf, dataSmall, target, cv=cv)
    unique, counts = np.unique(DT_predicted, return_counts=True)
    DT_counts = dict(zip(unique, counts))
    DT_confusion = confusion_matrix(target,DT_predicted)
    model_names.append('DecisionTree - Small')
    train_accuracy = accuracy_score(y_train, DT_clf.predict(x_train))
    train_accuracies.append(train_accuracy)
    test_accuracy = accuracy_score(y_test, DT_clf.predict(x_test))
    test_accuracies.append(test_accuracy)
    cv_score = accuracy_score(target, DT_predicted)
    cv_scores.append(cv_score)
    print("Decision Tree Classifier Model: ")
    print("  Score of {} for training set: {:.4f}.".format(DT_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(DT_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (DT_scores.mean(), DT_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, DT_predicted) ))
    plot_outcome_chart(DT_counts)
    plt.figure()
    plot_confusion_matrix(DT_confusion, class_names)
    plt.show()
    print(classification_report(target, DT_predicted)) 
    print()
    
    #############    Graph to compare original models
    plot_model_comparison(model_names, train_accuracies,
                          test_accuracies, cv_scores)
    
    #############    Let's improve this one model...
    print()
    print()
    print('Feature Comparison for best model:')
    num_features = ['1', '2', '3', '4']
    cv_scores = []
    
    data_origin = pd.DataFrame()
    data_origin['diff_avg_player_rating'] = abt_table['avg_home_player_rating'] - abt_table['avg_away_player_rating']
    x = data_origin.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pd.DataFrame(x_scaled, columns=data_origin.columns)
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    GNB_clf = GaussianNB()
    GNB_clf.fit(x_train, y_train['expected'])
    GNB_predicted = cross_val_predict(GNB_clf, data, target['expected'])
    GNB_scores = cross_val_score(GNB_clf, data, target.values.ravel(), cv=cv)
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GNB_predicted) ))
    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
    data_origin = pd.DataFrame()
    data_origin['diff_avg_player_rating'] = abt_table['avg_home_player_rating'] - abt_table['avg_away_player_rating']
    data_origin['diff_goal_differential'] = abt_table['total_home_goal_differential'] - abt_table['total_away_goal_differential']
    x = data_origin.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pd.DataFrame(x_scaled, columns=data_origin.columns)
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    GNB_clf = GaussianNB()
    GNB_clf.fit(x_train, y_train['expected'])
    GNB_predicted = cross_val_predict(GNB_clf, data, target['expected'])
    GNB_scores = cross_val_score(GNB_clf, data, target.values.ravel(), cv=cv)
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GNB_predicted) ))
    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
    data_origin = pd.DataFrame()
    data_origin['diff_avg_player_rating'] = abt_table['avg_home_player_rating'] - abt_table['avg_away_player_rating']
    data_origin['diff_goal_differential'] = abt_table['total_home_goal_differential'] - abt_table['total_away_goal_differential']
    data_origin['diff_win_percentage'] = abt_table['home_win_percentage'] - abt_table['away_win_percentage']
    x = data_origin.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pd.DataFrame(x_scaled, columns=data_origin.columns)
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    GNB_clf = GaussianNB()
    GNB_clf.fit(x_train, y_train['expected'])
    GNB_predicted = cross_val_predict(GNB_clf, data, target['expected'])
    GNB_scores = cross_val_score(GNB_clf, data, target.values.ravel(), cv=cv)
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GNB_predicted) ))
    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
    data_origin = pd.DataFrame()
    data_origin['diff_avg_player_rating'] = abt_table['avg_home_player_rating'] - abt_table['avg_away_player_rating']
    data_origin['diff_goal_differential'] = abt_table['total_home_goal_differential'] - abt_table['total_away_goal_differential']
    data_origin['diff_win_percentage'] = abt_table['home_win_percentage'] - abt_table['away_win_percentage']
    data_origin['home_win_percent_against_away'] = abt_table['home_win_percent_against_away']
    x = data_origin.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pd.DataFrame(x_scaled, columns=data_origin.columns)
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=3)
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=3)
    GNB_clf = GaussianNB()
    GNB_clf.fit(x_train, y_train['expected'])
    GNB_predicted = cross_val_predict(GNB_clf, data, target['expected'])
    GNB_scores = cross_val_score(GNB_clf, data, target.values.ravel(), cv=cv)
    unique, counts = np.unique(GNB_predicted, return_counts=True)
    GNB_counts = dict(zip(unique, counts))
    GNB_confusion = confusion_matrix(target,GNB_predicted)
    train_accuracy = accuracy_score(y_train, GNB_clf.predict(x_train))
    test_accuracy = accuracy_score(y_test, GNB_clf.predict(x_test))
    cv_score = accuracy_score(target, GNB_predicted)
    cv_scores.append(cv_score)
    print("GaussianNB Model: ")
    print("  Score of {} for training set: {:.4f}.".format(GNB_clf.__class__.__name__, train_accuracy))
    print("  Score of {} for test set: {:.4f}.".format(GNB_clf.__class__.__name__, test_accuracy))
    print("  Cross validation score: %0.2f (+/- %0.2f)" % (GNB_scores.mean(), GNB_scores.std() * 2))
    print("  Predicted values accuracy: %0.2f" % (accuracy_score(target, GNB_predicted) ))
    plot_outcome_chart(GNB_counts)
    plt.figure()
    plot_confusion_matrix(GNB_confusion, class_names)
    plt.show()
    print(classification_report(target, GNB_predicted)) 
    print()
    
    plot_feature_comparison(num_features, cv_scores)

    

start_time = time.time()    
main(numRecords=5000)
print()
print("--- %s seconds ---" % (time.time() - start_time))
