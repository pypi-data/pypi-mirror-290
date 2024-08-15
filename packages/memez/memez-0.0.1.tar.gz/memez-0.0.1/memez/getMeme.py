import requests

def getMeme(subreddit: str, json: bool = False):
    if bool == True:
        request = requests.get(f"https://meme-api.com/gimme/{subreddit}" if subreddit else f"https://meme-api.com/gimme/")
        x = request.json()
        return x
    else:
        request = requests.get(f"https://meme-api.com/gimme/{subreddit}" if subreddit else f"https://meme-api.com/gimme/")
        x = request.json()
        return x["url"]