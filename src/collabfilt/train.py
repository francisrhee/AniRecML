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

from collabfilt.input import getData


def get_top_n(user, predictions, n=10):
    # TODO: Make this only for one user and exclude already seen shows

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n[user]

def train(user):
    # Get data
    df = getData(user)
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

    trainset, testset = train_test_split(data, test_size=.25)

    # Train
    algo = SVD()
    algo.fit(trainset)
    predictions = algo.test(testset)

    top_n = get_top_n(user, predictions, n=10)

    # Print the recommended items for each user
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])

    # Metrics
    # accuracy.rmse(predictions)
    # cross_validate(NormalPredictor(), data, cv=2, verbose=True)

train("FrannehR")