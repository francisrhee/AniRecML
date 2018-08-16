from surprise import BaselineOnly
from collections import defaultdict
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise import NormalPredictor
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV
import pandas as pd
# from collabfilt.input import getData
from datetime import date, datetime

def get_top_n(df, user, predictions, n=5):

    year = datetime.now().year

    # First map the predictions to each user.
    top_n = defaultdict(list)
    counter = 0
    for uid, iid, true_r, est, _ in predictions:
        # For debugging purposes
        counter += 1
        if(counter % 1000 == 0):
            print(counter)
        # If started in current year and is currently airing
        if (df.loc[df['MediaTitle'] == iid]['CurrentlyAiring'].iloc[0] == True and df.loc[df['MediaTitle'] == iid]['Year'].iloc[0] == year):
            top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n[user] # Return top_n_ongoing[user]

def get_year():
    return datetime.now.year


def get_season(now):
    Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
    seasons = [('WINTER', (date(Y, 1),      date(Y, 3, 20))),
               ('SPRING', (date(Y, 3, 21),  date(Y, 6, 20))),
               ('SUMMER', (date(Y, 6, 21),  date(Y, 9, 22))),
               ('FALL',   (date(Y, 9, 23),  date(Y, 12, 20))),
               ('WINTER', (date(Y, 12, 21), date(Y, 12, 31)))]


    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

def train(user):
    # Get data
    # df = getData(user)
    df = pd.read_csv("C:/Users/francis/PycharmProjects/AniRecML/src/collabfilt/data.csv")
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(df[['UserName', 'MediaTitle', 'Score']], reader=reader)





    # # Tune params
    # param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005],
    #               'reg_all': [0.4, 0.6]}
    # gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3) # Selects best param out of given param_grid
    # gs.fit(data)
    # print(gs.best_score['rmse'])
    # print(gs.best_params['rmse'])
    # algo = gs.best_estimator['rmse']
    # algo.fit(data.build_full_trainset())
    # results_df = pd.DataFrame.from_dict(gs.cv_results)

    # trainset, testset = train_test_split(data, test_size=.25) # Predictions doesn't predict everything. Try not splitting train and test sets?
    trainset = data.build_full_trainset()

    # Train
    algo = SVD()
    algo.fit(trainset)

    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    top_n = get_top_n(df, user, predictions, n=5)

    # Print the recommended items for each user
    for i in range(len(top_n)):
        print(top_n[i][0])
    print("End.")
    # Metrics
    # accuracy.rmse(predictions)
    # cross_validate(NormalPredictor(), data, cv=2, verbose=True)

train("FrannehR")