import requests
import json

''' TODO:
1. Find a query that gets a list of all animes on user's list, and their score/features
2. Find out how to do logistic regression on tensorflow
3. Convert this response into a csv of features|y, or whatever the input is for tensorflow
4. Run logistic regression on training set
5. Optimize lambda based on cross-validation set (Note the accuracies for paper), see if good generalization on test set
6. Plot learning curves from different account examples to see if more data would help (error vs training set size for both training and cv)
7. Port to a website using Django?
'''

# TODO: Change query to pull user data
query = '''
query GetAnimeList($userName: String) {
  MediaListCollection(userName: $userName, type: ANIME) {
    lists {
      name
      entries {
        score
        media {
          title {
            romaji
            english
          }
          episodes
          duration
          genres
          studios(isMain: true) {
            nodes {
              name
            }
          }
          tags {
            name
            category
          }
        }
      }
    }
  }
}

'''

# Define our query variables and values that will be used in the query request
variables = {
    "userName": "frhee97"
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})

responseJSON = json.loads(response.text)
print(json.dumps(responseJSON, indent=4, sort_keys=True))

