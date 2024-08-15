import requests
import random


def getMeme(subreddit: str = None, json: bool = False):
    if json == True:
        request = requests.get(f"https://meme-api.com/gimme/{subreddit}" if subreddit else f"https://meme-api.com/gimme/")
        request_json = request.json()
        return request_json
    else:
        request = requests.get(f"https://meme-api.com/gimme/{subreddit}" if subreddit else f"https://meme-api.com/gimme/")
        request_json = request.json()
        return request_json["url"]