from surprise import BaselineOnly
from collections import defaultdict
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise import NormalPredictor
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from collabfilt.input import queryData

def get_top_n(predictions, n=10):
    # TODO: Make this only for one user and exclude already seen shows
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n



# Get data
df = queryData()
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(df[['UserName', 'MediaTitle', 'Score']], reader=reader)

trainset, testset = train_test_split(data, test_size=.25)

# Train
algo = SVD()
algo.fit(trainset)
predictions = algo.test(testset)

top_n = get_top_n(predictions, n=10)

# Print the recommended items for each user
for uid, user_ratings in top_n.items():
    print(uid, [iid for (iid, _) in user_ratings])

# Metrics
# accuracy.rmse(predictions)
# cross_validate(NormalPredictor(), data, cv=2, verbose=True)


