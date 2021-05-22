from django.shortcuts import render

# Create your views here.

from datetime import datetime, timedelta

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response





@api_view(['GET'])
def list_langs(request):
    """
    Dictionary of languages used in top 100 trending repositories on Github,
    
    with following attributes:
	    + the number of public repos using the language
	    + list of public repos' urls (api + html urls)
    

    """
    
    # We will return the most recent public repos in the 30 days window.

    today = datetime.now()
    thirty_days_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # api call to list of 100 trending public repositories in GH sorted by stars
    # in descending order

    url = "https://api.github.com/search/repositories?q=created:>{0}&sort=stars&order=desc&page=1&per_page=100".format(
        thirty_days_ago)


    response = requests.get(url)
    
    # Response state if 200 it's OK.

    if response.status_code == 200:
        trending_repositories = response.json()['items']
        list_languages = {}
        NO_OF_REPOS = "N° of public repos"
        LIST_OF_REPOS = "List of public repos"
        URL = "url"
        HTML_URL = "html_url"

        for repo in trending_repositories:
            language = repo['language']
            prevEntry = list_languages.setdefault(language,
                                                  {NO_OF_REPOS: 0,
                                                   LIST_OF_REPOS: []})

            list_languages[language][NO_OF_REPOS] = prevEntry[NO_OF_REPOS] + 1
            prevEntry[LIST_OF_REPOS].append({repo[URL], repo[HTML_URL]})

        return Response(list_languages)

    return Response(response, status=response.status_code)
