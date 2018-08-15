import requests
import json
import re
import pandas as pd
from random import randint
import time



url = 'https://graphql.anilist.co'

def queryUsers():
    maxPage = 10

    userQuery = '''
    query GetUserNames($page: Int) { 
      Page(page: $page) {
        pageInfo {
          total
          perPage
          lastPage
          hasNextPage
        }
        
        users(sort:USERNAME) {
          name
        }
      }
    }
    '''

    # pageNum = randint(0, 3400) # Approx. 3400 pages with 50 users each, grab a random page
    # print("Page: {}".format(pageNum))
    userVariables = {
        "page": 1 # pageNum
    }

    users = []
    while (True):
        print("Page: {}".format(userVariables['page']))

        try:
            response = requests.post(url, json={'query': userQuery, 'variables': userVariables})
            responseJSON = json.loads(response.text)
            users.extend([responseJSON['data']['Page']['users'][u]['name'] for u in range(len(responseJSON['data']['Page']['users']))]) # Add users in current page
            hasNextPage = responseJSON['data']['Page']['pageInfo']['hasNextPage']

            if (hasNextPage == False or userVariables['page'] >= maxPage):
                break

            userVariables['page'] += 1
        except TypeError:
            print("Calls being made too quickly. Waiting 60s. Page: {}".format(userVariables['page']))
            time.sleep(60)
            print("Continuing.")
            continue

    return users

def queryData(users):

    query = '''
    query GetAnimeList($userName: String) {
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
              id
              title {
                romaji
                english
              }
              status
            }
          }
        }
      }
    }
    '''

    # Define our query variables and values that will be used in the query request
    variables = {
        "userName": None
    }

    df = pd.DataFrame(columns=['UserName', 'MediaTitle', 'Score', 'CurrentlyAiring'])

    for i, u in enumerate(users):
        print("User #{}, {} remaining".format(i, len(users) - i))
        temp_df = pd.DataFrame()
        variables["userName"] = u

        try:
            response = requests.post(url, json={'query': query, 'variables': variables})
            responseJSON = json.loads(response.text)

            lists = responseJSON['data']['MediaListCollection']['lists']
            lists = [lists[x] for x in range(len(lists)) if bool(re.search('Completed|Dropped', lists[x]['name']))]
            scoreFormat = responseJSON['data']['User']['mediaListOptions']['scoreFormat']
            scores = [lists[l]['entries'][x]['score'] for l in range(len(lists)) for x in range(len(lists[l]['entries']))]
            mediaTitles = [lists[l]['entries'][x]['media']['title']['romaji'] for l in range(len(lists)) for x in range(len(lists[l]['entries']))]
            mediaStatus = [lists[l]['entries'][x]['media']['status'] for l in range(len(lists)) for x in range(len(lists[l]['entries']))]

            # Convert mediaStatus to 1 or 0 based on currently airing
            mediaStatus = [status == "RELEASING" for status in mediaStatus]

            # Convert all scores to POINT-10 system for consistency
            if (scoreFormat == "POINT_100"):
                scores = [int(score/100) for score in scores]
            elif (scoreFormat == "POINT_10_DECIMAL"):
                scores = [int(score) for score in scores]
            elif (scoreFormat == "POINT_5"):
                scores = [score*2 for score in scores]
            elif (scoreFormat == "POINT_3"):
                scores = [int(score*(10/3)) for score in scores]

            # Input into dataframe
            scores = pd.Series(scores)
            mediaTitles = pd.Series(mediaTitles)
            userNameEntries = pd.Series([u for i in range(len(mediaTitles))])

            temp_df['UserName'] = userNameEntries
            temp_df['MediaTitle'] = mediaTitles
            temp_df['Score'] = scores
            temp_df['CurrentlyAiring'] = mediaStatus

            # Remove entries with no score
            temp_df = temp_df[temp_df.Score != 0]

            df = df.append(temp_df)

        except TypeError:
            print("Calls being made too quickly. Waiting 60s. User: {}".format(u))
            time.sleep(60)
            print("Continuing.")
            continue

    return df

def getData(user):
    users = queryUsers()
    users.insert(0, user)
    df = queryData(users)
    df.to_csv('data.csv')
    return df