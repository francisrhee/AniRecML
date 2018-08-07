from surprise import BaselineOnly
from surprise import Dataset
from surprise import Reader
from surprise import NormalPredictor
from surprise.model_selection import cross_validate
from collabfilt.input import queryData

# path to dataset file
df = queryData()

reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(df[['UserName', 'MediaTitle', 'Score']], reader=reader)

cross_validate(NormalPredictor(), data, cv=2, verbose=True)