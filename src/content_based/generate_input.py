import requests
import json
import re
import numpy as np
from content_based.helper_functions import encodeOneHot

''' TODO:
1. Find a query that gets a list of all animes on user's list, and their score/features
2. Find out how to do logistic regression on tensorflow
3. Convert this response into a csv of features|y, or whatever the input is for tensorflow
4. Run logistic regression on training set
5. Optimize lambda based on cross-validation set (Note the accuracies for paper), see if good generalization on test set
6. Plot learning curves from different account examples to see if more data would help (error vs training set size for both training and cv)
7. Port to a website using Django?
'''

def queryData():
    query = '''
    query GetAnimeList($userName: String) {
      GenreCollection
      
      User(name:$userName) {
        mediaListOptions {
          scoreFormat
        }
      }

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
            }
          }
        }
      }
    }
    '''

    # Define our query variables and values that will be used in the query request
    variables = {
        "userName": "FrannehR"
    }

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    responseJSON = json.loads(response.text)

    # Extract relevant features
    genreListFull = responseJSON['data']['GenreCollection']
    lists = responseJSON['data']['MediaListCollection']['lists']
    lists = [lists[x] for x in range(len(lists)) if bool(re.search('Completed|Dropped', lists[x]['name']))]

    scores = [lists[l]['entries'][x]['score'] for l in range(len(lists)) for x in range(len(lists[l]['entries']))]
    scoreFormat = responseJSON['data']['User']['mediaListOptions']['scoreFormat']



    numEpisodes = [lists[l]['entries'][x]['media']['episodes'] for l in range(len(lists)) for x in
                   range(len(lists[l]['entries']))]
    avgEpDuration = [lists[l]['entries'][x]['media']['duration'] for l in range(len(lists)) for x in
                     range(len(lists[l]['entries']))]
    genres = [lists[l]['entries'][x]['media']['genres'] for l in range(len(lists)) for x in
              range(len(lists[l]['entries']))]
    studios = [lists[l]['entries'][x]['media']['studios']['nodes'] for l in range(len(lists)) for x in
               range(len(lists[l]['entries']))]

    studiosFormatted = []
    for i in range(len(studios)):
        studiosFormatted.append([studios[i][s]['name'] for s in range(len(studios[i]))])

    return scores, numEpisodes, avgEpDuration, genres, studiosFormatted, genreListFull


# List of all possible studios takes a little more effort to get
def getStudioListFull():
    studioList = []

    studioQuery = '''query ($page: Int) {
                  Page(page: $page) {
                    pageInfo {
                      hasNextPage
                    }
                    studios {
                      id
                      name
                    }
                  }
                }'''
    pageVariables = {
        "page": 1
    }

    while True:
        studioResponse = requests.post(url, json={'query': studioQuery, 'variables': pageVariables})
        studioResponseJSON = json.loads(studioResponse.text)
        studiosOnPage = studioResponseJSON['data']['Page']['studios']
        studioList.extend([studiosOnPage[s]['name'] for s in range(len(studiosOnPage))])

        pageVariables['page'] += 1

        if(studioResponseJSON['data']['Page']['pageInfo']['hasNextPage'] == False):
            break

    return studioList

def combineData(numEpisodes, avgEpDuration, genres, studiosFormatted, genreListFull, studioListFull):

    # Encode genres and studios to one-hot and combine data
    genresOneHot = encodeOneHot(genreListFull, genres)
    studiosOneHot = encodeOneHot(studioListFull, studiosFormatted)

    dataList = np.vstack((numEpisodes, avgEpDuration)).T
    dataList = list(np.hstack((dataList, genresOneHot, studiosOneHot)))

    return dataList

# def convertLabels(scores):
    # Convert all scores to a 5 point system
    # Convert them to a 1/0 system




url = 'https://graphql.anilist.co'
scores, numEpisodes, avgEpDuration, genres, studiosFormatted, genreListFull = queryData()
studioListFull = getStudioListFull()
inputData = combineData(numEpisodes, avgEpDuration, genres, studiosFormatted, genreListFull, studioListFull)